from django.shortcuts import render
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Department, Doctor, Queue, Ticket, QueueStatus, ConsultationRecord, Notification, Service
from .serializers import (
    DepartmentSerializer, DoctorSerializer, QueueSerializer, TicketSerializer,
    QueueStatusSerializer, ConsultationRecordSerializer, NotificationSerializer, ServiceSerializer
)

class IsAdminOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or hasattr(request.user, 'doctor')

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Queue.objects.none()
        user = self.request.user
        if user.is_staff or hasattr(user, 'doctor'):
            return Queue.objects.all()
        return Queue.objects.filter(department__is_active=True)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        queue = self.get_object()
        queue.is_active = not queue.is_active
        queue.save()
        return Response(QueueSerializer(queue).data)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Ticket.objects.none()
        user = self.request.user
        if user.is_staff or hasattr(user, 'doctor'):
            return Ticket.objects.all()
        return Ticket.objects.filter(patient=user)

    def perform_create(self, serializer):
        # Get the next ticket number
        last_ticket = Ticket.objects.order_by('-ticket_number').first()
        next_number = (last_ticket.ticket_number + 1) if last_ticket else 1
        
        # Create the ticket
        ticket = serializer.save(
            patient=self.request.user,
            ticket_number=next_number
        )
        
        # Update queue status
        queue_status, _ = QueueStatus.objects.get_or_create(
            department=ticket.department
        )
        queue_status.total_waiting = Ticket.objects.filter(
            department=ticket.department,
            status='WAITING'
        ).count()
        queue_status.save()
        
        # Send notification
        self._send_notification(ticket, 'TICKET_CREATED')

    @action(detail=False, methods=['get'])
    def my_position(self, request):
        user_tickets = Ticket.objects.filter(
            patient=request.user,
            status='WAITING'
        ).order_by('created_at')
        
        if not user_tickets.exists():
            return Response({'message': 'No active tickets'})
        
        ticket = user_tickets.first()
        waiting_count = Ticket.objects.filter(
            department=ticket.department,
            status='WAITING',
            created_at__lt=ticket.created_at
        ).count()
        
        return Response({
            'position': waiting_count + 1,
            'ticket': TicketSerializer(ticket).data
        })

    def _send_notification(self, ticket, notification_type):
        channel_layer = get_channel_layer()
        message = f"Ticket #{ticket.ticket_number} status updated"
        
        # Create notification
        Notification.objects.create(
            user=ticket.patient,
            ticket=ticket,
            notification_type=notification_type,
            message=message
        )
        
        # Send WebSocket notification
        async_to_sync(channel_layer.group_send)(
            f"user_{ticket.patient.id}",
            {
                "type": "notification",
                "message": message,
                "notification_type": notification_type
            }
        )

class TicketStatusUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrDoctor]

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Ticket.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = new_status
        ticket.save()
        
        # Update queue status
        queue_status = QueueStatus.objects.get(department=ticket.department)
        queue_status.total_waiting = Ticket.objects.filter(
            department=ticket.department,
            status='WAITING'
        ).count()
        queue_status.save()
        
        # Send notification
        if new_status == 'IN_PROGRESS':
            self._send_notification(ticket, 'TURN_NOW')
        
        return Response(TicketSerializer(ticket).data)

class QueueStatusViewSet(viewsets.ModelViewSet):
    serializer_class = QueueStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QueueStatus.objects.all()

    @action(detail=True, methods=['post'])
    def update_current_ticket(self, request, pk=None):
        queue_status = self.get_object()
        current_ticket_id = request.data.get('current_ticket_id')
        
        try:
            current_ticket = Ticket.objects.get(id=current_ticket_id)
            queue_status.current_ticket = current_ticket
            queue_status.save()
            
            # Update ticket status
            current_ticket.status = 'IN_PROGRESS'
            current_ticket.save()
            
            # Send notification
            self._send_notification(current_ticket, 'TURN_NOW')
            
            return Response(QueueStatusSerializer(queue_status).data)
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def toggle_queue(self, request, pk=None):
        queue_status = self.get_object()
        queue_status.is_active = not queue_status.is_active
        queue_status.save()
        return Response(QueueStatusSerializer(queue_status).data)

class ConsultationRecordViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultationRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrDoctor]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ConsultationRecord.objects.none()
        user = self.request.user
        if user.is_staff or hasattr(user, 'doctor'):
            return ConsultationRecord.objects.all()
        return ConsultationRecord.objects.filter(ticket__patient=user)

    def perform_create(self, serializer):
        ticket = serializer.validated_data['ticket']
        ticket.status = 'COMPLETED'
        ticket.save()
        
        # Update queue status
        queue_status = QueueStatus.objects.get(department=ticket.department)
        queue_status.total_waiting = Ticket.objects.filter(
            department=ticket.department,
            status='WAITING'
        ).count()
        queue_status.save()
        
        serializer.save()

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'message': 'All notifications marked as read'})

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Service.objects.none()
        user = self.request.user
        if user.is_staff or hasattr(user, 'doctor'):
            return Service.objects.all()
        return Service.objects.filter(department__is_active=True, is_active=True)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        service = self.get_object()
        service.is_active = not service.is_active
        service.save()
        return Response(ServiceSerializer(service).data)

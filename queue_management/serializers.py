from rest_framework import serializers
from .models import Department, Doctor, Queue, Ticket, QueueStatus, ConsultationRecord, Notification, Service
from users.serializers import UserProfileSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'

class QueueSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Queue
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    patient = UserProfileSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'patient', 'department', 'doctor', 'department_id', 
                 'doctor_id', 'ticket_number', 'status', 'created_at', 
                 'updated_at', 'estimated_wait_time', 'actual_wait_time')
        read_only_fields = ('id', 'ticket_number', 'created_at', 'updated_at')

class QueueStatusSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    current_ticket = TicketSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    current_ticket_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = QueueStatus
        fields = ('id', 'department', 'current_ticket', 'department_id', 
                 'current_ticket_id', 'is_active', 'total_waiting', 
                 'average_wait_time', 'last_updated')
        read_only_fields = ('id', 'last_updated')

class ConsultationRecordSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    ticket_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ConsultationRecord
        fields = ('id', 'ticket', 'doctor', 'ticket_id', 'doctor_id', 
                 'diagnosis', 'prescription', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class NotificationSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    ticket_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'ticket', 'user_id', 'ticket_id', 
                 'notification_type', 'message', 'is_read', 'created_at')
        read_only_fields = ('id', 'created_at') 
from django.contrib import admin
from .models import Department, Doctor, Ticket, QueueStatus, ConsultationRecord, Notification

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'specialization', 'is_active')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'specialization')
    list_filter = ('department', 'is_active')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'patient', 'department', 'doctor', 'status', 'created_at')
    search_fields = ('ticket_number', 'patient__email', 'patient__first_name', 'patient__last_name')
    list_filter = ('status', 'department', 'created_at')
    ordering = ('-created_at',)

@admin.register(QueueStatus)
class QueueStatusAdmin(admin.ModelAdmin):
    list_display = ('department', 'current_ticket', 'is_active', 'total_waiting', 'last_updated')
    list_filter = ('department', 'is_active')
    ordering = ('department',)

@admin.register(ConsultationRecord)
class ConsultationRecordAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'doctor', 'created_at')
    search_fields = ('ticket__ticket_number', 'doctor__user__email', 'diagnosis')
    list_filter = ('doctor', 'created_at')
    ordering = ('-created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'message')
    list_filter = ('notification_type', 'is_read', 'created_at')
    ordering = ('-created_at',)

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    duration = models.DurationField(help_text="Expected duration of the service")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    class Meta:
        ordering = ['name']

class Queue(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    max_wait_time = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    class Meta:
        ordering = ['name']

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    ticket_number = models.PositiveIntegerField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_wait_time = models.DurationField(null=True, blank=True)
    actual_wait_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.patient.get_full_name()}"

    class Meta:
        ordering = ['-created_at']

class QueueStatus(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    current_ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_waiting = models.PositiveIntegerField(default=0)
    average_wait_time = models.DurationField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department.name} Queue Status"

    class Meta:
        verbose_name_plural = "Queue Statuses"

class ConsultationRecord(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation for {self.ticket}"

    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    TYPE_CHOICES = [
        ('TICKET_CREATED', 'Ticket Created'),
        ('TURN_NEAR', 'Turn Near'),
        ('TURN_NOW', 'Turn Now'),
        ('QUEUE_UPDATE', 'Queue Update'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} - {self.user.get_full_name()}"

    class Meta:
        ordering = ['-created_at']

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'doctors', views.DoctorViewSet, basename='doctor')
router.register(r'queues', views.QueueViewSet, basename='queue')
router.register(r'tickets', views.TicketViewSet, basename='ticket')
router.register(r'queue-status', views.QueueStatusViewSet, basename='queue-status')
router.register(r'consultations', views.ConsultationRecordViewSet, basename='consultation')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'services', views.ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
    # Additional custom endpoints
    path('tickets/<int:pk>/status/', views.TicketStatusUpdateView.as_view(), name='ticket-status-update'),
] 
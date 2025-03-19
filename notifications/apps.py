from django.apps import AppConfig
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        import notifications.signals  # noqa

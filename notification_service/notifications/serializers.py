from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'user_id', 'notification_type', 
            'subject', 'message', 'status', 'created_at', 'sent_at'
        ]
        read_only_fields = ['status', 'created_at', 'sent_at']
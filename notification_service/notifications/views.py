from rest_framework import generics, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification_task

class NotificationCreateView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()
        
        # Queue the notification task
        send_notification_task.delay(notification.id)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NotificationHistoryView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Notification.objects.filter(user_id=user_id)
from celery import shared_task
from .models import Notification
from .utils import send_email, send_sms, send_push_notification

@shared_task
def send_notification_task(notification_id):
    notification = Notification.objects.get(id=notification_id)
    
    try:
        if notification.notification_type == 'email':
            send_email(
                to=notification.user.email,
                subject=notification.subject,
                body=notification.message
            )
        elif notification.notification_type == 'sms':
            send_sms(
                phone_number=notification.user.phone,
                message=notification.message
            )
        elif notification.notification_type == 'push':
            send_push_notification(
                user_id=notification.user_id,
                title=notification.subject,
                message=notification.message
            )
            
        notification.status = 'delivered'
    except Exception as e:
        notification.status = 'failed'
        notification.message += f"\nError: {str(e)}"
    
    notification.save()
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from .base import PaymentStrategy

class PayPalPaymentStrategy(PaymentStrategy):
    def __init__(self):
        environment = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID,
            client_secret=settings.PAYPAL_SECRET
        )
        self.client = PayPalHttpClient(environment)

    def process_payment(self, amount, currency, **kwargs):
        try:
            request = OrdersCaptureRequest(kwargs['order_id'])
            response = self.client.execute(request)
            
            if response.result.status == 'COMPLETED':
                return {
                    'success': True,
                    'payment_id': response.result.id,
                    'amount': response.result.purchase_units[0].amount.value
                }
            return {'success': False, 'error': 'Payment not completed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
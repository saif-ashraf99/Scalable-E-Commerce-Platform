import stripe
from .base import PaymentStrategy

class StripePaymentStrategy(PaymentStrategy):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def process_payment(self, amount, currency, **kwargs):
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency.lower(),
                payment_method=kwargs['payment_method_id'],
                confirmation_method='manual',
                confirm=True
            )
            return {
                'success': True,
                'payment_id': payment_intent.id,
                'client_secret': payment_intent.client_secret
            }
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
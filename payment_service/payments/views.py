from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .processor import PaymentProcessor
from .strategies import StripePaymentStrategy, PayPalPaymentStrategy
from .serializers import PaymentSerializer

class ProcessPaymentView(APIView):
    STRATEGY_MAP = {
        'stripe': StripePaymentStrategy,
        'paypal': PayPalPaymentStrategy
    }

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        gateway = request.data.get('gateway')
        strategy_class = self.STRATEGY_MAP.get(gateway)
        
        if not strategy_class:
            return Response(
                {'error': 'Invalid payment gateway'},
                status=status.HTTP_400_BAD_REQUEST
            )

        processor = PaymentProcessor(strategy_class())
        result = processor.execute_payment(
            amount=serializer.validated_data['amount'],
            currency=serializer.validated_data['currency'],
            **request.data.get('gateway_data', {})
        )

        if result['success']:
            payment = serializer.save(
                payment_id=result['payment_id'],
                status='completed'
            )
            return Response(PaymentSerializer(payment).data)
        
        payment = serializer.save(
            payment_id=result.get('payment_id', ''),
            status='failed'
        )
        return Response(
            {'error': result['error']},
            status=status.HTTP_400_BAD_REQUEST
        )
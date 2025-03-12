from abc import ABC, abstractmethod
from django.conf import settings

class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, **kwargs):
        pass
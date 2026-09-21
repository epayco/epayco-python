from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def create(self, payment_method, options):
        ...

    @abstractmethod
    def get(self, payment_method, ref_payco):
        ...

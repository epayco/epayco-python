from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    """Contrato único para crear/consultar una transacción, sin importar
    qué backend responde detrás (flujo legado o ms-transaction)."""

    @abstractmethod
    def create(self, payment_method, options):
        ...

    @abstractmethod
    def get(self, payment_method, ref_payco):
        ...

from epaycosdk.client import Client
from epaycosdk.gateways.base import PaymentGateway


class LegacyGateway(PaymentGateway):

    # Solo safetypay -- SDK-1032 es la unica card certificada para este
    # branch. No agregar cash/pse/daviplata aqui hasta que sus propias cards
    # (SDK-1030/1029/1031) esten certificadas y se despliegue cada una por
    # separado a green.
    _CREATE_ENDPOINTS = {
        "safetypay": ("payment/process/safetypay", False, True, False),
    }

    def __init__(self, epayco):
        self.epayco = epayco
        self.client = Client()

    def create(self, payment_method, options):
        url, switch, apify, pse = self._CREATE_ENDPOINTS[payment_method]
        return self.client.request(
            "POST", url, self.epayco.api_key, options, self.epayco.private_key,
            self.epayco.test, switch, self.epayco.lang, False, False, apify, pse,
        )

    def get(self, payment_method, ref_payco):
        raise NotImplementedError(
            "El flujo legado no tiene consulta para '{}'. Actívalo vía "
            "msTransactionMethods para usar esta capacidad nueva.".format(payment_method)
        )

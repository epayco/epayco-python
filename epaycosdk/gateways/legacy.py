from epaycosdk.client import Client
from epaycosdk.gateways.base import PaymentGateway


class LegacyGateway(PaymentGateway):

    _CREATE_ENDPOINTS = {
        "safetypay": ("payment/process/safetypay", False, True, False),
        "daviplata": ("payment/process/daviplata", False, True, False),
       
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

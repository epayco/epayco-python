from epaycosdk.client import Client
from epaycosdk.gateways.base import PaymentGateway


class LegacyGateway(PaymentGateway):
    """Reproduce el flujo legado (switch AES / apify) tal como epaycosdk lo
    hace hoy, vía Client.request() -- ningún backend nuevo, ninguna lógica
    reescrita. Cada historia de usuario registra aquí el endpoint del medio
    de pago que reemplaza al migrarlo, hasta que se retire por completo.

    No delega en las clases de epaycosdk.resources (Bank/Cash/Daviplata/
    Safetypay) a propósito: esas clases pasan por Epayco.gateway_for(), así
    que delegar en ellas produciría recursión. Este gateway contiene la
    llamada real a Client.request(), igual que antes vivía directo en cada
    método de recurso.
    """

    # payment_method -> (url, switch, apify, pse)
    _CREATE_ENDPOINTS = {
        "safetypay": ("payment/process/safetypay", False, True, False),
        # "pse": ("/pagos/debitos.json", True, False, True),               (SDK-1029)
        # "cash": ("payment/process/cash", True, False, True),             (SDK-1030)
        # "daviplata": ("payment/process/daviplata", False, True, False),  (SDK-1031)
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

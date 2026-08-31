import requests

from epaycosdk.gateways.base import PaymentGateway


class MsTransactionGateway(PaymentGateway):
    """Adaptador hacia el backend nuevo (ms-transaction). Traduce en ambas
    direcciones vía un RequestMapper/ResponseMapper por medio de pago, para
    que el resto del SDK -- y sus consumidores -- no vean el cambio.

    Cada historia de usuario registra su mapper en _MAPPERS al migrar un
    medio de pago. Ver el documento técnico (SDK-1029..SDK-1032) para el
    detalle de la arquitectura.
    """

    BASE_URL = "https://apiflow.epayco.io/payment/api"

    _MAPPERS = {}
    # Cada HU agrega su entrada aquí, p. ej.:
    # from epaycosdk.mappers.safetypay import SafetypayRequestMapper, SafetypayResponseMapper
    # _MAPPERS["safetypay"] = (SafetypayRequestMapper(), SafetypayResponseMapper())

    def __init__(self, epayco):
        self.epayco = epayco

    def create(self, payment_method, options):
        request_mapper, response_mapper = self._MAPPERS[payment_method]
        body = request_mapper.to_ms_transaction(options, self.epayco)
        response = requests.post(
            "{}/v1/{}/transactions".format(self.BASE_URL, payment_method),
            json=body,
            headers=self._headers(),
        )
        return response_mapper.to_sdk_response(response.json())

    def get(self, payment_method, ref_payco):
        _, response_mapper = self._MAPPERS[payment_method]
        response = requests.get(
            "{}/v1/{}/transactions".format(self.BASE_URL, payment_method),
            params={"ref_payco": ref_payco},
            headers=self._headers(),
        )
        return response_mapper.to_sdk_response(response.json())

    def _headers(self):
        # Placeholder -- el mecanismo real de auth es una pregunta abierta
        # de Fase 0 (documento técnico SDK-1029..1032). Los tickets solo
        # muestran un header X-CSRF-TOKEN con un valor literal idéntico en
        # los cuatro curls, que no parece una credencial reutilizable
        # servidor-a-servidor. No se hardcodea aquí hasta confirmarlo.
        return {"Accept": "application/json", "Content-Type": "application/json"}

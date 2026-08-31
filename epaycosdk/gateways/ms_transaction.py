import requests

from epaycosdk.client import Auth
from epaycosdk.gateways.base import PaymentGateway


class MsTransactionGateway(PaymentGateway):
    """Adaptador hacia el backend nuevo (ms-transaction). Traduce en ambas
    direcciones vía un RequestMapper/ResponseMapper por medio de pago, para
    que el resto del SDK -- y sus consumidores -- no vean el cambio.

    Cada historia de usuario registra su mapper en _MAPPERS al migrar un
    medio de pago. Ver el documento técnico (SDK-1029..SDK-1032) para el
    detalle de la arquitectura.
    """

    # Endpoint único para los cuatro medios de pago -- confirmado por QA
    # (SDK-1032): la ruta por medio de pago (/v1/<medio>/transactions, la
    # que mostraban los curls de los tickets) devuelve 404 real contra
    # ms-transaction. El medio de pago va en el body (request_mapper ya
    # arma "paymentMethod": "SP"/"PSE"/etc.), no en la URL.
    TRANSACTIONS_URL = "https://apiflow.epayco.io/payment/api/v1/transactions"

    # Auth: el mismo login "apify" que el SDK ya usa para Daviplata/
    # Safetypay/pseBank (epaycosdk.client.Auth -- Basic base64(public:
    # private) -> POST /login -> {"token": "<JWT>"}), contra este host.
    # No es un mecanismo nuevo: se reusa la clase Auth existente tal cual,
    # sin tocarla, solo apuntándola aquí. Confirmado real (SDK-1032, Fase
    # 0) -- se probaron antes v1 (/oauth/login, scope obligatorio, sin
    # documentar en ningún ticket) y v2 (/auth/login, JSON) del servicio de
    # autenticación nuevo; este login "apify" es el que corresponde usar.
    AUTH_HOST = "https://eks-apify-service.epayco.io"

    _MAPPERS = {}
    # Cada HU agrega su entrada aquí, p. ej.:
    # from epaycosdk.mappers.safetypay import SafetypayRequestMapper, SafetypayResponseMapper
    # _MAPPERS["safetypay"] = (SafetypayRequestMapper(), SafetypayResponseMapper())

    def __init__(self, epayco, auth=None):
        self.epayco = epayco
        self._auth = auth or Auth(epayco.api_key, epayco.private_key)

    def create(self, payment_method, options):
        request_mapper, response_mapper = self._MAPPERS[payment_method]
        body = request_mapper.to_ms_transaction(options, self.epayco)
        response = requests.post(
            self.TRANSACTIONS_URL,
            json=body,
            headers=self._headers(),
        )
        return response_mapper.to_sdk_response(response.json())

    def get(self, payment_method, ref_payco):
        _, response_mapper = self._MAPPERS[payment_method]
        response = requests.get(
            self.TRANSACTIONS_URL,
            params={"ref_payco": ref_payco},
            headers=self._headers(),
        )
        return response_mapper.to_sdk_response(response.json())

    def _headers(self):
        # Auth.make(BASE_URL, BASE_URL_APIFY, apify) solo usa BASE_URL_APIFY
        # cuando apify=True -- se pasa AUTH_HOST en ambos por firma, el
        # primero se ignora.
        token = self._auth.make(self.AUTH_HOST, self.AUTH_HOST, True)
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }

import requests

from epaycosdk.gateways.base import PaymentGateway


class MsTransactionAuth:
    """Login OAuth2 (client_credentials) contra el servicio de autenticación
    de ms-transaction -- confirmado manualmente en QA (Fase 0, SDK-1032),
    distinto del login JWT que usa el resto del SDK (epaycosdk.client.Auth).

    Forma real (no documentada en ningún ticket, descubierta por prueba y
    error contra el endpoint):
    - application/x-www-form-urlencoded, no JSON.
    - grant_type=client_credentials, client_id/client_secret = las mismas
      apiKey/privateKey del comercio que ya usa el resto del SDK (NO las
      credenciales P_CUST_ID/P_KEY -- esas dan 400 invalid_client en este
      endpoint).
    - scope es obligatorio -- sin él, el servicio responde 503 con un
      error interno (server_error) en vez de un 400 claro. No estaba en
      ningún ejemplo de los tickets.
    """

    LOGIN_URL = "https://eks-ms-authentication-service.epayco.io/api/v1/oauth/login"
    SCOPE = "ms-transaction"

    def token(self, epayco):
        response = requests.post(
            self.LOGIN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": epayco.api_key,
                "client_secret": epayco.private_key,
                "scope": self.SCOPE,
            },
        )
        data = response.json()
        access_token = (data.get("access_token") or {}).get("accessToken")
        if not access_token:
            # accessToken puede venir en false (no una excepción HTTP) cuando
            # el comercio existe pero no tiene el scope "ms-transaction"
            # autorizado todavía -- visto en QA con credenciales de prueba
            # reales. Falla explícito en vez de mandar "Bearer False".
            raise Exception(
                "No se pudo obtener token de ms-transaction (scope '{}'). "
                "El comercio puede no tener este scope autorizado todavía "
                "-- confirmar con backend antes de reintentar. Respuesta: "
                "{}".format(self.SCOPE, data)
            )
        return access_token


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

    _MAPPERS = {}
    # Cada HU agrega su entrada aquí, p. ej.:
    # from epaycosdk.mappers.safetypay import SafetypayRequestMapper, SafetypayResponseMapper
    # _MAPPERS["safetypay"] = (SafetypayRequestMapper(), SafetypayResponseMapper())

    def __init__(self, epayco, auth=None):
        self.epayco = epayco
        self._auth = auth or MsTransactionAuth()

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
        token = self._auth.token(self.epayco)
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }

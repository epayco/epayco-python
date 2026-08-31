import base64
import json

import requests

from epaycosdk.client import AESCipher, Auth
from epaycosdk.gateways.base import PaymentGateway
from epaycosdk.mappers.safetypay import SafetypayRequestMapper, SafetypayResponseMapper


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

    # Cifrado: la documentación real del endpoint (Swagger de
    # eks-ms-transaction-service, GET /docs?api-docs.json) confirma que
    # TODO el body debe ir cifrado AES-256-CBC excepto "publicKey", con el
    # mismo IV fijo que ya usa epaycosdk.client.AESCipher para el flujo
    # legado "switch" (el ejemplo del campo "i" en el spec decodifica
    # exactamente a este IV). Se reusa esa clase tal cual, sin tocarla.
    IV = "0000000000000000"

    _MAPPERS = {
        "safetypay": (SafetypayRequestMapper(), SafetypayResponseMapper()),  # SDK-1032
        # "pse": (...),        (SDK-1029)
        # "cash": (...),       (SDK-1030)
        # "daviplata": (...),  (SDK-1031)
    }

    def __init__(self, epayco, auth=None):
        self.epayco = epayco
        self._auth = auth or Auth(epayco.api_key, epayco.private_key)

    def create(self, payment_method, options):
        request_mapper, response_mapper = self._MAPPERS[payment_method]
        body = request_mapper.to_ms_transaction(options, self.epayco)
        response = requests.post(
            self.TRANSACTIONS_URL,
            json=self._encrypt(body),
            headers=self._headers(),
        )
        # options se pasa al mapper porque algunos campos legados (p. ej.
        # "country") no vienen sin enmascarar en la respuesta de
        # ms-transaction -- ver SafetypayResponseMapper.
        return response_mapper.to_sdk_response(response.json(), options)

    def get(self, payment_method, ref_payco):
        _, response_mapper = self._MAPPERS[payment_method]
        response = requests.get(
            self.TRANSACTIONS_URL,
            params={"ref_payco": ref_payco},
            headers=self._headers(),
        )
        return response_mapper.to_sdk_response(response.json())

    def _encrypt(self, body):
        """Cifra cada campo del body (menos publicKey) con AES-256-CBC,
        IV fijo -- misma mecánica que epaycosdk.client.AESCipher.encryptArray
        para el flujo legado "switch", generalizada para valores no-string
        (dict/list/bool/número), que ese método original no soporta.

        Los objetos anidados (p. ej. paymentMethodData) se cifran campo a
        campo, no como un bloque JSON -- confirmado por QA (SDK-1032): el
        backend rechaza "country"/"expirationDate" dentro de
        paymentMethodData como "no válidos" cuando se manda el objeto
        entero cifrado de una sola vez.
        """
        aes = AESCipher(self.epayco.private_key, self.IV)

        def encrypt_value(value):
            if isinstance(value, dict):
                return {k: encrypt_value(v) for k, v in value.items() if v is not None}
            raw = value if isinstance(value, str) else json.dumps(value)
            return aes.encrypt(raw).decode("utf-8")

        encrypted = {}
        for key, value in body.items():
            if key == "publicKey" or value is None:
                if value is not None:
                    encrypted[key] = value
                continue
            encrypted[key] = encrypt_value(value)
        encrypted["i"] = base64.b64encode(self.IV.encode("ascii")).decode("utf-8")
        # Obligatorio según la doc real del endpoint (confirmado por QA:
        # "El campo language es obligatorio" sin él) -- no estaba en
        # ningún ejemplo de los tickets originales.
        encrypted["language"] = encrypt_value("python")
        return encrypted

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

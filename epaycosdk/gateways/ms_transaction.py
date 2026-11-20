import base64
import json
import re
from urllib.parse import quote

import requests

from epaycosdk.client import AESCipher
from epaycosdk.gateways.base import PaymentGateway
from epaycosdk.mappers.base import LegacyResponseError
from epaycosdk.mappers.safetypay import SafetypayRequestMapper, SafetypayResponseMapper
from epaycosdk.mappers.daviplata import DaviplataRequestMapper, DaviplataResponseMapper
from epaycosdk.mappers.pse import PseRequestMapper, PseResponseMapper
from epaycosdk.mappers.cash import CashQueryResponseMapper, CashRequestMapper, CashResponseMapper
from epaycosdk.mappers.tdc import (
    InvalidChargeRequest, TdcRequestMapper, TdcResponseMapper, TdcQueryResponseMapper,
    TokenRequestMapper, TokenResponseMapper,
)


class MsTransactionGateway(PaymentGateway):

    BASE_URL = "https://apiflow.epayco.io/"
    TRANSACTIONS_URL = f"{BASE_URL}payment/api/v1/transactions"
    PSE_BANKS_URL = f"{BASE_URL}payment/api/v1/pse/banks"
    AUTH_URL = f"{BASE_URL}authentication/api/v2/login"
    TOKENIZATION_URL = f"{BASE_URL}payment/subscriptions/v1/tokenization/createToken"
    # La tokenizacion lleva PAN/CVC: no se deja la conexion colgada sin limite.
    TOKENIZATION_TIMEOUT = 30
    REQUEST_TIMEOUT = (5, 30)
    IV = "0000000000000000"
    REF_PAYCO_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,64}")

    _MAPPERS = {
        "safetypay": (SafetypayRequestMapper(), SafetypayResponseMapper()),
        "daviplata": (DaviplataRequestMapper(), DaviplataResponseMapper()),
        "pse": (PseRequestMapper(), PseResponseMapper()),
        "cash": (CashRequestMapper(), CashResponseMapper())
    }
    _QUERY_MAPPERS = {"cash": CashQueryResponseMapper()}

    def __init__(self, epayco):
        self.epayco = epayco

    def create(self, payment_method, options):
        request_mapper, response_mapper = self._MAPPERS[payment_method]
        try:
            body = request_mapper.to_ms_transaction(options, self.epayco)
        except LegacyResponseError as error:
            return error.response
        response = requests.post(
            self.TRANSACTIONS_URL,
            json=self._encrypt(body),
            headers=self._headers(),
            timeout=self.REQUEST_TIMEOUT,
        )
        return response_mapper.to_sdk_response(self._parse(response), options)
    
    def create_token(self, options):
        """Tokeniza la tarjeta en el servicio nuevo. El id devuelto es el
        tokenMdb que create_charge envia en paymentMethodData."""
        body = TokenRequestMapper().to_tokenization(options, self.epayco)
        response = requests.post(
            self.TOKENIZATION_URL, json=body, headers=self._headers(), timeout=self.TOKENIZATION_TIMEOUT
        )
        return TokenResponseMapper().to_sdk_response(
            self._parse(response), response.status_code, options, self.epayco.lang
        )

    def create_charge(self, options):
        try:
            body = TdcRequestMapper().to_ms_transaction(options, self.epayco)
        except InvalidChargeRequest as error:
            # Se responde el error sin pedir el token ni llamar a ms-transaction.
            return TdcResponseMapper().invalid_request_response(str(error), self.epayco.lang)
        response = requests.post(
            self.TRANSACTIONS_URL,
            json=self._encrypt(body),
            headers=self._headers(),
            timeout=self.REQUEST_TIMEOUT,
        )
        return TdcResponseMapper().to_sdk_response(
            self._parse(response), response.status_code, options, self.epayco.lang
        )

    def get_charge(self, ref_payco):
        if not self._valid_ref_payco(ref_payco):
            return TdcQueryResponseMapper().to_sdk_response(
                self._not_found(ref_payco), 422, None, self.epayco.lang
            )
        response = requests.get(
            self._transaction_url(ref_payco),
            headers=self._headers(),
            timeout=self.REQUEST_TIMEOUT,
        )
        return TdcQueryResponseMapper().to_sdk_response(
            self._parse(response), response.status_code, None, self.epayco.lang
        )

    def pse_banks(self):
        public_key = self.epayco.api_key

        url = f"{self.PSE_BANKS_URL}/{public_key}"
        headers = self._headers()

        response = requests.get(
            url,
            headers=headers,
            timeout=self.REQUEST_TIMEOUT,
        )
 
        return self._parse(response)

    def get(self, payment_method, ref_payco):
        _, response_mapper = self._MAPPERS[payment_method]
        response_mapper = self._QUERY_MAPPERS.get(payment_method, response_mapper)
        if not self._valid_ref_payco(ref_payco):
            return response_mapper.to_sdk_response(self._not_found(ref_payco))

        url = self._transaction_url(ref_payco)
        headers = self._headers()

        response = requests.get(
            url,
            headers=headers,
            timeout=self.REQUEST_TIMEOUT,
        )

      

        return response_mapper.to_sdk_response(
            self._parse(response)
        )

    def _valid_ref_payco(self, ref_payco):
        return isinstance(ref_payco, (str, int)) and not isinstance(ref_payco, bool) and bool(
            self.REF_PAYCO_PATTERN.fullmatch(str(ref_payco))
        )

    def _not_found(self, ref_payco):
        return {
            "success": False,
            "message": "Transaction request",
            "data": {
                "errorType": "ValidationException",
                "errorTypeDescription": "Information error",
                "errors": [{"code": "", "message": "Transaction # {} no encontrada.".format(ref_payco)}],
            },
        }

    def _transaction_url(self, ref_payco):
        return "{}/{}".format(self.TRANSACTIONS_URL, quote(str(ref_payco), safe=""))

    def _parse(self, response):
        try:
            return response.json()
        except ValueError:
            raise Exception(
                "ms-transaction respondió HTTP {} sin JSON válido: {}".format(
                    response.status_code, response.text[:300]
                )
            )

    def _encrypt(self, body):
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
        encrypted["language"] = encrypt_value("python")
        return encrypted

    def _get_token(self):
        response = requests.post(
            self.AUTH_URL,
            headers={"Content-Type": "application/json"},
            json={
                "client_id": self.epayco.api_key,
                "client_secret": self.epayco.private_key,
                "grant_type": "client_credentials",
            },
            timeout=self.REQUEST_TIMEOUT,
        )
        return self._parse(response)["data"]["token"]

    def _headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self._get_token()),
        }

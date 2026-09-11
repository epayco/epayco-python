import base64
import json

import requests

from epaycosdk.client import AESCipher
from epaycosdk.gateways.base import PaymentGateway
from epaycosdk.mappers.safetypay import SafetypayRequestMapper, SafetypayResponseMapper


class MsTransactionGateway(PaymentGateway):

    TRANSACTIONS_URL = "https://apiflow.epayco.io/payment/api/v1/transactions"
    AUTH_HOST = "https://apiflow.epayco.io"
    AUTH_PATH = "/authentication/api/v2/login"
    IV = "0000000000000000"

    _MAPPERS = {
        "safetypay": (SafetypayRequestMapper(), SafetypayResponseMapper()),
    }

    def __init__(self, epayco):
        self.epayco = epayco

    def create(self, payment_method, options):
        request_mapper, response_mapper = self._MAPPERS[payment_method]
        body = request_mapper.to_ms_transaction(options, self.epayco)
        response = requests.post(
            self.TRANSACTIONS_URL,
            json=self._encrypt(body),
            headers=self._headers(),
        )
        return response_mapper.to_sdk_response(self._parse(response), options)

    def get(self, payment_method, ref_payco):
        _, response_mapper = self._MAPPERS[payment_method]
        response = requests.get(
            self.TRANSACTIONS_URL,
            params={"ref_payco": ref_payco},
            headers=self._headers(),
        )
        return response_mapper.to_sdk_response(self._parse(response))

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
            "{}{}".format(self.AUTH_HOST, self.AUTH_PATH),
            headers={"Content-Type": "application/json"},
            json={
                "client_id": self.epayco.api_key,
                "client_secret": self.epayco.private_key,
                "grant_type": "client_credentials",
            },
        )
        return self._parse(response)["data"]["token"]

    def _headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self._get_token()),
        }

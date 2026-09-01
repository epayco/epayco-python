from epaycosdk.mappers.base import is_validation_error, legacy_validation_error_response


class DaviplataRequestMapper:

    def to_ms_transaction(self, options, epayco):
        options = options or {}
        return {
            "documentType": options.get("doc_type"),
            "document": options.get("document"),
            "names": options.get("name"),
            "lastNames": options.get("last_name"),
            "phone": options.get("phone"),
            "cellphone": options.get("cell_phone"),
            "email": options.get("email"),
            "responseUrl": options.get("url_response"),
            "confirmationUrl": options.get("url_confirmation"),
            "confirmationMethod": options.get("method_confirmation", "POST"),
            "amount": options.get("value"),
            "tax": options.get("tax", 0),
            "ico": options.get("ico", 0),
            "taxBase": options.get("tax_base", 0),
            "currency": options.get("currency", "COP"),
            "uniqueTransactionPerBill": options.get("unique_transaction_per_bill", False),
            "testMode": epayco.test,
            "paymentMethod": "DP",
            "country": options.get("country", "CO"),
            "ip": options.get("ip"),
            "description": options.get("description"),
            "integrationType": {"tipo_checkout": "api", "modo_pago": "payment"},
            "publicKey": epayco.api_key,
            "extras": {},
            "extrasEpayco": {
                "extra{}".format(i): options.get("extra{}".format(i), "") for i in range(1, 11)
            },
            "paymentMethodData": {},
        }


class DaviplataResponseMapper:

    _LAST_ACTION = "Registrar pago en daviplata"

    def to_sdk_response(self, ms_response, options=None):
        if is_validation_error(ms_response):
            return legacy_validation_error_response(ms_response)

        options = options or {}
        success = bool(ms_response.get("success"))
        data = ms_response.get("data") or {}
        provider_data = data.get("paymentProviderData") or {}
        if isinstance(provider_data, list):
            provider_data = {}
        extras_epayco_new = data.get("extrasEpayco") or {}
        amount = data.get("amount")

        return {
            "success": success,
            "titleResponse": "SUCCESS" if success else "Error",
            "textResponse": ms_response.get("message"),
            "lastAction": self._LAST_ACTION,
            "data": {
                "refPayco": data.get("refPayco"),
                "invoice": data.get("invoice"),
                "description": data.get("description"),
                "value": amount,
                "tax": data.get("tax"),
                "ico": data.get("ico"),
                "taxBase": data.get("taxBase"),
                "netoValue": amount,
                "currency": data.get("currency"),
                "bank": "DaviPlata",
                "estatus": data.get("status"),
                "response": data.get("response"),
                "autorization": data.get("authorization"),
                "receipt": data.get("receipt"),
                "date": data.get("date"),
                "franchise": data.get("franchise"),
                "codResponse": data.get("responseCode"),
                "codError": "",
                "ip": data.get("ip"),
                "testMode": data.get("testMode"),
                "docType": options.get("doc_type"),
                "document": options.get("document"),
                "name": options.get("name"),
                "lastName": options.get("last_name"),
                "email": options.get("email"),
                "city": data.get("city"),
                "address": options.get("address"),
                "indCountry": options.get("ind_country", ""),
                "idSessionToken": provider_data.get("paymentSessionId"),
                "tokenExpirationDate": provider_data.get("paymentSessionExpirationDate"),
                "daviplataOtpLab": None,
                "extras": data.get("extras") or {},
                "extras_epayco": {"extra5": extras_epayco_new.get("extra5", "")},
            },
        }

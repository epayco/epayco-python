from epaycosdk.mappers.base import is_validation_error, legacy_validation_error_response


class SafetypayRequestMapper:

    _ISO_ALPHA3 = {"CO": "COL"}

    def to_ms_transaction(self, options, epayco):
        options = options or {}
        return {
            "quotes": options.get("quotes", "1"),
            "documentType": options.get("doc_type"),
            "document": options.get("document"),
            "names": options.get("name"),
            "lastNames": options.get("last_name"),
            "phone": options.get("phone"),
            "cellphone": options.get("cell_phone"),
            "address": options.get("address"),
            "city": options.get("city"),
            "email": options.get("email"),
            "responseUrl": options.get("url_response"),
            "confirmationUrl": options.get("url_confirmation"),
            "confirmationMethod": options.get("method_confirmation", "POST"),
            "amount": options.get("value"),
            "tax": options.get("tax", 0),
            "ico": options.get("ico", 0),
            "baseTax": options.get("tax_base", 0),
            "currency": options.get("currency", "COP"),
            "uniqueTransactionPerBill": options.get("unique_transaction_per_bill", False),
            "testMode": epayco.test,
            "paymentMethod": "SP",
            "country": options.get("country", "CO"),
            "ip": options.get("ip"),
            "description": options.get("description"),
            "publicKey": epayco.api_key,
            "extras": {},
            "extrasEpayco": {
                "extra{}".format(i): options.get("extra{}".format(i), "") for i in range(1, 11)
            },
            "paymentMethodData": {
                "country": self._ISO_ALPHA3.get(
                    options.get("country", "CO"), options.get("country", "CO")
                ),
                "expirationDate": options.get("end_date"),
            },
        }


class SafetypayResponseMapper:

    _LAST_ACTION = "Envio Transaction Safetypay"

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

        return {
            "success": success,
            "titleResponse": "Ok" if success else ms_response.get("message"),
            "textResponse": ms_response.get("message"),
            "lastAction": self._LAST_ACTION,
            "data": {
                "refPayco": data.get("refPayco"),
                "invoice": data.get("invoice"),
                "description": data.get("description"),
                "value": data.get("amount"),
                "tax": data.get("tax"),
                "ico": data.get("ico"),
                "taxBase": data.get("taxBase"),
                "currency": data.get("currency"),
                "status": data.get("status"),
                "response": data.get("response"),
                "codResponse": data.get("responseCode", ""),
                "codError": "",
                "autorization": data.get("authorization"),
                "receipt": data.get("receipt"),
                "date": data.get("date"),
                "country": options.get("country", "CO"),
                "city": data.get("city"),
                "urlBank": provider_data.get("urlPayment", ""),
                "transactionId": data.get("refPayco"),
                "ticketId": data.get("receipt"),
                "extras": data.get("extras") or {},
                "extras_epayco": {"extra5": extras_epayco_new.get("extra5", "")},
            },
        }

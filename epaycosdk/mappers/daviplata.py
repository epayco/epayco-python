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

    def to_sdk_response(self, ms_response, options=None):
        return ms_response

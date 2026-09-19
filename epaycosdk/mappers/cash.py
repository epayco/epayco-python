from epaycosdk.mappers.base import is_validation_error, legacy_validation_error_response, legacy_status_code


class CashRequestMapper:

 def to_ms_transaction(self, options, epayco):
    options = options or {}
    body = {
        "invoice": options.get("invoice"),
        "quotes": options.get("quotes", "1"),
        "documentType": options.get("doc_type"),
        "document": options.get("docNumber"),
        "names": options.get("name"),
        "lastNames": options.get("last_name"),
        "phone": options.get("phone"),
        "cellphone": options.get("cellPhone"),
        "address": options.get("address", ""),
        "city": options.get("city", ""),
        "email": options.get("email"),
        "amount": options.get("value"),
        "tax": options.get("tax", 0),
        "ico": options.get("ico", 0),
        "taxBase": options.get("tax_base", 0),
        "currency": options.get("currency", "COP"),
        "testMode": epayco.test,
        "uniqueTransactionPerBill": options.get("unique_transaction_per_bill", False),
        "paymentMethod": "CASH",
        "paymentMethodData": {
            "franchise": options.get("paymentMethod")
        },
        "country": options.get("country", "CO"),
        "ip": options.get("ip"),
        "responseUrl": options.get("url_response"),
        "confirmationUrl": options.get("url_confirmation"),
        "confirmationMethod": options.get("metodoconfirmacion", "POST"),
        "description": options.get("description"),
        "integrationType": {"tipo_checkout": "smart_checkout", "modo_pago": "cash"},
        "publicKey": epayco.api_key,
        "extras": {
            "extra{}".format(i): options.get("extra{}".format(i), "") for i in range(1, 11)
        },
        "extrasEpayco": {"extra5": "P43"}
    }

    # Split Payment block
    split_info = options.get("split_payment")
    if split_info:
        # credits go inside paymentMethodData
        credits = split_info.get("credits")
        if credits:
            body["paymentMethodData"]["credits"] = credits

        # splitPayment goes at the root level of the body
        body["splitPayment"] = {
            "splitMethod": split_info.get("split_method", "multiple"),
            "splitAppId": split_info.get("split_app_id"),
            "splitMerchantId": split_info.get("split_merchant_id"),
            "splitType": split_info.get("split_type", "02"),
            "splitPrimaryReceiver": split_info.get("split_primary_receiver"),
            "splitPrimaryReceiverFee": split_info.get("split_primary_receiver_fee", "0"),
            "splitRule": split_info.get("split_rule", "multiple"),
            "splitReceivers": split_info.get("split_receivers", []),
        }

    return body
        

class CashResponseMapper:

    _LAST_ACTION = "Registrar pago en Cash"

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
        status = data.get("status")
        response_code = legacy_status_code(status, data.get("responseCode"))

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
                "total": data.get("subtotal", amount),
                "netoValue": amount,
                "currency": data.get("currency"),
                "bank": data.get("nameBank", "Cash"),
                "status": status,
                "response": data.get("response"),
                "autorization": data.get("authorization"),
                "receipt": data.get("receipt"),
                "date": data.get("date"),
                "paymentDate": data.get("date"),
                "franchise": data.get("franchise"),
                "codResponse": response_code,
                "codError": data.get("responseCode") or "",
                "ip": data.get("ip"),
                "testMode": data.get("testMode"),
                "docType": options.get("doc_type"),
                "document": options.get("docNumber") or options.get("document"),
                "name": options.get("name"),
                "lastName": options.get("last_name"),
                "email": options.get("email"),
                "city": options.get("city", ""),
                "address": options.get("address", "NA"),
                "indCountry": options.get("ind_country"),
                "pin": provider_data.get("pin"),
                "codeProject": provider_data.get("agreementCode"),
                "expirationDate": provider_data.get("expirationDate"),
                "conversionFactor": provider_data.get("trm"),
                "pesos": amount,
                "idSessionToken": provider_data.get("paymentSessionId"),
                "tokenExpirationDate": provider_data.get("paymentSessionExpirationDate"),
                "CashOtpLab": None,
                "extras": data.get("extras") or {},
                "extras_epayco": {"extra5": extras_epayco_new.get("extra5", "")},
            },
        }

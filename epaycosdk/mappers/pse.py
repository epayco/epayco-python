<<<<<<< HEAD
from epaycosdk.mappers.base import is_validation_error, legacy_validation_error_response
=======
from epaycosdk.mappers.base import is_validation_error, legacy_validation_error_response, legacy_status_code
>>>>>>> 00f1aebede90193425c7b8d560088cc0324e5702


class PseRequestMapper:

    _ISO_ALPHA3 = {"CO": "COL"}

    def to_ms_transaction(self, options, epayco):
        options = options or {}

        payment_method_data = {
            "typePerson": options.get("type_person"),
            "bankCode": options.get("bank"),
        }

        body = {
            "invoice": options.get("invoice"),
            "documentType": options.get("doc_type"),
<<<<<<< HEAD
            "document": options.get("document"),
            "names": options.get("name"),
            "lastNames": options.get("last_name"),
            "phone": options.get("phone"),
            "cellphone": options.get("cellphone"),
=======
            "document": options.get("docNumber") or options.get("document") or options.get("doc_number"),
            "names": options.get("name"),
            "lastNames": options.get("last_name"),
            "phone": options.get("phone"),
            "cellphone": options.get("cell_phone") or options.get("cellPhone"),
>>>>>>> 00f1aebede90193425c7b8d560088cc0324e5702
            "email": options.get("email"),
            "amount": options.get("value"),
            "tax": options.get("tax", 0),
            "ico": options.get("ico", 0),
            "taxBase": options.get("tax_base", 0),
            "currency": options.get("currency", "COP"),
            "uniqueTransactionPerBill": options.get("unique_transaction_per_bill", False),
            "testMode": epayco.test,
            "paymentMethod": "PSE",
            "paymentMethodData": payment_method_data,
            "country": options.get("country", "CO"),
<<<<<<< HEAD
            "city": options.get("city", ""),
            "ip": options.get("ip"),
            "responseUrl": options.get("url_response"),
            "confirmationUrl": options.get("url_confirmation"),
            "confirmationMethod": options.get("method_confirmation", "POST"),
=======
            "ip": options.get("ip"),
            "responseUrl": options.get("url_response"),
            "confirmationUrl": options.get("url_confirmation"),
            "confirmationMethod": options.get("metodoconfirmacion") or options.get("method_confirmation", "POST"),
>>>>>>> 00f1aebede90193425c7b8d560088cc0324e5702
            "description": options.get("description"),
            "integrationType": {
                "tipo_checkout": "onpage",
                "modo_pago": "PSE"
            },
            "publicKey": epayco.api_key,
            "extras": {
                "extra{}".format(i): options.get("extra{}".format(i), "") for i in range(1, 11)
            },
            "extrasEpayco": {"extra5": "P43"}
        }

        #  Bloque de Split Payment
        split_info = options.get("split_payment")
        if split_info:
            # credits van dentro de paymentMethodData
            credits = split_info.get("credits")
            if credits:
                payment_method_data["credits"] = credits

            # splitPayment va a nivel raíz del body
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

class PseResponseMapper:
<<<<<<< HEAD

    _LAST_ACTION = "Envio Transaction Pse"
=======
    """Replica el contrato historico de PSE legacy (/pagos/debitos.json), que
    usa nombres de campo en espanol/snake_case tanto a nivel raiz como en
    'data' -- distinto de safetypay/daviplata/cash, cuyo legacy (estilo
    apify) ya usaba nombres en ingles/camelCase equivalentes al del flujo
    nuevo. Ver comparacion legacy vs nuevo del 2026-09-18."""
>>>>>>> 00f1aebede90193425c7b8d560088cc0324e5702

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
<<<<<<< HEAD

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
=======
        cycle = provider_data.get("cycle")
        ticket_id = provider_data.get("ticketId", data.get("receipt"))
        estado = data.get("status")

        return {
            "success": success,
            "title_response": "SUCCESS" if success else "Error",
            "text_response": "Transaccion Creada Exitosamente" if success else ms_response.get("message"),
            "last_action": "get bank url",
            "data": {
                "ref_payco": data.get("refPayco"),
                "factura": data.get("invoice"),
                "descripcion": data.get("description"),
                "valor": data.get("amount"),
                "iva": data.get("tax"),
                "ico": data.get("ico"),
                "baseiva": data.get("taxBase"),
                "moneda": data.get("currency"),
                "estado": estado,
                "respuesta": data.get("response"),
                "cod_respuesta": legacy_status_code(estado, data.get("responseCode")),
                "cod_error": None,
                "autorizacion": data.get("authorization"),
                "ciudad": options.get("city", data.get("city")),
                "recibo": data.get("receipt"),
                "fecha": data.get("date"),
                "urlbanco": provider_data.get("urlPayment", ""),
                "transactionID": provider_data.get("trazabilityCode", data.get("authorization")),
                "ticketId": str(ticket_id) if ticket_id is not None else None,
                "extras": data.get("extras") or {},
                "extras_epayco": {"extra5": extras_epayco_new.get("extra5", "")},
                "ciclo": str(cycle) if cycle is not None else None,
>>>>>>> 00f1aebede90193425c7b8d560088cc0324e5702
            },
        }

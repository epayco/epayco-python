class SafetypayRequestMapper:
    """options público de hoy (ver Safetypay.create en README.rst) -> body
    anidado que pide ms-transaction (SDK-1032).

    Forma confirmada contra la documentación real del endpoint
    (eks-ms-transaction-service, GET /docs?api-docs.json -- ver
    SPPaymentMethodData): requiere paymentMethodData.country en ISO
    alfa-3 (ej. "COL"), distinto del campo raíz "country" que usa
    alfa-2 ("CO") como el resto del SDK. Confirmado por QA (SDK-1032):
    el backend rechazaba "CO" ahí con "El campo country no es válido".
    """

    # Alfa-2 -> alfa-3, solo lo que el SDK ya soporta como default hoy.
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
                # options["cash"] (flag legado "pago en efectivo Safetypay")
                # no tiene equivalente claro en el esquema nuevo -- no se
                # mapea hasta confirmar con backend (Fase 0).
                "expirationDate": options.get("end_date"),
            },
        }


class SafetypayResponseMapper:
    """Respuesta de ms-transaction -> misma forma que Safetypay.create()
    devuelve hoy en el flujo legado (apify).

    Mapeo confirmado comparando en QA (SDK-1032) las dos respuestas reales,
    misma transacción de prueba, contra los backends reales:

    Legado (apify)                       ms-transaction
    ------------------------------------ -----------------------------------
    success                              success
    titleResponse ("Ok")                 -- (no existe; se fija "Ok" si
                                             success, si no se usa message)
    textResponse                         message
    lastAction                           -- (no existe; se fija el mismo
                                             string estático que ya usaba
                                             el flujo legado para Safetypay)
    data.refPayco                        data.refPayco
    data.invoice                         data.invoice
    data.description                     data.description
    data.value                           data.amount
    data.tax / .ico / .taxBase           data.tax / .ico / .taxBase
    data.currency                        data.currency
    data.status                          data.status
    data.response                        data.response
    data.codResponse                     data.responseCode
    data.codError                        -- (no existe; "" como en legado)
    data.autorization (sic, typo legado) data.authorization
    data.receipt                         data.receipt
    data.date                            data.date
    data.country                         -- (viene enmascarado en
                                             payerInformation; se toma del
                                             options original, no de la
                                             respuesta)
    data.city                            data.city
    data.urlBank                         data.paymentProviderData.urlPayment
                                          (ausente/"" si el estado no lo trae
                                          -- visto en pruebas: solo viene
                                          poblado cuando status = Pendiente)
    data.transactionId                   data.refPayco
    data.ticketId                        data.receipt
    data.extras                          data.extras
    data.extras_epayco["extra5"]         data.extrasEpayco["extra5"]
                                          (el valor del marcador interno
                                          difiere -- P43 legado vs P51
                                          ms-transaction -- es un código de
                                          producto del backend, no algo que
                                          el consumidor del SDK dependa de
                                          leer; se pasa tal cual sin
                                          "corregirlo" a P43)

    Nota: options se recibe además de ms_response porque "country" no
    viene sin enmascarar en ningún campo de la respuesta nueva.
    """

    _LAST_ACTION = "Envio Transaction Safetypay"

    def to_sdk_response(self, ms_response, options=None):
        options = options or {}
        success = bool(ms_response.get("success"))
        data = ms_response.get("data") or {}
        provider_data = data.get("paymentProviderData") or {}
        # paymentProviderData puede venir como [] (lista vacía) cuando no
        # aplica en el estado actual de la transacción -- normalizado a {}.
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

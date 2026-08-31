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
    """Respuesta de ms-transaction -> misma forma que el SDK devuelve hoy.

    Placeholder deliberado: el ticket SDK-1032 no trae un ejemplo de
    respuesta real (éxito ni error). El mapeo de abajo NO se implementa
    hasta cerrar la Fase 0 del documento técnico -- esto solo fija dónde
    vive esa traducción para no bloquear el resto del gateway."""

    def to_sdk_response(self, ms_response):
        return ms_response  # TODO(Fase 0): mapear campo a campo

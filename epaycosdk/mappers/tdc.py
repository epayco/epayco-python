import json

import epaycosdk.errors as errors
from epaycosdk.mappers.base import legacy_status_code
from epaycosdk.utils import with_default_extra5


# Mensaje/descripcion que el legacy (/payment/v1/charge/create y v1/tokens)
# devuelve dentro de "data" cuando rechaza la solicitud por validacion.
# Verificado en vivo contra pre-prod (merchant 630339) el 2026-09-29.
_LEGACY_VALIDATION_MESSAGE = "Error validando datos"
_LEGACY_VALIDATION_DESCRIPTION = "Los datos son erroneos o son requeridos por favor compruebe."


class InvalidChargeRequest(ValueError):
    """Opciones de charge.create que no se pueden enviar a ms-transaction (hoy,
    un split que no se puede leer). El gateway responde el error sin cobrar."""


def _tdc_status_code(status, fallback):
    # Legacy de TDC devuelve 4 para "Fallida" (verificado en vivo 2026-09-29,
    # tarjeta 5170394490379427 en ambos flujos), no el 2 de la tabla comun
    # de mappers/base.py (verificada solo para Cash/PSE).
    if status == "Fallida":
        return 4
    return legacy_status_code(status, fallback)


def _legacy_card_mask(card_mask):
    # ms-transaction devuelve "5170399427" (6 primeros + 4 ultimos); la
    # consulta legada devuelve "517039*******9427".
    if isinstance(card_mask, str) and len(card_mask) == 10 and card_mask.isdigit():
        return card_mask[:6] + "*******" + card_mask[6:]
    return card_mask


def _as_number(value):
    # La consulta de ms-transaction trae ico como "0.00"; legacy devuelve 0.
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return value
        return int(number) if number.is_integer() else number
    return value


def _error_messages(ms_response):
    """Mensajes de error reales de ms-transaction o del servicio de
    tokenizacion. ms-transaction los trae en data.errors[].message
    (ValidationException); tokenizacion en data.error[] (lista de strings)."""
    data = ms_response.get("data") if isinstance(ms_response, dict) else None
    if isinstance(data, dict):
        errs = data.get("errors")
        if isinstance(errs, list) and errs:
            return " ".join(
                e.get("message") if isinstance(e, dict) else str(e) for e in errs
            )
        if isinstance(errs, str) and errs:
            return errs
        err = data.get("error")
        if isinstance(err, list) and err:
            return " ".join(str(e) for e in err)
        if isinstance(err, str) and err:
            return err
    if isinstance(ms_response, dict):
        return ms_response.get("textResponse") or ms_response.get("message") or ""
    return ""


def legacy_error_response(ms_response, http_code, lang, with_status_code=True):
    """Forma exacta que devuelve Client.request del legacy ante un 4xx:
    {status: False, message: "ErrorException: [103] ...", data: "<json>",
    errors: {http_code}}. "data" es un string JSON, igual que en legacy."""
    inner = {
        "status": False,
        "message": _LEGACY_VALIDATION_MESSAGE,
        "data": {
            "status": "error",
            "description": _LEGACY_VALIDATION_DESCRIPTION,
            "errors": _error_messages(ms_response),
        },
    }
    if with_status_code:
        inner["statusCode"] = http_code
    return {
        "status": False,
        "message": str(errors.ErrorException(lang or "ES", 103)),
        "data": json.dumps(inner),
        "errors": {"http_code": http_code},
    }


class TokenRequestMapper:
    """card[...] del token.create legado -> body del servicio de tokenizacion
    (POST payment/subscriptions/v1/tokenization/createToken)."""

    # El servicio solo acepta "cybersource" o "kms" (verificado: cualquier otro
    # valor responde 400 "providerTokenizer debe ser cybersource o kms"). "kms"
    # por defecto; el comercio puede enviar options["providerTokenizer"].
    PROVIDER_TOKENIZER = "kms"

    def to_tokenization(self, options, epayco):
        options = options or {}
        body = {
            "card[number]": options.get("card[number]"),
            "card[exp_month]": options.get("card[exp_month]"),
            "card[exp_year]": options.get("card[exp_year]"),
            "card[cvc]": options.get("card[cvc]"),
            "card[name]": options.get("card[name]"),
            "card[email]": options.get("card[email]"),
            "session": "API",
            "type": "single-payment",
            "providerTokenizer": options.get("providerTokenizer") or self.PROVIDER_TOKENIZER,
            "test": bool(epayco.test),
        }
        return {k: v for k, v in body.items() if v is not None}


class TokenResponseMapper:
    """Respuesta de tokenizacion -> forma de v1/tokens legado:
    {status, id, success, type, data, card: {exp_month, exp_year, name, mask}, object}."""

    def to_sdk_response(self, ms_response, http_code, options, lang):
        if not ms_response.get("success"):
            return legacy_error_response(ms_response, http_code, lang, with_status_code=False)
        options = options or {}
        data = ms_response.get("data") or {}
        card = dict(data.get("card") or {})
        # Legacy devuelve exp_month/exp_year antes de name/mask; el servicio
        # nuevo no los incluye, se toman de la solicitud.
        card = {
            "exp_month": options.get("card[exp_month]"),
            "exp_year": options.get("card[exp_year]"),
            **card,
        }
        return {
            "status": True,
            "id": data.get("id"),
            "success": bool(data.get("success", True)),
            "type": data.get("type", "card"),
            "data": data.get("data") or {},
            "card": card,
            "object": data.get("object", "token"),
        }


def _load_split_json(value, field):
    # Un split en string que no es JSON (p. ej. str() de un dict de Python) no
    # se puede descartar en silencio: el cobro saldria sin dispersion y con
    # success true.
    try:
        return json.loads(value)
    except (ValueError, RecursionError):
        raise InvalidChargeRequest("El campo {} no es un JSON válido".format(field)) from None


def _split_payment(options):
    """Acepta los dos formatos de split que ya usa el SDK: el plano de
    charge.create legado (splitpayment/split_app_id/... en la raiz, receptores
    con base_iva) y el dict anidado split_payment de Cash/PSE (tambien como
    string JSON). Un split que no se puede leer lanza InvalidChargeRequest."""
    nested = options.get("split_payment")
    if isinstance(nested, str):
        nested = _load_split_json(nested, "split_payment") if nested.strip() else None
    if nested is not None and not isinstance(nested, dict):
        raise InvalidChargeRequest("El campo split_payment debe ser un objeto JSON")
    if isinstance(nested, dict):
        src = nested
    elif str(options.get("splitpayment", "")).lower() == "true":
        src = options
    else:
        return None

    receivers = src.get("split_receivers") or []
    if isinstance(receivers, str):
        receivers = _load_split_json(receivers, "split_receivers")
    if not isinstance(receivers, list) or not all(isinstance(r, dict) for r in receivers):
        raise InvalidChargeRequest("El campo split_receivers debe ser una lista de receptores")
    mapped = []
    for r in receivers:
        mapped.append({
            "id": r.get("id"),
            "total": r.get("total"),
            "iva": r.get("iva", 0),
            "baseTax": r.get("baseTax", r.get("base_iva", 0)),
            "fee": r.get("fee", 0),
        })

    return {
        "splitMethod": src.get("split_method", "multiple"),
        "splitAppId": src.get("split_app_id"),
        "splitMerchantId": src.get("split_merchant_id"),
        "splitType": src.get("split_type", "02"),
        "splitPrimaryReceiver": src.get("split_primary_receiver"),
        "splitPrimaryReceiverFee": src.get("split_primary_receiver_fee", "0"),
        "splitRule": src.get("split_rule", "multiple"),
        "splitReceivers": mapped,
    }


def _extras_epayco(options):
    # extrasEpayco (convencion del resto de mappers de ms-transaction) gana si
    # trae algun valor; si no, se usa extras_epayco (la del legado).
    for key in ("extrasEpayco", "extras_epayco"):
        extras = options.get(key)
        if isinstance(extras, dict) and any(v not in (None, "") for v in extras.values()):
            return extras
    return None


class TdcRequestMapper:
    """Opciones de charge.create legado -> body TDC de ms-transaction.

    customer_id/use_default_card_customer no se envian: ms-transaction cobra
    directo contra el tokenMdb (verificado en vivo, no requiere customer)."""

    def to_ms_transaction(self, options, epayco):
        options = options or {}
        extras = options.get("extras")
        if not isinstance(extras, dict):
            extras = {}
        extras = {
            "extra{}".format(i): extras.get("extra{}".format(i), options.get("extra{}".format(i), ""))
            for i in range(1, 11)
        }
        body = {
            "invoice": options.get("bill") or options.get("invoice"),
            "documentType": options.get("doc_type"),
            "document": options.get("doc_number"),
            "names": options.get("name"),
            "lastNames": options.get("last_name"),
            "phone": options.get("phone"),
            "cellphone": options.get("cell_phone"),
            "address": options.get("address"),
            "city": options.get("city"),
            "email": options.get("email"),
            "amount": options.get("value"),
            "tax": options.get("tax", 0),
            "ico": options.get("ico", 0),
            "taxBase": options.get("tax_base", 0),
            "currency": options.get("currency", "COP"),
            # Debe ser booleano literal: omitirlo hace 500 en ms-transaction.
            "uniqueTransactionPerBill": bool(options.get("unique_transaction_per_bill", False)),
            "testMode": epayco.test,
            "paymentMethod": "TDC",
            # quotes va DENTRO de paymentMethodData (en la raiz se ignora).
            "paymentMethodData": {
                "tokenMdb": options.get("token_card"),
                "quotes": str(options.get("dues") or options.get("quotes") or "1"),
            },
            "country": options.get("country", "CO"),
            "ip": options.get("ip"),
            "responseUrl": options.get("url_response") or options.get("url_confirmation"),
            "confirmationUrl": options.get("url_confirmation"),
            "confirmationMethod": options.get("method_confirmation", "POST"),
            "description": options.get("description"),
            # tipo_checkout "api" es el que devuelve el bloque 3DS real.
            "integrationType": {"tipo_checkout": "api", "modo_pago": "payment"},
            "publicKey": epayco.api_key,
            "extras": extras,
            "extrasEpayco": with_default_extra5(_extras_epayco(options)),
        }
        split = _split_payment(options)
        if split:
            body["splitPayment"] = split
        return body


def _cc_network_response(data):
    # ms-transaction devuelve ccNetworkResponse vacio; legacy lo arma con el
    # codigo y el texto de respuesta de la red (verificado: Aceptada ->
    # {"code": "00", "message": "Aprobada"}, Rechazada -> {"code": "04", ...}).
    provider = data.get("paymentProviderData") or {}
    network = provider.get("ccNetworkResponse") or {}
    if network.get("code"):
        return {"code": network.get("code"), "message": network.get("name") or network.get("message")}
    return {"code": data.get("responseCode"), "message": data.get("response")}


class TdcResponseMapper:
    """Respuesta de ms-transaction -> forma de /payment/v1/charge/create legado."""

    def to_sdk_response(self, ms_response, http_code, options, lang):
        if not ms_response.get("success"):
            return legacy_error_response(ms_response, http_code, lang)

        options = options or {}
        data = ms_response.get("data") or {}
        provider = data.get("paymentProviderData") or {}
        if isinstance(provider, list):
            provider = {}
        amount = data.get("amount")
        status = data.get("status")

        response = {
            "status": True,
            "success": True,
            "type": "Create payment",
            "data": {
                "ref_payco": data.get("refPayco"),
                "factura": data.get("invoice"),
                "descripcion": data.get("description"),
                "valor": amount,
                "iva": data.get("tax"),
                "ico": data.get("ico"),
                "baseiva": data.get("taxBase"),
                "valorneto": data.get("subtotal", amount),
                "moneda": data.get("currency"),
                "banco": data.get("nameBank"),
                "estado": status,
                "respuesta": data.get("response"),
                "autorizacion": data.get("authorization"),
                "recibo": data.get("receipt"),
                "fecha": data.get("date"),
                "franquicia": data.get("franchise"),
                "cod_respuesta": _tdc_status_code(status, data.get("responseCode")),
                "cod_error": data.get("responseCode"),
                "ip": data.get("ip"),
                "enpruebas": data.get("testMode"),
                "tipo_doc": options.get("doc_type"),
                "documento": options.get("doc_number"),
                "nombres": options.get("name"),
                "apellidos": options.get("last_name"),
                "email": options.get("email"),
                "ciudad": data.get("city") or options.get("city"),
                # Sin address, el legado responde "SIN DIRECCION" (verificado
                # 2026-09-28) y ms-transaction guarda lo mismo.
                "direccion": options.get("address") or "SIN DIRECCION",
                # Pais emisor de la tarjeta: ms-transaction no lo expone
                # (payerInformation.country viene enmascarado). Sin equivalente.
                "ind_pais": None,
                "country_card": None,
                "extras": data.get("extras") or {},
                "cc_network_response": _cc_network_response(data),
                "extras_epayco": {"extra5": (data.get("extrasEpayco") or {}).get("extra5", "")},
            },
            "object": "payment",
        }
        three_ds = provider.get("threeDsAuthentication")
        if three_ds:
            response["data"]["3DS"] = three_ds
        return response

    def invalid_request_response(self, message, lang):
        """Error de validacion del legado para un cobro que no se envio a
        ms-transaction (InvalidChargeRequest)."""
        return legacy_error_response({"data": {"errors": message}}, 400, lang)


class TdcQueryResponseMapper:
    """GET ms-transaction /transactions/{ref} -> forma de
    /transaction/response.json legado (campos x_*)."""

    def to_sdk_response(self, ms_response, http_code, options, lang):
        if not ms_response.get("success"):
            return {
                "success": False,
                "title_response": "Error",
                "text_response": _error_messages(ms_response) or ms_response.get("message"),
                "last_action": "Consultar Transaccion",
                "data": {},
            }

        data = ms_response.get("data") or {}
        provider = data.get("paymentProviderData") or {}
        if isinstance(provider, list):
            provider = {}
        payer = data.get("payerInformation") or {}
        extras = data.get("extras") or {}
        status = data.get("status")
        code = _tdc_status_code(status, data.get("responseCode"))
        amount = data.get("amount")
        ref = data.get("refPayco")

        out = {
            "x_ref_payco": ref,
            "x_id_factura": data.get("invoice"),
            "x_id_invoice": data.get("invoice"),
            "x_description": data.get("description"),
            "x_mpd_points": provider.get("accumulatedPoints", 0),
            "x_amount": amount,
            "x_amount_country": amount,
            "x_amount_ok": amount,
            "x_tax": data.get("tax"),
            "x_tax_ico": _as_number(data.get("ico")),
            "x_amount_base": data.get("taxBase"),
            "x_currency_code": data.get("currency"),
            "x_bank_name": data.get("nameBank"),
            "x_cardnumber": _legacy_card_mask(provider.get("cardMask")),
            "x_respuesta": status,
            "x_response": status,
            "x_approval_code": data.get("authorization"),
            "x_transaction_id": data.get("receipt"),
            "x_fecha_transaccion": data.get("date"),
            "x_transaction_date": data.get("date"),
            "x_cod_respuesta": code,
            "x_cod_response": code,
            "x_response_reason_text": data.get("response"),
            "x_cod_transaction_state": code,
            "x_transaction_state": status,
            "x_errorcode": data.get("responseCode"),
            "x_franchise": data.get("franchise"),
            "x_customer_doctype": payer.get("documentType"),
            "x_customer_document": payer.get("document"),
            "x_customer_name": payer.get("names"),
            "x_customer_lastname": payer.get("lastNames"),
            "x_customer_email": payer.get("email"),
            "x_customer_country": payer.get("country"),
            "x_customer_city": data.get("city"),
            "x_customer_address": payer.get("address"),
            "x_customer_ip": data.get("ip"),
            "x_test_request": "TRUE" if data.get("testMode") else "FALSE",
            "x_transaction_cycle": None,
            "paymentProviderData": {"accumulatedPoints": provider.get("accumulatedPoints", 0)},
        }
        for i in range(1, 11):
            out["x_extra{}".format(i)] = extras.get("extra{}".format(i), "")
        out["x_extra5_epayco"] = (data.get("extrasEpayco") or {}).get("extra5", "")
        return {
            "success": True,
            "title_response": "Correcto",
            "text_response": "Transacción consultada existosamente",
            "last_action": "Consultar Transaccion",
            "data": out,
        }

import math
import re
from datetime import datetime

from epaycosdk.mappers.base import LegacyResponseError, is_validation_error, legacy_status_code
from epaycosdk.mappers.tdc import _error_messages
from epaycosdk.utils import with_default_extra5

FRANCHISE_POINTS = {"EF": "efecty", "BA": "baloto", "GA": "gana", "RS": "red servi", "PR": "punto red", "SR": "sured"}
MINIMUM_AMOUNTS = {"EF": 20000, "RS": 10000, "PR": 10000}
LEGACY_UNSUPPORTED_FRANCHISES = {"BA"}
DATE_PREFIX_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})[ T]")
NUMERIC_PIN_FRANCHISES = {"GA", "SR"}
NUMERIC_AGREEMENT_FRANCHISES = {"EF"}
REQUIRED_FIELDS = (("value", "value"), ("doc_type", "docType"), ("docNumber", "docNumber"), ("name", "name"),
                   ("last_name", "lastName"))
MAX_EMAIL_LENGTH = 254
EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+")

EXPIRATION_DATE_ERROR = ("E024", "Fecha expiración pago invalida o menor a la fecha actual")
MINIMUM_AMOUNT_ERROR = ("E014", "La transacción no se puede iniciar, monto minimo no superado")
TOTALS_ERROR = ("E036", "Error al validar totales, iva, o base iva")
LEGACY_TRANSACTION_ERRORS = (
    (re.compile(r"expirationDate no es v", re.I), EXPIRATION_DATE_ERROR),
    (re.compile(r"document type seleccionado|campo document es inv", re.I),
     ("E003", "El tipo de documento y documento no coinciden")),
    (re.compile(r"currency seleccionado no es v|campo currency es obligatorio", re.I), ("E021", "Moneda no soportada")),
    (re.compile(r"validar totales", re.I), TOTALS_ERROR),
    (re.compile(r"monto m[ií]nimo", re.I), MINIMUM_AMOUNT_ERROR),
    (re.compile(r"monto m[aá]ximo", re.I), ("E015", "La transacción no se puede iniciar, monto máximo superado")),
    (re.compile(r"factura o referencia", re.I), ("E035", "Número de factura o referencia cliente duplicada")),
)
NON_NUMERIC_AMOUNT_DETAIL = "Undefined property: stdClass::$data"
COLLECTION_AMOUNT_DETAIL = "Array to string conversion"
QUERY_LAST_ACTION = "Consultar Transaccion"
UNSUPPORTED_FRANCHISE_CODE = 109
UNSUPPORTED_FRANCHISE_DETAIL = ("[109] Método de pago en efectivo no válido, unicamnete soportados: efecty, baloto, gana, "
                                "redservi, puntored, sured, apostar, susuerte")


def _error_list(errors):
    return {"totalErrors": len(errors), "errors": [{"codError": code, "errorMessage": message} for code, message in errors]}


def _data_validation_response(errors):
    return {
        "success": False,
        "titleResponse": "Error",
        "textResponse": "Algunos campos son obligatorios, corrija los errores e intente nuevamente",
        "lastAction": "validation data",
        "data": _error_list(errors),
    }


def _transaction_validation_response(errors):
    return {
        "success": False,
        "titleResponse": "Error",
        "textResponse": "Algunos campos son invalidos, por favor corrija los errores y vuelva a intentarlo",
        "lastAction": "validation transaction",
        "data": _error_list(errors),
    }


def _payment_method_error_response():
    return {
        "success": False,
        "titleResponse": "Error payment method",
        "textResponse": "Error create transaction",
        "lastAction": "valid_payment_method",
        "data": _error_list([("A002", "El campo 'paymentMethod' es invalido")]),
    }


def _internal_error_response(detail, code=0):
    return {
        "success": False,
        "titleResponse": "Error code: {}".format(code),
        "textResponse": "Error internal server: {}".format(detail or ""),
        "lastAction": "NA",
        "data": _error_list([("AE100", "Error interno en el servidor, no se logró realizar la acción")]),
    }


def _is_blank(value):
    return value is None or (isinstance(value, str) and not value.strip())


def _to_number(value):
    try:
        number = float(value if isinstance(value, (bool, int, float)) else str(value).strip())
    except (ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def _missing_field_errors(options):
    errors = [("A001", "El campo '{}' es requerido".format(label))
              for key, label in REQUIRED_FIELDS if _is_blank(options.get(key))]
    email = options.get("email")
    if email is None:
        errors.append(("A001", "El campo 'email' es requerido"))
    elif not (isinstance(email, str) and len(email) <= MAX_EMAIL_LENGTH and EMAIL_PATTERN.fullmatch(email)):
        errors.append(("A002", "el campo 'email' debe ser tipo email"))
    if _is_blank(options.get("cellPhone")):
        errors += [("A001", "El campo 'cellPhone' es requerido")] * 2
    if options.get("paymentMethod") is None:
        errors.append(("A001", "El campo 'paymentMethod' es requerido"))
    return errors


def _amount_errors(amount, tax, franchise):
    errors = []
    if amount < MINIMUM_AMOUNTS.get(franchise, 0):
        errors.append(MINIMUM_AMOUNT_ERROR)
    if amount <= 0 or tax < 0 or tax > amount:
        errors.append(TOTALS_ERROR)
    if amount <= 0:
        errors.append(MINIMUM_AMOUNT_ERROR)
    return errors


def _expiration_date(end_date):
    match = DATE_PREFIX_PATTERN.match(str(end_date))
    return match.group(1) if match else str(end_date).strip()


def _expiration_date_errors(end_date):
    if _is_blank(end_date):
        return []
    try:
        datetime.strptime(_expiration_date(end_date), "%Y-%m-%d")
    except ValueError:
        return [EXPIRATION_DATE_ERROR]
    return []


def _legacy_input_error(options, franchise):
    missing = _missing_field_errors(options)
    if missing:
        return _data_validation_response(missing)
    if franchise not in FRANCHISE_POINTS:
        return _payment_method_error_response()
    if franchise in LEGACY_UNSUPPORTED_FRANCHISES:
        return _internal_error_response(UNSUPPORTED_FRANCHISE_DETAIL, UNSUPPORTED_FRANCHISE_CODE)
    value = options.get("value")
    if isinstance(value, (list, tuple, dict)):
        return _internal_error_response(COLLECTION_AMOUNT_DETAIL)
    amount = _to_number(value)
    if amount is None:
        return _internal_error_response(NON_NUMERIC_AMOUNT_DETAIL)
    transaction_errors = _expiration_date_errors(options.get("end_date"))
    transaction_errors += _amount_errors(amount, _to_number(options.get("tax", 0)) or 0, franchise)
    return _transaction_validation_response(transaction_errors) if transaction_errors else None


def _upper(value):
    return value.upper() if isinstance(value, str) else value


class CashRequestMapper:

 def to_ms_transaction(self, options, epayco):
    options = options or {}
    franchise = str(_upper(options.get("paymentMethod")))
    input_error = _legacy_input_error(options, franchise)
    if input_error:
        raise LegacyResponseError(input_error)
    body = {
        "invoice": options.get("invoice"),
        "quotes": options.get("quotes", "1"),
        "documentType": options.get("doc_type"),
        "document": options.get("docNumber"),
        "names": options.get("name"),
        "lastNames": options.get("last_name"),
        "phone": options.get("phone"),
        "cellphone": options.get("cellPhone", ""),
        "address": options.get("address", ""),
        "city": options.get("city", ""),
        "email": options.get("email"),
        "amount": options.get("value"),
        "tax": options.get("tax", 0),
        "ico": options.get("ico", 0),
        "taxBase": options.get("tax_base", 0),
        "currency": _upper(options.get("currency", "COP")),
        "testMode": epayco.test,
        "uniqueTransactionPerBill": options.get("unique_transaction_per_bill", False),
        "paymentMethod": "CASH",
        "paymentMethodData": {
            "franchise": franchise
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
        "extrasEpayco": with_default_extra5(options.get("extrasEpayco"))
    }

    if not _is_blank(options.get("end_date")):
        body["paymentMethodData"]["expirationDate"] = _expiration_date(options["end_date"])

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
        

def _translate_validation_errors(ms_errors):
    translated = []
    for error in ms_errors:
        message = str(error.get("message") or "")
        known = next((legacy for pattern, legacy in LEGACY_TRANSACTION_ERRORS if pattern.search(message)), None)
        entry = known or (error.get("code"), error.get("message"))
        if entry not in translated:
            translated.append(entry)
    return translated


def _legacy_response_text(response, point):
    if not isinstance(response, str) or not point:
        return response
    for backend_name in (point, point.replace(" ", "")):
        if response.lower().endswith(backend_name):
            return response[:len(response) - len(backend_name)] + point.title()
    return response


def _as_number(value):
    return int(value) if isinstance(value, str) and value.strip().isdigit() else value


def _as_text(value):
    return value if value is None else str(value)


class CashResponseMapper:

    def to_sdk_response(self, ms_response, options=None):
        if is_validation_error(ms_response):
            errors = (ms_response.get("data") or {}).get("errors") or []
            return _transaction_validation_response(_translate_validation_errors(errors))
        if not ms_response.get("success"):
            return _internal_error_response(ms_response.get("message"))
        return _legacy_transaction(ms_response.get("data") or {}, options or {})


class CashQueryResponseMapper:

    def to_sdk_response(self, ms_response, options=None):
        if not ms_response.get("success"):
            return {
                "success": False,
                "titleResponse": "Error",
                "textResponse": _error_messages(ms_response),
                "lastAction": QUERY_LAST_ACTION,
                "data": {},
            }
        transaction = _legacy_transaction(ms_response.get("data") or {}, {})
        return {
            "success": True,
            "titleResponse": "Correcto",
            "textResponse": "Transacción consultada existosamente",
            "lastAction": QUERY_LAST_ACTION,
            "data": transaction["data"],
        }


def _legacy_transaction(data, options):
    provider_data = data.get("paymentProviderData") or {}
    if isinstance(provider_data, list):
        provider_data = {}
    extras_epayco_new = data.get("extrasEpayco") or {}
    amount = data.get("amount")
    status = data.get("status")
    franchise = data.get("franchise")
    point = FRANCHISE_POINTS.get(franchise, str(data.get("nameBank") or "").lower())
    pin = provider_data.get("pin")
    agreement_code = provider_data.get("agreementCode")

    return {
        "success": True,
        "titleResponse": "SUCCESS",
        "textResponse": "Transacción y pin generados exitosamente",
        "lastAction": "Crear pin {}".format(point),
        "data": {
            "refPayco": data.get("refPayco"),
            "invoice": data.get("invoice"),
            "description": data.get("description") or "",
            "value": amount,
            "tax": data.get("tax"),
            "ico": data.get("ico"),
            "taxBase": data.get("taxBase"),
            "total": data.get("subtotal", amount),
            "currency": data.get("currency"),
            "bank": point.upper(),
            "status": status,
            "response": _legacy_response_text(data.get("response"), point),
            "autorization": data.get("authorization"),
            "receipt": data.get("receipt"),
            "date": data.get("date"),
            "franchise": franchise,
            "codResponse": legacy_status_code(status, data.get("responseCode")),
            "codError": data.get("responseCode") or "",
            "ip": data.get("ip"),
            "testMode": data.get("testMode"),
            "docType": options.get("doc_type"),
            "document": options.get("docNumber") or options.get("document"),
            "name": options.get("name"),
            "lastName": options.get("last_name"),
            "email": options.get("email"),
            "city": options.get("city", ""),
            "address": "NA",
            "indCountry": None,
            "pin": _as_number(pin) if franchise in NUMERIC_PIN_FRANCHISES else _as_text(pin),
            "codeProject": (_as_number(agreement_code) if franchise in NUMERIC_AGREEMENT_FRANCHISES
                            else _as_text(agreement_code)),
            "paymentDate": data.get("date"),
            "expirationDate": provider_data.get("expirationDate"),
            "conversionFactor": provider_data.get("trm"),
            "pesos": amount,
            "extras": data.get("extras") or {},
            "extras_epayco": {"extra5": extras_epayco_new.get("extra5", "")},
        },
    }

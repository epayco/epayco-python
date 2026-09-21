def is_validation_error(ms_response):
    data = ms_response.get("data") or {}
    return isinstance(data, dict) and "errorType" in data


def legacy_validation_error_response(ms_response):
    data = ms_response.get("data") or {}
    errors = data.get("errors") or []
    return {
        "success": False,
        "titleResponse": "Error",
        "textResponse": "Algunos campos son obligatorios, corrija los errores e intente nuevamente",
        "lastAction": "validation data",
        "data": {
            "totalErrors": len(errors),
            "errors": [
                {"codError": e.get("code"), "errorMessage": e.get("message")}
                for e in errors
            ],
        },
    }


# Mapeo de 'estado'/'status' -> x_cod_transaction_state, el codigo numerico
# de estado que usa todo el ecosistema legado de ePayco (el mismo que
# consumen los webhooks/plugins, ej. WooCommerce), distinto del codigo de
# negocio que trae ms-transaction (ej. 'P004'/'0000'). Basado en el switch
# real de x_cod_transaction_state usado por los plugins:
#   1            -> Approved / Aceptada
#   2, 4, 10, 11 -> Cancelled, failed or rejected / Rechazada, Fallida, Cancelada
#   3, 7         -> Pending / Pendiente
#   6            -> Reversed / Reversada
# Confirmado ademas empiricamente comparando legacy vs ms-transaction el
# 2026-09-19: tanto Cash como PSE devuelven 3 para 'Pendiente'. Para
# cualquier estado que no este en esta tabla se usa el valor de
# ms-transaction como respaldo (mejor esfuerzo, no confirmado).
_LEGACY_STATUS_CODES = {
    "Aceptada": 1,
    "Rechazada": 2,
    "Fallida": 2,
    "Cancelada": 2,
    "Pendiente": 3,
    "Reversada": 6,
}


def legacy_status_code(status, fallback):
    """Codigo numerico legado para el estado dado, si ya fue verificado
    contra legacy real; si no, devuelve fallback (valor de ms-transaction)."""
    return _LEGACY_STATUS_CODES.get(status, fallback)

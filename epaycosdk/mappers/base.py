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


# Mapeo de 'estado'/'status' -> codigo numerico interno del backend legado,
# distinto del codigo de negocio que trae ms-transaction (ej. 'P004'/'0000').
# Confirmado empiricamente comparando legacy vs ms-transaction el 2026-09-19:
# tanto Cash como PSE devuelven el entero 3 para 'Pendiente'. Solo se agregan
# aqui los estados ya verificados contra una respuesta real de legacy -- para
# cualquier otro estado se usa el valor de ms-transaction como respaldo
# (mejor esfuerzo, no confirmado). Ampliar esta tabla a medida que se
# verifiquen mas estados (Aceptada, Rechazada, Fallida, etc).
_LEGACY_STATUS_CODES = {
    "Pendiente": 3,
}


def legacy_status_code(status, fallback):
    """Codigo numerico legado para el estado dado, si ya fue verificado
    contra legacy real; si no, devuelve fallback (valor de ms-transaction)."""
    return _LEGACY_STATUS_CODES.get(status, fallback)

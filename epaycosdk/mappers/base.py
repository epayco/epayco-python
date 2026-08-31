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

DEFAULT_EXTRA5 = "P43"


def with_default_extra5(extras):
    """Copy of the integrator's extras_epayco/extrasEpayco dict with extra5 set to
    the SDK's "P43" marker only when it was not sent (or was sent empty)."""
    extras = dict(extras) if isinstance(extras, dict) else {}
    if extras.get("extra5") in (None, ""):
        extras["extra5"] = DEFAULT_EXTRA5
    return extras

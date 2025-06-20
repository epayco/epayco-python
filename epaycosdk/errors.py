import urllib.request
import ssl
import json
# No verificar el certifcado para los request
ssl._create_default_https_context = ssl._create_unverified_context
# Se Extiende de la clase Exception y se inicializa la url en s3
class EpaycoException(Exception):
    ERRORS_URL = "https://multimedia.epayco.co/message-api/errors.json"
    pass

class ErrorException(Exception):
    def __init__(self, code, details=None):
        self.code = code
        self.details = details
        super().__init__(f"Error {code} : {details}")

    def __str__(self):
        try:
            return f"Error {self.code} {self.details.get('message', '')}"
        except Exception as e:
            return f"Error al obtener el mensaje: {str(e)}"

import urllib.request
import ssl
import json
# No verificar el certifcado para los request
ssl._create_default_https_context = ssl._create_unverified_context
# Se Extiende de la clase Exception y se inicializa la url en s3
class EpaycoException(Exception):
    ERRORS_URL = "https://s3-us-west-2.amazonaws.com/epayco/message_api/errors.json"
    pass

class ErrorException(EpaycoException):
    # Se inicializa pasando los argmentos codigo e idioma
    def __init__(self, idioma,code):
            self.code=code
            self.message = idioma
    # Se carga el json de la url se parsea y de devuelve el código del error de acuerdo al idioma
    def __str__(self):
        # Se carga el json de la url
        request = urllib.request.Request(self.ERRORS_URL)
        # Se abre el json de la url
        response = urllib.request.urlopen(request)
        # Se decodifica en utf8
        encoding = response.info().get_content_charset('utf8')
        # Se carga el json en la variable errors
        errors = json.loads(response.read().decode(encoding))
        # Se retorna el error de acuerdo al idioma y código pasado
        return "ErrorException:{"+errors[str(self.code)][self.message]+"}\n"

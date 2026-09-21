import base64

from Crypto.Cipher import AES

from epaycosdk.client import pad


class AESCipher:
    """Cifrado AES-256-CBC campo por campo para el body de ms-transaction.

    Independiente del pipeline de cifrado que ya usa Client.request() para
    los endpoints legacy 'switch' -- no se toca ese codigo existente, este es
    un mecanismo nuevo y aislado, solo usado por MsTransactionGateway.
    """

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, row):
        raw = pad(row).encode("utf8")
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc)

    def encryptArray(self, data):
        aux = {}
        for key, value in data.items():
            if key == "extras_epayco" and isinstance(value, dict) and "extra5" in value:
                aux[key] = {"extra5": self.encrypt(value["extra5"]).decode('utf-8')}
            else:
                aux[key] = self.encrypt(value).decode('utf-8')
        return aux

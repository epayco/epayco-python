import urllib.request
import urllib.parse
import ssl
import json
import base64
import hashlib
from Crypto.Cipher import AES
import requests
import pyepayco.errors as errors
#import os

from requests.exceptions import ConnectionError
from pathlib import Path

# No verificar el certifcado para los request
ssl._create_default_https_context = ssl._create_unverified_context

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-(s[-1])]

BASE_DIR = Path(__file__).resolve().parent.parent
EPAYCO_KEY_LANG_FILE = str(BASE_DIR.joinpath('pyepayco/utils/key_lang.json'))
#Dir = os.path.join(EPAYCO_KEY_LANG_FILE, 'key_lang.json')


class AESCipher:
    def __init__( self, key,iv  ):
        self.key = key
        self.iv = iv    

    def encrypt( self, row ):
          
    
        raw = pad(row).encode("utf8")
        cipher = AES.new( self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc)
        #         cipher = AES.new( raw.encode("utf8"), AES.MODE_CBC, iv().encode("utf8") )
        # return base64.b64encode(cipher.encrypt( pad(raw) ) ).strip()
    def decrypt( self, enc ):
       
        enc = base64.b64decode(enc)
        cipher = AES.new( self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')

    def encryptArray(self,data):
        aux = {}
        for key, value in data.items():
            aux[key] = self.encrypt(value)
        return aux

class Util():

    def setKeys(self, array={}):

        file = open(EPAYCO_KEY_LANG_FILE, 'r').read()
        values = json.loads(file)
        aux = {}
        for key, value in array.items():
            if key in values:
                aux[values[key]] = value
            else:
                aux[key] = value
        return aux

class Client:

    BASE_URL = "https://api.secure.payco.co";
    BASE_URL_SECURE = "https://secure.payco.co";
    IV = "0000000000000000";
    LANGUAGE = "python";
    SWITCH= False

    def __init__(self):

        pass



    """
    Make request and return a Python object from the JSON response. If
    HTTP method is DELETE return True for 204 response, false otherwise.
    :param method: String with the HTTP method
    :param url: String with the EndPoint Api
    :param api_key: String with the API key
    :param data: Dictionary with query strings
    :param private_key: String with the Private key Api
    :param test: String TRUE O FALSE transaction in pruebas or production
    :param swich: Dictionary with data that will be sent
    :param lang: String languaje response errors
    :return: Native python object resulting of the JSON deserialization of the API response
    """


    def request(self,method='POST',url="",api_key="",data={}, private_key="",test="", switch="", lang="",cashdata="" ):
        dataSet = None

        if (switch and hasattr(data, "__len__")):
            util = Util()
            data = util.setKeys(data)
           
        self.SWITCH=switch

        headers = {'Content-Type':'application/json','Accept' : "application/json" ,'type':'sdk'}


        try:
            if (method == "GET"):
                if (switch):
                    if (test):
                        test = "TRUE"
                    else:
                        test = "FALSE"

                    #Encriptamos el enpruebas
                    aes = AESCipher(private_key,self.IV)
                    enpruebas=aes.encrypt(test)

                    addData = {
                        'public_key': api_key,
                        'i': base64.b64encode(self.IV.encode('ascii')),
                        'lenguaje': self.LANGUAGE,
                        'enpruebas': enpruebas,
                    }

                    url_params = addData
                    url_params.update(data)
                    response=requests.get(self.build_url(url), data={},params=url_params,auth=(api_key, ""),headers=headers)

                else:
                    url_params=data
                    #url_params.update({"public_key":api_key,'test':test})
                    response=requests.get(self.build_url(url),data={},params=url_params,auth=(api_key,""),headers=headers)

            elif (method == "POST"):
                if (switch):
                    if(test):
                        test= "TRUE"
                    else:
                        test= "FALSE"

                    
                    if(cashdata):
                        aes = AESCipher(private_key,self.IV)
                        enpruebas = aes.encrypt(test)

                        encryptData = data
                        #encryptData = aes.encryptArray(data)
                        addData = {
                            "public_key": api_key,
                            "i": base64.b64encode(self.IV.encode('ascii')),
                            "enpruebas": enpruebas,
                            "lenguaje": self.LANGUAGE,
                            "p": ""
                        }
                        enddata = {}
                        enddata.update(encryptData)
                        enddata.update(addData)
                        data=enddata
                        #print('//',data)
                        response = requests.post(self.build_url(url),params=data, auth=(api_key, ''),headers=headers)
                        #response = enddata
                        #print('/////////////////////////////////////////////////')
                       
                    else:
                        aes = AESCipher(private_key,self.IV)
                        enpruebas = aes.encrypt(test)

                        encryptData = None
                        encryptData = aes.encryptArray(data)
                        addData = {
                            'public_key': api_key,
                            'i': base64.b64encode(self.IV.encode('ascii')),
                            'enpruebas': enpruebas,
                            'lenguaje': self.LANGUAGE,
                            'p': ''
                        }
                        enddata = {}
                        enddata.update(encryptData)
                        enddata.update(addData)
                        data=enddata
                        response = requests.post(self.build_url(url),params=data, auth=(api_key, ''),headers=headers)
                        #response = enddata
                        #print('***************************************')



                else:
                    #Agregamos la llave publica
                    #data.update({'public_key':api_key,'test': test})
                    data.update({'test': test})
                    data=json.dumps(data)
                    response = requests.post(
                        self.build_url(url),
                        data=data,
                        auth=(api_key, ''),
                        headers=headers
                    )

            elif (method == "PATCH"):
                response = requests.request(
                    method,
                    self.build_url(url),
                    data=json.dumps(data),
                    auth=(api_key, ""),
                    headers=headers
                )
            elif (method == "DELETE"):
                response = requests.request(
                    method,
                    self.build_url(url),
                    data=json.dumps(data),
                    auth=(api_key, ""),
                    headers=headers
                )
        except Exception:
            raise  errors.ErrorException(lang, 101)

        if (response.status_code >= 200 and response.status_code <= 206):
            if (method == "DELETE"):
                return response.status_code == 204 or response.status_code == 200;

            return response.json()

        if (response.status_code == 400):
            code = 0;
            message = "";

            raise errors.ErrorException(lang, 103)

        if (response.status_code == 401):

            raise errors.ErrorException(lang, 104)

        if (response.status_code == 404):

            raise errors.ErrorException(lang, 105)

        if (response.status_code == 403):

            raise errors.ErrorException(lang, 106)

        if (response.status_code == 405):

            raise errors.ErrorException(lang, 107)


        raise errors.ErrorException(lang, 102)

    def build_url(self,endpoint):
            """
            Build complete URL from API endpoint
            :param endpoint: String with the endpoint, ex: /v1/charges/
            :return: String with complete URL, ex: https://api.secure.payco.co/v1/charges/
            """
            if(self.SWITCH):
                return "{base_url}/{endpoint}".format(
                    base_url=self.BASE_URL_SECURE,
                    endpoint=endpoint
                )
            else:
                return "{base_url}/{endpoint}".format(
                    base_url=self.BASE_URL,
                    endpoint=endpoint
                    
                )
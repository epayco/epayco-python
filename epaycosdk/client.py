import urllib.request
import urllib.parse
import ssl
import json
import base64
import hashlib
from Crypto.Cipher import AES
import requests
import epaycosdk.errors as errors
import os
import sys
from requests.exceptions import ConnectionError
from pathlib import Path
from dotenv import load_dotenv
from requests import Session

load_dotenv() 

# No verificar el certifcado para los request
ssl._create_default_https_context = ssl._create_unverified_context

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-(s[-1])]

BASE_DIR = Path(__file__).resolve().parent.parent
EPAYCO_KEY_LANG_FILE = str(BASE_DIR.joinpath('epaycosdk/utils/key_lang.json'))
EPAYCO_KEY_LANG_FILE_APIFY = str(BASE_DIR.joinpath('epaycosdk/utils/key_lang_apify.json'))

class AESCipher:
    def __init__( self, key,iv  ):
        self.key = key
        self.iv = iv    

    def encrypt( self, row ):
        raw = pad(row).encode("utf8")
        cipher = AES.new( self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc)
    def decrypt( self, enc ):
       
        enc = base64.b64decode(enc)
        cipher = AES.new( self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')

    def encryptArray(self,data):
        aux = {}
        values = {"extras_epayco":"extras_epayco"}
        for key, value in data.items():
            if key in values:
                aux[values[key]] = json.dumps({'extra5':json.loads(value)["extra5"].__str__()})
            else:
                aux[key] = self.encrypt(value)
        return aux

class Util():

    def setKeys(self, array={},sp=''):
        file = open(EPAYCO_KEY_LANG_FILE, 'r').read()
        values = json.loads(file)
        aux = {}
        for key, value in array.items():
            if key in values:
                aux[values[key]] = value
            else:
                aux[key] = value
        return aux

    def setKeys_apify(self, array={}):
        file = open(EPAYCO_KEY_LANG_FILE_APIFY, 'r').read()
        values = json.loads(file)
        aux = {}
        for key, value in array.items():
            if key in values:
                aux[values[key]] = value
            else:
                aux[key] = value
        return aux


class Auth:
    def __init__( self, api_key, private_key ):
        self.api_key = api_key
        self.private_key = private_key

    def make(self, BASE_URL, BASE_URL_APIFY, apify):
        url = BASE_URL_APIFY + "/login" if apify else BASE_URL + "/v1/auth/login"
        payload = "{\"public_key\":\""+self.api_key+"\",\"private_key\":\""+self.private_key+"\"}"
        headers = {
            'Content-Type': 'application/json',
            'type': 'sdk-jwt',
            'Accept': 'application/json'
        }

        if (apify):
            text = "{public}:{private}".format(
                    public=self.api_key,
                    private=self.private_key
                )
            encode = base64.b64encode(text.encode("utf-8"))
            token = str(encode, "utf-8")
            headers["Authorization"] = "Basic {token}".format(token=token)
            payload = ""
        response = requests.request("POST", url, headers=headers, data = payload)
        data=response.text.encode('utf8')
        json_data=json.loads(data)
        bearer_token=json_data['token'] if apify else json_data['bearer_token']
        return bearer_token
        
class NoRebuildAuthSession(Session):
    def rebuild_auth(self, prepared_request, response):
        """
        No code here means requests will always preserve the Authorization
        header when redirected.
        Be careful not to leak your credentials to untrusted hosts!
        """

class Client:

    BASE_URL = os.getenv("BASE_URL_SDK") if os.getenv("BASE_URL_SDK") else "https://api.secure.payco.co"
    BASE_URL_SECURE = os.getenv("SECURE_URL_SDK") if os.getenv("SECURE_URL_SDK") else"https://secure.payco.co"
    ENTORNO = os.getenv("ENTORNO_SDK") if os.getenv("ENTORNO_SDK") else "/restpagos"
    BASE_URL_APIFY = os.getenv("BASE_URL_APIFY") if os.getenv("BASE_URL_APIFY") else "https://apify.epayco.co"
    IV = "0000000000000000"
    LANGUAGE = "python"
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


    def request(self,method='POST',url="",api_key="",data={}, private_key="",test="", switch="", lang="",cashdata="",dt="", apify=False ):
        auth = Auth(api_key, private_key)
        authentication = auth.make(self.BASE_URL,self.BASE_URL_APIFY,apify)
        token_bearer = 'Bearer ' +authentication
        util = Util()
        if(apify):
            data = util.setKeys_apify(data)
        elif (hasattr(data, "__len__")):
            if(switch):
                data = util.setKeys(data)

        self.SWITCH=switch  
        self.APIFY=apify
        headers = {
            'Content-Type': 'application/json',
            'type': 'sdk-jwt',
            'lang': 'PYTHON',
            'Authorization': token_bearer
        }

        try:
            if (method == "GET"):
                if (switch):
                    if test == True or test == "true":
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
                    payload = {}
                    session = NoRebuildAuthSession()
                    response = session.get(self.build_url(url), headers=headers, data = payload, params=url_params)
                    
                 
            elif (method == "POST"):
                data["extras_epayco"] = json.dumps({"extra5":"P43"})
                if (switch):
                    if test == True or test == "true":
                        test= "TRUE"
                    else:
                        test= "FALSE"
                    aes = AESCipher(private_key, self.IV)
                    enpruebas = aes.encrypt(test)
                    if(cashdata):
                        encryptData = data  
                    else:
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

                else:
                    #Agregamos la llave publica
                    if(dt):
                        data=json.dumps(data)
                        response = requests.request("POST", self.build_url(url), headers=headers, data = data)
                    else:
                        enddata = {}
                        data.update({'test': test})
                        enddata.update(data)
                        data = enddata
                        response = requests.post(self.build_url(url), params=data, headers=headers)


            elif (method == "PATCH"):
                response = requests.request(
                    method,
                    self.build_url(url),
                    data=json.dumps(data),
                    auth=(token_bearer, ""),
                    headers=headers
                )
            elif (method == "DELETE"):
                response = requests.request(
                    method,
                    self.build_url(url),
                    data=json.dumps(data),
                    auth=(token_bearer, ""),
                    headers=headers
                )
        except Exception:
            raise  errors.ErrorException(lang, 101)

        if (response.status_code >= 200 and response.status_code <= 206):
            if (method == "DELETE"):
                return response.status_code == 204 or response.status_code == 200

            return response.json()

        if (response.status_code == 400):
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
            if(self.APIFY):
                return "{base_url}/{endpoint}".format(
                    base_url=self.BASE_URL_APIFY,
                    endpoint=endpoint
                )
            elif(self.SWITCH):
                return "{base_url}{entorno}{endpoint}".format(
                    base_url=self.BASE_URL_SECURE,
                    entorno=self.ENTORNO,
                    endpoint=endpoint
                )
            else:
                return "{base_url}/{endpoint}".format(
                    base_url=self.BASE_URL,
                    endpoint=endpoint   
                )
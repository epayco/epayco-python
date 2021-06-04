import epaycosdk.resources
from epaycosdk.resources import Token
from epaycosdk.resources import Customers
from epaycosdk.resources import Plan
from epaycosdk.resources import Subscriptions
from epaycosdk.resources import Bank
from epaycosdk.resources import Cash
from epaycosdk.resources import Charge
#from epaycosdk.resources import Safetypay

class Epayco:

    public_key = ""
    api_key = ""
    test = False
    lang = "ES"

    def __init__(self, options):
        self.api_key = options["apiKey"]
        self.private_key = options["privateKey"]
        self.test = "true" if options["test"] else "false"
        self.lang = options["lenguage"]

        self.token = Token(self)
        self.customer = Customers(self)
        self.plan = Plan(self)
        self.subscriptions = Subscriptions(self)
        self.bank = Bank(self)
        self.cash = Cash(self)
        self.charge=Charge(self)
        #self.safetypay=Safetypay(self)

import pyepayco.resources
from pyepayco.resources import Token
from pyepayco.resources import Customers
from pyepayco.resources import Plan
from pyepayco.resources import Subscriptions
from pyepayco.resources import Bank
from pyepayco.resources import Cash
from pyepayco.resources import Charge
from pyepayco.resources import Safetypay

class Epayco:

    public_key = ""
    api_key = ""
    test = False
    lang = "ES"

    def __init__(self, options):
        self.api_key = options["apiKey"]
        self.private_key = options["privateKey"]
        self.test = options["test"]
        self.lang = options["lenguage"]

        self.token = Token(self)
        self.customer = Customers(self)
        self.plan = Plan(self)
        self.subscriptions = Subscriptions(self)
        self.bank = Bank(self)
        self.cash = Cash(self)
        self.charge=Charge(self)
        self.safetypay=Safetypay(self)

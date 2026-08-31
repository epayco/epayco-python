import epaycosdk.resources
from epaycosdk.resources import Token
from epaycosdk.resources import Customers
from epaycosdk.resources import Plan
from epaycosdk.resources import Subscriptions
from epaycosdk.resources import Bank
from epaycosdk.resources import Cash
from epaycosdk.resources import Charge
from epaycosdk.resources import Safetypay
from epaycosdk.resources import Daviplata
from epaycosdk.gateways.legacy import LegacyGateway
from epaycosdk.gateways.ms_transaction import MsTransactionGateway

class Epayco:

    public_key = ""
    api_key = ""
    test = ""
    lang = "ES"

    def __init__(self, options):
        self.api_key = options["apiKey"]
        self.private_key = options["privateKey"]
        self.test = True if options["test"] else False
        self.lang = options["lenguage"]

        # Opcional. Vive junto a las credenciales del comercio porque es una
        # decisión POR COMERCIO, no un ajuste global del proceso. Ausente o
        # [] => 100% flujo legado, idéntico al SDK de hoy. Lista de medios
        # de pago ("pse", "cash", "daviplata", "safetypay") que este
        # comercio ya tiene migrados a ms-transaction.
        self.ms_transaction_methods = set(options.get("msTransactionMethods", []))
        self._legacy_gateway = LegacyGateway(self)
        self._ms_transaction_gateway = MsTransactionGateway(self)

        self.token = Token(self)
        self.customer = Customers(self)
        self.plan = Plan(self)
        self.subscriptions = Subscriptions(self)
        self.bank = Bank(self)
        self.cash = Cash(self)
        self.charge = Charge(self)
        self.safetypay = Safetypay(self)
        self.daviplata = Daviplata(self)

    def gateway_for(self, payment_method):
        """Strategy: qué gateway atiende este medio de pago para ESTE comercio."""
        if payment_method in self.ms_transaction_methods:
            return self._ms_transaction_gateway
        return self._legacy_gateway

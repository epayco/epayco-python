import epayco
import unittest

class EpaycoTest(unittest.TestCase):

    def __init__(self):

        self.apiKey = "491d6a0b6e992cf924edd8d3d088aff1"
        self.privateKey = "268c8e0162990cf2ce97fa7ade2eff5a"
        self.lenguage = "ES";
        self.test = True;
        self.options = {"apiKey": self.apiKey, "privateKey": self.privateKey, "test": self.test, "lenguage": self.lenguage}
        self.switch = False
        self.epayco=epayco.Epayco(self.options)

    def test_createplan(self):

        dataplan = {
            "id_plan": "plangold",
            "name": "Plan Gold",
            "description": "Plan gold gym",
            "amount": 80000,
            "currency": "cop",
            "interval": "month",
            "interval_count": 1,
            "trial_days": 30,
            "public_key": self.apiKey
        }

        plan=self.epayco.plan.create(dataplan)

        self.assertTrue(len(plan['data']['id'])>0)

    if __name__ == "__main__":
        unittest.main()
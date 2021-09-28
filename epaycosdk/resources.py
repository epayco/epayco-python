from epaycosdk.client import Client
import epaycosdk.errors as errors

class Resource(Client):
    """
     * Instance epayco class
     * @param array $epayco
     */
    """

    def __init__(self, epayco):
        self.epayco = epayco


"""
 * Constructor resource requests
"""


class Token(Resource):
    """
     * Instance epayco class
     * @param array $epayco
     */
    """

    def create(self, options):

        return self.request(
            "POST",
            "v1/tokens",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )


"""
 * Customer methods
"""


class Customers(Resource):
    """
     * Create client and asocciate credit card
     * @param  array $options client and token id info
     * @return object
    """

    def create(self, options=None):
        return self.request(
            "POST",
            "payment/v1/customer/create",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Get client for id
     * @param  String $uid id client
     * @return object
    """

    def get(self, uid):
        return self.request(
            "GET",
            "payment/v1/customer/" + self.epayco.api_key + "/" + uid + "/",
            self.epayco.api_key,
            None,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Get list customer rom client epayco
     * @return object
    """

    def getlist(self):
        return self.request(
            "GET",
            "payment/v1/customers/" + self.epayco.api_key + "/",
            self.epayco.api_key,
            None,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    def update(self,uid,options):

        return self.request(
            "POST",
            "payment/v1/customer/edit/" + self.epayco.api_key + "/" + uid + "/",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )
        
    def delete(self,options):

        return self.request(
            "POST",
            "/v1/remove/token",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    def addDefaultCard(self,options):
        return self.request(
            "POST",
            "/payment/v1/customer/reasign/card/default",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False,
            False,
            True
        )

    def addNewToken(self,options):
        return self.request(
            "POST",
            "/v1/customer/add/token",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False,
            False,
            True
        )
        

"""
 * Class Charge
"""

class Charge(Resource):
    """
         * Create charge token card and customer
         * @param  object $options data from charge
         * @return object
        """

    def create(self, options=None):
        return self.request(
            "POST",
            "payment/v1/charge/create",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    def get(self, uid):

        return self.request(
            "GET",
            "restpagos/transaction/response.json",
            self.epayco.api_key,
            {'ref_payco': uid},
            self.epayco.private_key,
            self.epayco.test,
            True,
            self.epayco.lang,
            False
        )
"""
 * Plan methods
"""


class Plan(Resource):
    """
     * Create plan
     * @param  object $options data from plan
     * @return object
    """

    def create(self, options=None):
        return self.request(
            "POST",
            "recurring/v1/plan/create",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Get plan for id
     * @param  String $uid id plan
     * @return object
    """

    def get(self, uid):
        options = None
        return self.request(
            "GET",
            "recurring/v1/plan/" + self.epayco.api_key + "/"+uid,
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Get list all plan from client epayco
     * @return object
    """

    def getlist(self):
        options = None

        return self.request(
            "GET",
            "recurring/v1/plans/" + self.epayco.api_key,
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Update plan
     * @param String uid id plan
     * @param object options content update
     * @return object
    """

    def update(self, uid, options=None):
        return self.request(
            "POST",
            "recurring/v1/plan/edit/" + self.epayco.api_key + "/" + uid + "/",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    def delete(self,uid):
        options={}
        return self.request(
            "POST",
            "recurring/v1/plan/remove/" + self.epayco.api_key + "/" + uid,
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

"""
 * Create subcription from clients
"""


class Subscriptions(Resource):
    """
     * Create Subscription
     * @param  object $options data from plan
     * @return object
    """

    def create(self, options=None):
        return self.request(
            "POST",
            "recurring/v1/subscription/create",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Get plan subscription id
     * @param  String $uid id subscription
     * @return object
    """

    def get(self, uid):
        options = None
        return self.request(
            "GET",
            "recurring/v1/subscription/" + uid + "/" + self.epayco.api_key,
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Get list all suscriptions from client epayco
     * @return object
    """

    def getlist(self):
        options = None

        return self.request(
            "GET",
            "recurring/v1/subscriptions/" + self.epayco.api_key + "/",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    """
     * Update plan
     * @param String uid id plan
     * @param object options content update
     * @return object
    """

    def cancel(self, uid=None):
        options = {'id': uid}

        return self.request(
            "POST",
            "recurring/v1/subscription/cancel",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

    def charge(self, options=None):

        return self.request(
            "POST",
            "payment/v1/charge/subscription/create",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang,
            False
        )

"""
 * Pse methods
"""


class Bank(Resource):
    """
     * Return list all banks
     * @return object
    """

    def pseBank(self,options = None):
        return self.request(
            "GET",
            "restpagos/pse/bancos.json",
            self.epayco.api_key,
            {'public_key':self.epayco.api_key},
            self.epayco.private_key,
            self.epayco.test,
            True,
            self.epayco.lang,
            False
        )

    """
     * Create transaction in ACH
     * @param  Object $options data transaction
     * @return object
    """

    def create(self, options=None):
        return self.request(
            "POST",
            "restpagos/pagos/debitos.json",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            True,
            self.epayco.lang,
            False
        )

    """
     * Return data transaction
     * @param  String $uid cust id transaction
     * @return object
    """

    def pseTransaction(self, uid):
        return self.request(
            "GET",
            "restpagos/pse/transactioninfomation.json",
            self.epayco.api_key,
            {'transactionID':uid},
            self.epayco.private_key,
            self.epayco.test,
            True,
            self.epayco.lang,
            False
        )

    def get(self, uid):

        return self.request(
            "GET",
            "restpagos/transaction/response.json",
            self.epayco.api_key,
            {'ref_payco': uid},
            self.epayco.private_key,
            self.epayco.test,
            True,
            self.epayco.lang,
            False
        )
"""
 * Cash payment methods
"""


class Cash(Resource):
    """
    * Return data payment cash
    * @param  String $type method payment
    * @param  String $options data transaction
    * @return object
    """

    def create(self, type=None, options=None):

        url = None
        if (type == "efecty"):
            url = "restpagos/v2/efectivo/efecty"
        elif (type == "baloto"):
            url = "restpagos/v2/efectivo/baloto"
        elif (type == "gana"):
            url = "restpagos/v2/efectivo/gana"
        elif (type == "redservi"):
            url = "restpagos/v2/efectivo/redservi"
        elif (type == "puntored"):
            url = "restpagos/v2/efectivo/puntored"
        elif (type == "sured"):
            url = "restpagos/v2/efectivo/sured"
        else:
            raise errors.ErrorException(self.epayco.lang, 109)

        return self.request(
            "POST",
            url,
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            True,
            self.epayco.lang,
            True,
            False
        )

    def get(self, uid):

        return self.request(
            "GET",
            "restpagos/transaction/response.json",
            self.epayco.api_key,
            {'ref_payco': uid},
            self.epayco.private_key,
            self.epayco.test,
            True,
            self.epayco.lang,
            False
        )

from pyepayco.client import Client
import pyepayco.errors as errors

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
            self.epayco.lang
        )

    """
     * Get client for id
     * @param  String $uid id client
     * @return object
    """

    def get(self, uid):
        return self.request(
            "GET",
            "payment/v1/customer/" + uid + "/",
            self.epayco.api_key,
            None,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
        )

    """
     * Get list all plan from client epayco
     * @return object
    """

    def getlist(self):
        options = None

        return self.request(
            "GET",
            "recurring/v1/plans/" + self.epayco.api_key + "/",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang
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
            self.epayco.lang
        )

    def delete(self,uid):
        options={}
        return self.request(
            "POST",
            "recurring/v1/plan/remove/" + self.epayco.api_key + "/" + uid + "/",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
        )

    """
     * Update plan
     * @param String uid id plan
     * @param object options content update
     * @return object
    """

    def cancel(self, uid=None):
        options = {uid: uid}

        return self.request(
            "POST",
            "recurring/v1/subscription/cancel",
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test,
            False,
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            self.epayco.lang
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
            url = "restpagos/pagos/efecties.json"
        elif (type == "baloto"):
            url = "restpagos/pagos/balotos.json"
        elif (type == "gana"):
            url = "restpagos/pagos/ganas.json"
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
            self.epayco.lang
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
            self.epayco.lang
        )

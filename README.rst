*****
Epayco
*****

Python wrapper for Epayco API

Description
########

API to interact with Epayco
https://epayco.co/docs/api/

Installation
****

If you want clone the repository, point it directly into our GitHub project::

    $ git clone https://github.com/epayco/epayco-python.git

Run the file setup.py

    $ sudo python3 setup.py install

Usage
####

.. code-block:: python

    import pyepayco.epayco as epayco

    options={
      "apiKey": "491d6a0b6e992cf924edd8d3d088aff1",
      "privateKey": "268c8e0162990cf2ce97fa7ade2eff5a",
      "test": True,
      "lenguage": "ES"
    }

    objepayco = epayco.Epayco(options)

Create Token
####

.. code-block:: python

    credit_info = {
      "card[number]": "4575623182290326",
      "card[exp_year]": "2019",
      "card[exp_month]": "07",
      "card[cvc]": "123"
    }

    token = objepayco.token.create(credit_info)

Customers
####

Create
******
.. code-block:: python

    customer_info = {
      "token_card": "eXj5Wdqgj7xzvC7AR",
      "name": "Joe Doe",
      "email": "joe@payco.co",
      "phone": "3005234321",
      "default": true
    }

    customer = objepayco.customer.create(customer_info)

Retrieve
******
.. code-block:: python

    customer = objepayco.customer.get("eXj5Wdqgj7xzvC7AR")

List
******
.. code-block:: python

    customers = objepayco.customer.getlist()

Update
******
.. code-block:: python

    customer = test.customer.update(
        "eXj5Wdqgj7xzvC7AR", {"name": "Alex"}
    )

Plans
####

Create
******

.. code-block:: python

    plan_info = {
      "id_plan": "coursereact",
      "name": "Course react js",
      "description": "Course react and redux",
      "amount": 30000,
      "currency": "cop",
      "interval": "month",
      "interval_count": 1,
      "trial_days": 30
    }

    plan = objepayco.plan.create(plan_info)


Retrieve
******
.. code-block:: python

    plan = objepayco.plan.get("coursereact")

List
******
.. code-block:: python

    planes = objepayco.plan.getlist()

Remove
******
.. code-block:: python

    plan = objepayco.plan.delete("coursereact")

Subscriptions
####

Create
******
.. code-block:: python

    subscription_info = {
        "id_plan": "coursereact2",
        "customer": "9xRxhaJ2YmLTkT5uz",
        "token_card": "eXj5Wdqgj7xzvC7AR",
        "doc_type": "CC",
        "doc_number": "5234567"
    }

    sub = objepayco.subscriptions.create(subscription_info)

Retrieve
******
.. code-block:: python

    subscription = objepayco.subscriptions.get("efPXtZ5r4nZRoPtjZ")

List
******
.. code-block:: python

    subscriptions = objepayco.subscriptions.getlist()

Cancel
******
.. code-block:: python

    subscription = objepayco.subscriptions.cancel("fayE66HxYbxWydaN8")

Pay Subscription
******
.. code-block:: python

    sub = objepayco.subscriptions.charge({
      "id_plan": "coursereact",
      "customer": "A6ZGiJ6rgxK5RB2WT",
      "token_card": "eXj5Wdqgj7xzvC7AR",
      "doc_type": "CC",
      "doc_number": "1000000"

    })

PSE
####

Create
*****
.. code-block:: python

    pse_info = {
      "bank": "1007",
      "invoice": "1472050778",
      "description": "pay test",
      "value": "10000",
      "tax": "0",
      "tax_base": "0",
      "currency": "COP",
      "type_person": "0",
      "doc_type": "CC",
      "doc_number": "10000000",
      "name": "testing",
      "last_name": "PAYCO",
      "email": "no-responder@payco.co",
      "country": "CO",
      "cell_phone": "3010000001",
      "ip": "186.116.10.133",
      "url_response": "https://tudominio.com/respuesta.php",
      "url_confirmation": "https://tudominio.com/confirmacion.php",
      "method_confirmation": "GET",
    }

    pse = objepayco.bank.create(pse_info)

Retrieve
*****
.. code-block:: python

    pse = objepayco.bank.pseTransaction("transactionID")

Split Payments
*****

Previous requirements: https://docs.epayco.co/tools/split-payment
*****

.. code-block:: python

    pse_info = {
    #Other customary parameters...
      "splitpayment":"true",
       "split_app_id":"P_CUST_ID_CLIENTE APPLICATION",
       "split_merchant_id":"P_CUST_ID_CLIENTE COMMERCE",
       "split_type" : "02",
       "split_primary_receiver" : "P_CUST_ID_CLIENTE APPLICATION",
       "split_primary_receiver_fee":"10"
     }

    pse_split = objepayco.bank.create(pse_info)

Cash
####

Create
*****
.. code-block:: python

    cash_info = {
        "invoice": "1472050778",
        "description": "pay test",
        "value": "20000",
        "tax": "0",
        "tax_base": "0",
        "currency": "COP",
        "type_person": "0",
        "doc_type": "CC",
        "doc_number": "100000",
        "name": "testing",
        "last_name": "PAYCO",
        "email": "test@mailinator.com",
        "cell_phone": "3010000001",
        "end_date": "2019-12-05",
        "ip": "186.116.10.133",
        "url_response": "https://tudominio.com/respuesta.php",
        "url_confirmation": "https://tudominio.com/confirmacion.php",
        "method_confirmation": "GET",

    }

    cash = objepayco.cash.create('efecty',cash_info)
    cash = objepayco.cash.create('baloto',cash_info)
    cash = objepayco.cash.create('gana',cash_info)

Retrieve
*****
.. code-block:: python

    cash = epayco.cash.get("ref_payco")



Split Payments
*****

Previous requirements: https://docs.epayco.co/tools/split-payment
*****

.. code-block:: python

    cash_info = {
    #Other customary parameters...
      "splitpayment":"true",
       "split_app_id":"P_CUST_ID_CLIENTE APPLICATION",
       "split_merchant_id":"P_CUST_ID_CLIENTE COMMERCE",
       "split_type" : "02",
       "split_primary_receiver" : "P_CUST_ID_CLIENTE APPLICATION",
       "split_primary_receiver_fee":"10"
     }
  
    cash_info_split = objepayco.cash.create('efecty',cash_info)

Payment
*****

Create
*****
.. code-block:: python

    payment_info = {
      "token_card": "eXj5Wdqgj7xzvC7AR",
      "customer_id": "A6ZGiJ6rgxK5RB2WT",
      "doc_type": "CC",
      "doc_number": "1000000",
      "name": "John",
      "last_name": "Doe",
      "email": "example@email.com",
      "ip": "192.198.2.114",
      "bill": "OR-1234",
      "description": "Test Payment",
      "value": "119000",
      "tax": "19000",
      "tax_base": "100000",
      "currency": "COP",
      "dues": "12"
    }

    pay = objepayco.charge.create(payment_info)

Retrieve
*****

.. code-block:: python

    pay = epayco.charge.get("ref_payco")

Split Payments
*****

Previous requirements https://docs.epayco.co/tools/split-payment
*****

.. code-block:: python

    payment_info = {
    #Other customary parameters...
      "splitpayment":"true",
       "split_app_id":"P_CUST_ID_CLIENTE APPLICATION",
       "split_merchant_id":"P_CUST_ID_CLIENTE COMMERCE",
       "split_type" : "02",
       "split_primary_receiver" : "P_CUST_ID_CLIENTE APPLICATION",
       "split_primary_receiver_fee":"10"
     }

    pay_split = objepayco.charge.create(payment_info)


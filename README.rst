*****
Epayco
*****

Python wrapper for Epayco API

Description
########

API to interact with Epayco
https://api.epayco.co

Installation
****
Installation
============

If you want to clone the repository, point it directly into our GitHub project:

.. code-block:: bash

    $ git clone https://github.com/epayco/epayco-python.git

Install from Packages (Linux), Python = 3.7
-------------------------------------------

Run the file `setup.py`:

.. code-block:: bash

    $ sudo python3 setup.py install

Install the ePayco module:

.. code-block:: bash

    $ pip install epaycosdk

Install from Packages (Windows), Python = 3.7
---------------------------------------------

Run the file `setup.py`:

.. code-block:: bash

    $ pip install setuptools
    $ python setup.py install

Install the ePayco module:

.. code-block:: bash

    $ pip install epaycosdk


Usage
####

.. code-block:: python

    import epaycosdk.epayco as epayco

    apiKey = "PUBLIC_KEY"
    privateKey = "PRIVATE_KEY"
    lenguage = "ES"
    test = True
    options={"apiKey":apiKey,"privateKey":privateKey,"test":test,"lenguage":lenguage}

    objepayco=epayco.Epayco(options)

Create Token
####

.. code-block:: python

    credit_info = {
      "card[number]": "4575623182290326",
      "card[exp_year]": "2025",
      "card[exp_month]": "19",
      "card[cvc]": "123",
      "hasCvv": True #// hasCvv: validar codigo de seguridad en la transacción
      }

    token=objepayco.token.create(credit_info)

Customers
####

Create
******
.. code-block:: python

    customer_info = {
      "token_card": "eXj5Wdqgj7xzvC7AR",
      "name": "Joe",
      "last_name": "Doe", #This parameter is optional
      "email": "joe@payco.co",
      "phone": "3005234321",
      "default": True
      }

    customer=objepayco.customer.create(customer_info)

Retrieve
******
.. code-block:: python

    customer=objepayco.customer.get("id_client")

List
******
.. code-block:: python

    customers = objepayco.customer.getlist()

Update
******
.. code-block:: python

    update_customer_info = {
      "customerId": "id_client",
      "name": "Alex"
    }

    customer =objepayco.customer.update(update_customer_info)

Delete Token
******
.. code-block:: python

    delete_customer_info = {
      "franchise": "visa",
      "mask": "457562******0326",
      "customer_id":"id_client"
    }

    customer =objepayco.customer.delete(delete_customer_info)



Add new token default to card existed
******
.. code-block:: python

    customer_info = {
        "customer_id":"id_client",
        "token": "**********Q2ZLD9",
        "franchise":"visa",
        "mask":"457562******0326"
    }
    customer=objepayco.customer.addDefaultCard(customer_info)


Add new token to customer existed
******
.. code-block:: python

    customer_info = {
        "token_card": "6tWRMjsiDGPds2Krb",
        "customer_id":"id_client"
    }
    customer=objepayco.customer.addNewToken(customer_info)




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
        "doc_number": "0000000000",
        #Optional parameter: if these parameter it's not send, system get ePayco dashboard's url_confirmation
        "url_confirmation": "https://tudominio.com/confirmacion.php",
        "method_confirmation": "POST"
    }

    sub=objepayco.subscriptions.create(subscription_info)

Retrieve
******
.. code-block:: python

    sub=objepayco.subscriptions.get("efPXtZ5r4nZRoPtjZ")

List
******
.. code-block:: python

    sub=objepayco.subscriptions.getlist()

Cancel
******
.. code-block:: python

    sub=objepayco.subscriptions.cancel("fayE66HxYbxWydaN8")

Pay Subscription
******
.. code-block:: python

    subscription_info = {
      "id_plan": "coursereact",
      "customer": "A6ZGiJ6rgxK5RB2WT",
      "token_card": "eXj5Wdqgj7xzvC7AR",
      "doc_type": "CC",
      "doc_number": "1000000",
      "ip":"190.000.000.000"  #This is the client's IP, it is required

    }

    sub = objepayco.subscriptions.charge(subscription_info)

PSE
####

List Banks
*****
.. code-block:: python

    banks = objepayco.bank.pseBank()

Create
*****
.. code-block:: python

    pse_info = {
        "bank": "1007",
        "invoice": "147205",
        "description": "pay test",
        "value": "116000",
        "tax": float("16000"),
        "tax_base": float("100000"),
        "currency": "COP",
        "type_person": "0",
        "doc_type": "CC",
        "docNumber": "10000000",
        "name": "testing",
        "last_name": "PAYCO",
        "email": "no-responder@payco.co",
        "country": "CO",
        "cellPhone": "3010000001",
        "ip": "190.000.000.000",  # This is the client's IP, it is required,
        "url_response": "https://tudominio.com/respuesta.php",
        "url_confirmation": "https://tudominio.com/confirmacion.php",
        "metodoconfirmacion": "GET",
        # Los parámetros extras deben ser enviados tipo string, si se envía tipo array generara error.
        "extra1": "",
        "extra2": "",
        "extra3": "",
        "extra4": "",
        "extra5": "",
        "extra6": "",
        "extra7": ""
    }

    pse = objepayco.bank.create(pse_info)

Retrieve
*****
.. code-block:: python

    pse = objepayco.bank.pseTransaction("ticketId")

Split Payments
*****

Previous requirements: https://docs.epayco.co/tools/split-payment
*****


Split payment
*****

.. code-block:: python

    import json

    pse_info = {
    #Other customary parameters...
      "splitpayment":"true",
       "split_app_id":"P_CUST_ID_CLIENTE APPLICATION",
       "split_merchant_id":"P_CUST_ID_CLIENTE COMMERCE",
       "split_type" : "01",
       "split_primary_receiver" : "P_CUST_ID_CLIENTE APPLICATION",
       "split_primary_receiver_fee":"80000"
       "split_receivers": json.dumps([
                {"id":"P_CUST_ID_CLIENTE 1 RECEIVER","total":"58000","iva":"8000","base_iva":"50000","fee":"10"},
                {"id":"P_CUST_ID_CLIENTE 2 RECEIVER","total":"58000","iva":"8000","base_iva":"50000", "fee":"10"}
        ])
     }

    pse_split = objepayco.bank.create(pse_info)
    

Cash
####

Create
*****
.. code-block:: python

        # paymentMethod: EF=> efecty, GA=>gana, PR=>puntored, RS=>redservi, SR=>sured
        cash_info = {
        "paymentMethod" :"EF",
        "invoice": "1472050778",
        "description": "pay test",
        "value": "116000",
        "tax": "16000",
        "tax_base": "100000",
        "currency": "COP",
        "type_person": "0",
        "doc_type": "CC",
        "docNumber": "100000",
        "name": "testing",
        "last_name": "PAYCO",
        "email": "test@mailinator.com",
        "cellPhone": "3010000001",
        "end_date": "2025-02-05",
        "ip": "190.000.000.000",  # This is the client's IP, it is required,
        "url_response": "https://tudominio.com/respuesta.php",
        "url_confirmation": "https://tudominio.com/confirmacion.php",
        "metodoconfirmacion": "GET",
        # Los parámetros extras deben ser enviados tipo string, si se envía tipo array generara error.
        "extra1": "",
        "extra2": "",
        "extra3": "",
        "extra4": "",
        "extra5": "",
        "extra6": "",
        "extra7": ""
    }

    cash = objepayco.cash.create(cash_info)

Retrieve
*****
.. code-block:: python

    cash = epayco.cash.get("ref_payco")



Split Payments
*****

Previous requirements: https://docs.epayco.co/tools/split-payment



Split payment:
****

use the following attributes in case you need to do a dispersion with one or multiple providers

.. code-block:: python

    import json 

    payment_info = {
    #Other customary parameters...
        "splitpayment":"true",
        "split_app_id":"P_CUST_ID_CLIENTE APPLICATION",
        "split_merchant_id":"P_CUST_ID_CLIENTE COMMERCE",
        "split_type" : "02",
        "split_primary_receiver" : "P_CUST_ID_CLIENTE APPLICATION",
        "split_primary_receiver_fee":"0",
        "split_rule":'multiple', #si se envía este parámetro el campo split_receivers se vuelve obligatorio
        "split_receivers":json.dumps([
                {"id":"P_CUST_ID_CLIENTE 1 RECEIVER","total":"58000","iva":"8000","base_iva":"50000","fee":"10"},
                {"id":"P_CUST_ID_CLIENTE 2 RECEIVER","total":"58000","iva":"8000","base_iva":"50000", "fee":"10"}
        ]) #campo obligatorio sí se envía split_rule
        }

     cash_info_split = objepayco.cash.create('efecty',cash_info)





Payment
####

Create
*****
.. code-block:: python

    payment_info = {
      "token_card": "token_card",
      "customer_id": "customer_id",
      "doc_type": "CC",
      "doc_number": "1000000",
      "name": "John",
      "last_name": "Doe",
      "email": "example@email.com",
      "bill": "OR-1234",
      "description": "Test Payment",
      "country": "CO",
      "city": "bogota",
      "value": "116000",
      "tax": "16000",
      "tax_base": "100000",
      "currency": "COP",
      "dues": "12",
      "ip":"190.000.000.000",  #This is the client's IP, it is required
      "url_response": "https://tudominio.com/respuesta.php",
      "url_confirmation": "https://tudominio.com/confirmacion.php",
      "method_confirmation": "GET",
      "use_default_card_customer":True, # if the user wants to be charged with the card that the customer currently has as default = true
      #Los parámetros extras deben ser enviados tipo string, si se envía tipo array generara error.
      "extra1": "",
      "extra2": "",
      "extra3": "",
      "extra4": "",
      "extra5": "",  
      "extra6": "",
      "extra7": ""
    }

    pay = objepayco.charge.create(payment_info)

Retrieve
*****

.. code-block:: python

    pay = epayco.charge.get("ref_payco")


Split Payments
*****

Previous requirements https://docs.epayco.co/tools/split-payment


Split payment
****

use the following attributes in case you need to do a dispersion with one or multiple providers

.. code-block:: python

    import json
    
    payment_info = {
    #Other customary parameters...
        "splitpayment":"true",
        "split_app_id":"P_CUST_ID_CLIENTE APPLICATION",
        "split_merchant_id":"P_CUST_ID_CLIENTE COMMERCE",
        "split_type" : "02",
        "split_primary_receiver" : "P_CUST_ID_CLIENTE APPLICATION",
        "split_primary_receiver_fee":"0",
        "split_rule":'multiple', #si se envía este parámetro el campo split_receivers se vuelve obligatorio
        "split_receivers":[
                {"id":"P_CUST_ID_CLIENTE 1 RECEIVER","total":"58000","iva":"8000","base_iva":"50000","fee":"10"},
                {"id":"P_CUST_ID_CLIENTE 2 RECEIVER","total":"58000","iva":"8000","base_iva":"50000", "fee":"10"}
        ] #campo obligatorio sí se envía split_rule
        }

    pay_split = objepayco.charge.create(payment_info)


Daviplata
####

Create
*****

.. code-block:: python

    payment_info = {
        "doc_type": "CC",
        "document": "1053814580414720",
        "name": "Testing",
        "last_name": "PAYCO",
        "email": "exmaple@epayco.co",
        "ind_country": "57",
        "phone": "314853222200033",
        "country": "CO",
        "city": "bogota",
        "address": "Calle de prueba",
        "ip": "189.176.0.1",
        "currency": "COP",
        "description": "ejemplo de transaccion con daviplata",
        "value": "100",
        "tax": "0",
        "ico": "0"
        "tax_base": "0",
        "method_confirmation": "GET",
        "url_response": "https://tudominio.com/respuesta.php",
        "url_confirmation": "https://tudominio.com/confirmacion.php",
        "extra1": "",      
        "extra2": "",
        "extra3": "",
        "extra4": "",
        "extra5": "",  
        "extra6": "",
        "extra7": "",
        "extra8": "",
        "extra9": "",
        "extra10": ""
    }

    daviplata = objepayco.daviplata.create(payment_info)

confirm transaccion
*****

.. code-block:: python

    confirm = {
        "ref_payco": "45508846", # It is obtained from the create response
        "id_session_token": "45081749", # It is obtained from the create response
        "otp": "2580"
    }
   
    daviplata = objepayco.daviplata.confirm(payment_info)

Safetypay
####

Create
*****

.. code-block:: python

    payment_info = {
        "cash": "1",
        "end_date": "2021-08-05",
        "doc_type": "CC",
        "document"": "123456789",
        "name": "Jhon",
        "last_name": "doe",
        "email": "jhon.doe@yopmail.com",
        "ind_country": "57",
        "phone": "3003003434",
        "country": "CO",
        "invoice": "fac-01", # opcional
        "city": "N/A",
        "address": "N/A",
        "ip": "192.168.100.100",
        "currency": "COP",
        "description": "Thu Jun 17 2021 11:37:01 GMT-0400 (hora de Venezuela)",
        "value": 100000,
        "tax": 0,
        "ico": 0,
        "tax_base": 0,
        "url_confirmation": "https://tudominio.com/respuesta.php",
        "url_response": "https://tudominio.com/respuesta.php",
        "method_confirmation": "POST",
        "extra1": "",      
        "extra2": "",
        "extra3": "",
        "extra4": "",
        "extra5": "",  
        "extra6": "",
        "extra7": "",
        "extra8": "",
        "extra9": "",
        "extra10": ""
    }

    safetypay = objepayco.safetypay.create(payment_info)

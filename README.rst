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

    $ git clone https://github.com/Mango/mango-python.git

Run the file setup.py

    $ sudo python3 setup.py install

Usage
####


    import pyepayco.epayco as epayco

    apiKey = "491d6a0b6e992cf924edd8d3d088aff1"

    privateKey = "268c8e0162990cf2ce97fa7ade2eff5a"

    lenguage = "ES"

    test = True

    options={"apiKey":apiKey,"privateKey":privateKey,"test":test,"lenguage":lenguage}

    objepayco=epayco.Epayco(options)

Create Token
####

credit_info = {
  "card[number]": "4575623182290326",
  "card[exp_year]": "2017",
  "card[exp_month]": "07",
  "card[cvc]": "123"
  }

token=objepayco.token.create(credit_info)

Customers
####

Create
******
customer_info = {
  "token_card": "eXj5Wdqgj7xzvC7AR",
  "name": "Joe Doe",
  "email": "joe@payco.co",
  "phone": "3005234321",
  "default": true
}

customer=objepayco.customer.create(customer_info)

Retrieve
******

customer=objepayco.customer.get("eXj5Wdqgj7xzvC7AR")

List
******

customers = testepayco.customer.getlist()

Update
******

update_customer_info = {
  "name": "Alex"
}

customer =test.customer.update("eXj5Wdqgj7xzvC7AR",update_customer_info)

Plans
####

Create
******

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
plan = objepayco.plan.get("coursereact")

List
******
planes = objepayco.plan.getlist()

Remove
******

plan = objepayco.plan.delete("coursereact")

Subscriptions
####

Create
******
subscription_info = {
    "id_plan": "coursereact2",
    "customer": "9xRxhaJ2YmLTkT5uz",
    "token_card": "eXj5Wdqgj7xzvC7AR",
    "doc_type": "CC",
    "doc_number": "5234567"
}

sub=objepayco.subscriptions.create(subscription_info)

Retrieve
******
sub=objepayco.subscriptions.get("efPXtZ5r4nZRoPtjZ")

List
******

sub=objepayco.subscriptions.getlist()

Cancel
******
sub=objepayco.subscriptions.cancel("fayE66HxYbxWydaN8")

Pay Subscription
******

subscription_info = {
  "id_plan": "coursereact",
  "customer": "A6ZGiJ6rgxK5RB2WT",
  "token_card": "eXj5Wdqgj7xzvC7AR",
  "doc_type": "CC",
  "doc_number": "1035851980"
}

sub = objepayco.subscriptions.charge(subscription_info)

PSE
####

Create
*****


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
  "doc_number": "10358519",
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

pse = objepayco.bank.pseTransaction("transactionID")

Cash
####

Create
*****

cash_info = {
    "invoice": "1472050778",
    "description": "pay test",
    "value": "20000",
    "tax": "0",
    "tax_base": "0",
    "currency": "COP",
    "type_person": "0",
    "doc_type": "CC",
    "doc_number": "10358519",
    "name": "testing",
    "last_name": "PAYCO",
    "email": "test@mailinator.com",
    "cell_phone": "3010000001",
    "end_date": "2017-12-05",
    "ip": "186.116.10.133",
    "url_response": "https://tudominio.com/respuesta.php",
    "url_confirmation": "https://tudominio.com/confirmacion.php",
    "method_confirmation": "GET",
}

cash = objepayco.cash.create('efecty',cash_info)

#cash = objepayco.cash.create('baloto',cash_info)

#cash = objepayco.cash.create('gana',cash_info)

Retrieve
*****

cash = epayco.cash.get("ref_payco")

Payment
####

Create
*****

payment_info = {
  "token_card": "eXj5Wdqgj7xzvC7AR",
  "customer_id": "A6ZGiJ6rgxK5RB2WT",
  "doc_type": "CC",
  "doc_number": "1035851980",
  "name": "John",
  "last_name": "Doe",
  "email": "example@email.com",
  "ip": "192.198.2.114",
  "bill": "OR-1234",
  "description": "Test Payment",
  "value": "116000",
  "tax": "16000",
  "tax_base": "100000",
  "currency": "COP",
  "dues": "12"
}

pay = objepayco.charge.create(payment_info)

Retrieve
*******

pay = epayco.charge.get("ref_payco")
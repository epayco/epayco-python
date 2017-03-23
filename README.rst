Epayco
=====

Python wrapper for Epayco API

## Description

API to interact with Epayco
https://epayco.co/docs/api/

## Installation

You can get the library from ``PyPI`` using ``pip``::

$ pip install pyepayco

If you want clone the repository, point it directly into our GitHub project::

    $ git clone https://github.com/Mango/mango-python.git

## Usage

import pyepayco.epayco as epayco

apiKey = "491d6a0b6e992cf924edd8d3d088aff1"
privateKey = "268c8e0162990cf2ce97fa7ade2eff5a"
lenguage = "ES";
test = True;
options={"apiKey":apiKey,"privateKey":privateKey,"test":test,"lenguage":lenguage}

test=epayco.Epayco(options);


### Create Token

```python
credit_info = {
  "card[number]": "4575623182290326",
  "card[exp_year]": "2017",
  "card[exp_month]": "07",
  "card[cvc]": "123"
}

response=test.token.create(credit_info)

```

### Customers

#### Create

```ruby
customer_info = {
  token_card: "eXj5Wdqgj7xzvC7AR",
  name: "Joe Doe",
  email: "joe@payco.co",
  phone: "3005234321",
  default: true
}

begin
  customer = Epayco::Customers.create customer_info
rescue Epayco::Error => e
  puts e
end
```

#### Retrieve

```ruby
begin
  customer = Epayco::Customers.get "id_customer"
rescue Epayco::Error => e
  puts e
end
```

#### List

```ruby
begin
  customer = Epayco::Customers.list
rescue Epayco::Error => e
  puts e
end
```

#### Update

```ruby
update_customer_info = {
  name: "Alex"
}

begin
  customer = Epayco::Customers.update "id_customer", update_customer_info
rescue Epayco::Error => e
  puts e
end
```

### Plans

#### Create

```ruby
plan_info = {
  id_plan: "coursereact",
  name: "Course react js",
  description: "Course react and redux",
  amount: 30000,
  currency: "cop",
  interval: "month",
  interval_count: 1,
  trial_days: 30
}

begin
  plan = Epayco::Plan.create plan_info
rescue Epayco::Error => e
  puts e
end
```

#### Retrieve

```ruby
begin
  plan = Epayco::Plan.get "coursereact"
rescue Epayco::Error => e
  puts e
end
```

#### List

```ruby
begin
  plan = Epayco::Plan.list
rescue Epayco::Error => e
  puts e
end
```

#### Remove

```ruby
begin
  plan = Epayco::Plan.delete "coursereact"
rescue Epayco::Error => e
  puts e
end
```

### Subscriptions

#### Create

```ruby
subscription_info = {
  id_plan: "coursereact",
  customer: "A6ZGiJ6rgxK5RB2WT",
  token_card: "eXj5Wdqgj7xzvC7AR",
  doc_type: "CC",
  doc_number: "5234567"
}

begin
  sub = Epayco::Subscriptions.create subscription_info
  assert(sub)
rescue Epayco::Error => e
  puts e
end
```

#### Retrieve

```ruby
begin
  sub = Epayco::Subscriptions.get "id_subscription"
rescue Epayco::Error => e
  puts e
end
```

#### List

```ruby
begin
  sub = Epayco::Subscriptions.list
rescue Epayco::Error => e
  puts e
end
```

#### Cancel

```ruby
begin
  sub = Epayco::Subscriptions.cancel "id_subscription"
rescue Epayco::Error => e
  puts e
end
```

#### Pay Subscription

```ruby
subscription_info = {
  id_plan: "coursereact",
  customer: "A6ZGiJ6rgxK5RB2WT",
  token_card: "eXj5Wdqgj7xzvC7AR",
  doc_type: "CC",
  doc_number: "5234567"
}

begin
  sub = Epayco::Subscriptions.charge subscription_info
rescue Epayco::Error => e
  puts e
end
```

### PSE

#### Create

```ruby
pse_info = {
  bank: "1007",
  invoice: "1472050778",
  description: "pay test",
  value: "10000",
  tax: "0",
  tax_base: "0",
  currency: "COP",
  type_person: "0",
  doc_type: "CC",
  doc_number: "10358519",
  name: "testing",
  last_name: "PAYCO",
  email: "no-responder@payco.co",
  country: "CO",
  cell_phone: "3010000001",
  ip: "186.116.10.133",
  url_response: "https:/secure.payco.co/restpagos/testRest/endpagopse.php",
  url_confirmation: "https:/secure.payco.co/restpagos/testRest/endpagopse.php",
  method_confirmation: "GET",
}

begin
  pse = Epayco::Bank.create pse_info
rescue Epayco::Error => e
  puts e
end
```

#### Retrieve

```ruby
begin
  pse = Epayco::Bank.get "id_transaction"
rescue Epayco::Error => e
  puts e
end
```

### Cash

#### Create

```ruby
cash_info = {
    invoice: "1472050778",
    description: "pay test",
    value: "20000",
    tax: "0",
    tax_base: "0",
    currency: "COP",
    type_person: "0",
    doc_type: "CC",
    doc_number: "10358519",
    name: "testing",
    last_name: "PAYCO",
    email: "test@mailinator.com",
    cell_phone: "3010000001",
    end_date: "2017-12-05",
    ip: "186.116.10.133",
    url_response: "https:/secure.payco.co/restpagos/testRest/endpagopse.php",
    url_confirmation: "https:/secure.payco.co/restpagos/testRest/endpagopse.php",
    method_confirmation: "GET",
}

begin
  cash = Epayco::Cash.create cash_info, "efecty"
rescue Epayco::Error => e
  puts e
end
```

#### Retrieve

```ruby
begin
  cash = Epayco::Cash.get "id_transaction"
rescue Epayco::Error => e
  puts e
end
```

### Payment

#### Create

```ruby
payment_info = {
  token_card: "eXj5Wdqgj7xzvC7AR",
  customer_id: "A6ZGiJ6rgxK5RB2WT",
  doc_type: "CC",
  doc_number: "1035851980",
  name: "John",
  last_name: "Doe",
  email: "example@email.com",
  ip: "192.198.2.114",
  bill: "OR-1234",
  description: "Test Payment",
  value: "116000",
  tax: "16000",
  tax_base: "100000",
  currency: "COP",
  dues: "12"
}

begin
  pay = Epayco::Charge.create payment_info
rescue Epayco::Error => e
  puts e
end
```

#### Retrieve

```ruby
begin
  pay = Epayco::Charge.get "id_payment"
rescue Epayco::Error => e
  puts e
end
```
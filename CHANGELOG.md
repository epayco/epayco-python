# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [Unreleased]

### Changed
- **Cambio de comportamiento por defecto (SDK-1370):** tarjeta de crédito (TDC) pasa a
  ms-transaction. `Token.create(...)` tokeniza contra el servicio nuevo
  (`payment/subscriptions/v1/tokenization/createToken`), `Charge.create(...)` crea la
  transacción `paymentMethod: TDC` y `Charge.get(ref_payco)` consulta
  `GET payment/api/v1/transactions/{ref}`. Los tres mantienen firma y forma de respuesta del
  legado. Se vuelve al legado con `transactionMethods: ["charge"]` (aplica a los tres a la vez).
- En el flujo nuevo `customer_id`/`use_default_card_customer` no se envían: ms-transaction
  cobra directo contra el token. Los tokens de ambos servicios son intercambiables, así que
  `Customers`/`Subscriptions` (que siguen en legado) aceptan el token nuevo.
- El flujo nuevo exige una IP válida en `ip` (`190.000.000.000` responde error de validación).

### Known differences vs. legacy
- `ind_pais`/`country_card` salen en `None`: ms-transaction no expone el país emisor.
- `Charge.get` en el flujo nuevo no trae `x_cust_id_cliente`, `x_business`, `x_quotas`,
  `x_signature`, `x_customer_phone`/`x_customer_movil`/`x_customer_ind_pais`, y
  `x_customer_doctype`/`x_customer_country` vienen enmascarados por ms-transaction.
- `ciudad` y los `extraN` de primer nivel se respetan en el flujo nuevo; el legado los
  descarta (`Sin Ciudad`, extras vacíos).

## [3.6.0] - 2026-09-01

### Changed
- **Cambio de comportamiento por defecto:** Safetypay y Daviplata ahora usan ms-transaction por
  defecto, sin necesidad de configuración adicional. El flujo legado pasa a ser opt-in con la
  nueva clave `transactionMethods` en `options` (reemplaza a `msTransactionMethods`, que
  funcionaba al revés -- ms-transaction era el opt-in).
- `Safetypay.get(...)` y `Daviplata.get(...)` quedan disponibles por defecto (antes requerían
  activar ms-transaction explícitamente); dejan de funcionar si ese medio de pago se fuerza al
  flujo legado vía `transactionMethods`.

## [3.5.0] - 2026-08-31

### Added
- Migración de Daviplata al backend ms-transaction, activable de forma opcional y por comercio
  con `msTransactionMethods` (mismo mecanismo que Safetypay).
- `Daviplata.get(ref_payco)`: consulta de transacción, disponible solo cuando `daviplata` está en
  `msTransactionMethods` (no existe en el flujo legado).
- `epaycosdk.mappers.daviplata`.

### Changed
- `Daviplata.create(...)` mantiene su firma y forma de respuesta; internamente enruta al flujo
  legado o a ms-transaction según la configuración del comercio.
- `Daviplata.confirm(...)` no cambia: sigue siendo exclusivamente flujo legado.

## [3.4.0] - 2026-08-31

### Added
- Migración de Safetypay al backend ms-transaction, activable de forma opcional y por comercio
  con la clave `msTransactionMethods` en `options` (ausente o vacía = flujo legado, sin cambios).
- `Safetypay.get(ref_payco)`: consulta de transacción, disponible solo cuando `safetypay` está en
  `msTransactionMethods` (no existe en el flujo legado).
- `epaycosdk.gateways`: capa de adaptador (`PaymentGateway`, `LegacyGateway`, `MsTransactionGateway`)
  y `epaycosdk.mappers.safetypay` (traducción de entrada/salida hacia/desde ms-transaction).

### Changed
- `Safetypay.create(...)` mantiene su firma y forma de respuesta; internamente enruta al flujo
  legado o a ms-transaction según la configuración del comercio.

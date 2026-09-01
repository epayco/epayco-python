# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

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

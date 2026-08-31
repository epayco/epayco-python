# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

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

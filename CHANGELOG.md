# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[Versionado Semántico](https://semver.org/lang/es/).

## [Sin publicar]

## [1.0.0]
### Agregado
- Cálculo de la comisión de transferencias (`calcular_comision`).
- Cálculo del total a debitar (`calcular_total`).
- Validación del monto (`validar_monto`).

## [1.0.1] - 2026-10-05
### Corregido
- Defecto 1: Corrección de validación (`calcular_comision`), cambio de operador '<' por '<=' en validación 'monto <= LIMITE_SIN_COMISION'
- Defecto 2: Else agregado en (`calcular_comision`), no se aplicaba tope a la comisión.
- Defecto 3: Cambio de signo '-' por '+' en (`calcular_monto`) al momento de hacer el return.
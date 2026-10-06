"""MINI DUELO - Parte 2 del laboratorio.

Escribe aquí tus pruebas. El docente las ejecutará contra versiones del código
con defectos escondidos ("mutantes") y contará cuántos logran detectar.

REGLAS
  1. Solo puedes importar de `pytest` y de `pagofacil.comision`.
  2. TODAS tus pruebas deben PASAR con el código correcto (el que cumple
     ESPECIFICACION.md). Si una falla con el código correcto, no puntúas.
  3. Diseña desde la especificación (caja negra): particiones y valores límite.
  4. Evita montos cuyo resultado caiga justo en medio centavo (redondeo ambiguo).
  5. Trabaja SOLO en este archivo durante el duelo.
"""
import pytest

from pagofacil.comision import calcular_comision, calcular_total, validar_monto  # noqa: F401


def test_ejemplo_monto_bajo():  # ejemplo que ya pasa; puedes borrarlo o conservarlo
    assert calcular_comision(50) == 0


# --- Tus pruebas empiezan aquí ---


# ---------------------------------------------------------------------------
# 1) Comisión por tramos, fronteras (ambos lados), tope y redondeo
#    Técnicas: partición de equivalencia (PE) + valores límite (VL)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("monto, esperado", [
    # Tramo 1 (<= 100): Q0.00
    (0.01, 0.0),        # VL: mínimo monto válido
    (50, 0.0),          # PE: representativo tramo 1
    (100, 0.0),         # VL: 100 está INCLUIDO en tramo 1
    # Tramo 2 (> 100 y <= 1000): 1.5 %
    (100.01, 1.5),      # VL: primer valor del tramo 2 (1.50015 -> 1.5)
    (200, 3.0),         # PE: ejemplo de la especificación
    (500, 7.5),         # PE: representativo tramo 2
    (123.45, 1.85),     # RN2: 1.85175 -> 1.85 (detecta falta de redondeo / 1 decimal)
    (100.43, 1.51),     # RN2: 1.50645 -> 1.51
    (1000, 15.0),       # VL: 1000 está INCLUIDO en tramo 2 (no 10.0)
    # Tramo 3 (> 1000): 1 %, sin llegar al tope
    (1000.01, 10.0),    # VL: primer valor del tramo 3 (10.0001 -> 10.0)
    (1234.56, 12.35),   # RN2: 12.3456 -> 12.35
    (2000, 20.0),       # PE: representativo tramo 3
    (2490, 24.9),       # VL: justo debajo del tope
    # Tope Q25 (RN1)
    (2500, 25.0),       # VL: 1 % = 25 exacto (frontera del tope)
    (2510, 25.0),       # VL: 25.10 -> tope 25
    (3000, 25.0),       # ejemplo de la especificación (30 -> 25)
    (1000000, 25.0),    # PE: monto muy grande sigue topado
])
def test_comision_por_tramos(monto, esperado):
    assert calcular_comision(monto) == esperado


def test_comision_devuelve_float():
    assert isinstance(calcular_comision(200), float)


# ---------------------------------------------------------------------------
# 2) Total = monto + comisión, redondeado a 2 decimales (RN3)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("monto, esperado", [
    (50, 50.0),         # tramo 1: sin comisión
    (100, 100.0),       # VL tramo 1
    (200, 203.0),       # ejemplo de la especificación
    (1000, 1015.0),     # VL tramo 2
    (1000.01, 1010.01), # VL tramo 3
    (123.45, 125.3),    # redondeo del total
    (100.43, 101.94),   # RN3: sin redondear daria 101.94000000000001
    (3000, 3025.0),     # ejemplo de la especificación con tope
])
def test_total(monto, esperado):
    assert calcular_total(monto) == esperado


# ---------------------------------------------------------------------------
# 3) validar_monto: devuelve el monto como float
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("monto", [0.01, 1, 100, 2500.5])
def test_validar_monto_valido(monto):
    resultado = validar_monto(monto)
    assert resultado == monto
    assert isinstance(resultado, float)


# ---------------------------------------------------------------------------
# 4) Monto válido (RN4): tipos inválidos -> TypeError
#    OJO: bool es subclase de int en Python; la especificación pide TypeError
# ---------------------------------------------------------------------------
TIPOS_INVALIDOS = ["100", "", None, [100], {"monto": 100}, True, False]
FUNCIONES = [validar_monto, calcular_comision, calcular_total]


@pytest.mark.parametrize("funcion", FUNCIONES)
@pytest.mark.parametrize("monto", TIPOS_INVALIDOS)
def test_tipo_invalido(funcion, monto):
    with pytest.raises(TypeError):
        funcion(monto)


# ---------------------------------------------------------------------------
# 5) Monto válido (RN4): números <= 0 -> ValueError
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("funcion", FUNCIONES)
@pytest.mark.parametrize("monto", [0, 0.0, -0.01, -1, -200, -3000])
def test_numero_invalido(funcion, monto):
    with pytest.raises(ValueError):
        funcion(monto)
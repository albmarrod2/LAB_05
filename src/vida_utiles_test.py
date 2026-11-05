from unittest.mock import patch

from vida_utiles import *

def test_crear_tablero():
    tablero = crear_tablero(3, 4)
    assert tablero == [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False]
    ]
    tablero[0][0] = True
    assert tablero[1][0] is False, "Las filas del tablero deben ser independientes entre sí."

def test_crear_tablero_aleatorio():
    tablero = crear_tablero_aleatorio(5, 5, 0.5)
    assert len(tablero) == 5 # Número de filas esperado
    assert all(len(fila) == 5 for fila in tablero) # Número de columnas esperado, todas las filas mismo tamaño
    assert all(isinstance(celula, bool) for fila in tablero for celula in fila)   # Todos los valores son booleanos
    assert any(celula for fila in tablero for celula in fila) # Hay valores True
    assert any(not celula for fila in tablero for celula in fila) # Hay Valores False
    with patch("vida_utiles.random.random", side_effect=[0.1] * 25 + [0.9] * 25):
        tablero_uno = crear_tablero_aleatorio(5, 5, 0.5)
        tablero_dos = crear_tablero_aleatorio(5, 5, 0.5)
    assert tablero_uno != tablero_dos, "Dos llamadas deben poder generar configuraciones distintas."
    assert tablero_uno is not tablero_dos, "Cada llamada debe devolver un tablero nuevo e independiente."
    valor_otra_fila = tablero[1][0]
    tablero[0][0] = not tablero[0][0]
    assert tablero[1][0] == valor_otra_fila, "Las filas del tablero aleatorio deben ser independientes entre sí."

def test_insertar_patron():
    tablero = crear_tablero(5, 5)
    patron = [
        [True, True],
        [True, False]
    ]
    insertar_patron(tablero, patron, 1, 1)
    assert tablero == [
        [False, False, False, False, False],
        [False, True, True, False, False],
        [False, True, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False]
    ]

def test_contar_vecinos():
    tablero = [
        [False, True, False],
        [False, False, True],
        [True, True, True]
    ]
    assert contar_vecinos(tablero, 0, 0) == 5
    assert contar_vecinos(tablero, 0, 1) == 4
    assert contar_vecinos(tablero, 1, 1) == 5
    assert contar_vecinos(tablero, 2, 2) == 4

def test_calcular_siguiente_generacion():
    tablero_inicial = [
        [False, False, False, False],
        [False, False, True, False],
        [False, False, True, False],
        [False, False, True, False]
    ]
    tablero_siguiente = calcular_siguiente_generacion(tablero_inicial)
    assert tablero_siguiente == [
        [False, False, False, False],
        [False, False, False, False],
        [False, True, True, True],
        [False, False, False, False]
    ]

# Descomentar para ejecutar los tests
test_crear_tablero()
test_crear_tablero_aleatorio()
test_insertar_patron()
test_contar_vecinos()
test_calcular_siguiente_generacion()
print("Todos los tests pasaron correctamente.")

    
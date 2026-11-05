import random

def crear_tablero(filas: int, columnas: int) -> list[list[bool]]:
    """
    Crea un nuevo tablero vacío, con todas las células muertas.
    Parametros:
        filas (int): Número de filas del tablero.
        columnas (int): Número de columnas del tablero.
    Devuelve:
        Una lista de listas con todos los elementos False.
    """
    return [[False] * columnas for _ in range(filas)]
'''
 otra opcion : 
lista = []
lista_de_listas = []
for _ in range(columnas):
    lista.append(False)
for _ in range(filas):
    lista_de_listas.append(False)
return lista_de_listas
'''


def crear_tablero_aleatorio(filas: int, columnas: int, probabilidad_vida: float) -> list[list[bool]]:
    """
    Crea un tablero con células vivas distribuidas aleatoriamente.

    Parámetros:
        filas (int): Número de filas del tablero.
        columnas (int): Número de columnas del tablero.
        probabilidad_vida (float): Un valor entre 0.0 y 1.0 que representa la
                                   probabilidad de que una célula esté viva.

    Devuelve:
        Una lista de listas que representa el tablero con células vivas (True) y muertas (False).
    """
    tablero = crear_tablero(filas, columnas)
    for i in range(filas):
        for j in range(columnas):
            tablero[i][j] = random.random() < probabilidad_vida
    return tablero


def insertar_patron(tablero: list[list[bool]], patron: list[list[bool]], pos_fila: int, pos_col: int):
    """
    Inserta un patrón (una pequeña matriz) en el tablero en una posición dada.
    Parámetros:
        tablero (list[list[bool]]): El tablero donde se insertará el patrón.
        patron (list[list[bool]]): El patrón a insertar.
        pos_fila (int): La fila en la que se insertará la esquina superior izquierda del patrón.
        pos_col (int): La columna en la que se insertará la esquina superior izquierda del patrón.
    """
    f_tablero = len(tablero)
    c_tablero = len(tablero[0])
    f_patron = len(patron)
    c_patron = len(patron[0])
    for i in range(f_patron):
        for j in range(c_patron):
            f_dest = pos_fila + i
            c_dest = pos_col + j
            if 0 <= f_dest < f_tablero and 0 <= c_dest < c_tablero:  # para comprobar que no se sale del tablero
                tablero[f_dest][c_dest] = patron[i][j]
    return tablero



def contar_vecinos(tablero: list[list[bool]], fila: int, col: int) -> int:
    """
    Cuenta el número de vecinos vivos de una célula en la posición (fila, col).
    El tablero es toroidal, lo que significa que los bordes se conectan.
    Parámetros:
        tablero (list[list[bool]]): El tablero actual.
        fila (int): La fila de la célula.
        col (int): La columna de la célula.
    Devuelve:
        El número de vecinos vivos (int).
    """

    n_filas = len(tablero)
    n_col = len(tablero[0])
    vecinos_vivos = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue             # para no contar la celda de la que estamos hablando
            f_vecina = (fila + i) % n_filas
            c_vecina = (col + j) % n_col      # para que no se corte en la ultima fila y columna
            if tablero[f_vecina][c_vecina]:
                vecinos_vivos += 1
    return vecinos_vivos



def calcular_siguiente_generacion(tablero) -> list[list[bool]]:
    """
    Calcula el estado del tablero en el siguiente paso de tiempo basándose en las reglas
    del Juego de la Vida.
    Parámetros:
        tablero (list[list[bool]]): El tablero actual.
    Devuelve:
        Una nueva lista de listas que representa el tablero en la siguiente generación.
    """

    f_tab = len(tablero)
    c_tab = len(tablero[0])
    res = crear_tablero(f_tab, c_tab)
    for i in range(f_tab):
        for j in range(c_tab):
            if tablero[i][j]:        # si la celda esta viva es true y se ejecuta sino no
                if 2 <= contar_vecinos(tablero, i, j) <= 3:
                    res[i][j] = True
                else:
                    res[i][j] = False
            else:
                if contar_vecinos(tablero, i, j) == 3:
                    res[i][j] = True
                else:
                    res[i][j] = False
    return res

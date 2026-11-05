import tkinter as tk
from tkinter import ttk
import vida_utiles as logica 

# --- Constantes de Configuración ---
TAM_CELDA = 15
FILAS = 40
COLUMNAS = 60
VELOCIDAD_SIM = 10 

# --- Definición de Patrones Iniciales ---
PATRONES = {    
    "Aleatorio": [[]],
    "Vacío": [[]],    
    "Bloque": [
        [True, True],
        [True, True]
    ],
    "Colmena": [
        [False, True, True, False],
        [True, False, False, True],
        [False, True, True, False]
    ],    
    "Oscilador (Blinker)": [
        [True, True, True]
    ],    
    "Planeador (Glider)": [
        [False, True, False],
        [False, False, True],
        [True, True, True]
    ],
    "Nave Espacial Ligera (LWSS)": [ 
        [False, True, False, False, True],
        [True, False, False, False, False],
        [True, False, False, False, True],
        [True, True, True, True, False]
    ],    
    "Diehard": [
        [False, False, False, False, False, False, True, False],
        [True, True, False, False, False, False, False, False],
        [False, True, False, False, False, True, True, True]
    ],
    "R-pentomino": [
    [False, True, True],
    [True, True, False],
    [False, True, False],
    ],
    "La Bellota": [
    [False, True, False, False, False, False, False],
    [True, True, False, False, True, True, True]
    ],
    "Gosper Glider Gun": [
    [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,False,True,True,False,False,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,True,True],
    [False,False,False,False,False,False,False,False,False,False,False,True,False,False,False,True,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,True,True],
    [True,True,False,False,False,False,False,False,False,False,True,False,False,False,False,False,True,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
    [True,True,False,False,False,False,False,False,False,False,True,False,False,False,True,False,True,True,False,False,False,False,True,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,True,False,False,False,False,False,True,False,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,True,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
]
}


ventana = tk.Tk()
ventana.title("Juego de la Vida de Conway")
canvas = tk.Canvas(ventana, width=COLUMNAS * TAM_CELDA, height=FILAS * TAM_CELDA, bg='white')
tablero_actual = logica.crear_tablero(FILAS, COLUMNAS)
simulacion_activa = False

def dibujar_tablero():
    """Dibuja el estado actual del tablero en el canvas."""
    canvas.delete("all")
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x1, y1 = col * TAM_CELDA, fila * TAM_CELDA
            x2, y2 = x1 + TAM_CELDA, y1 + TAM_CELDA
            
            if tablero_actual[fila][col]:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='gray')
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='lightgray')

def actualizar_simulacion():
    """Función principal que actualiza y redibuja la simulación."""
    global tablero_actual
    if simulacion_activa:
        tablero_actual = logica.calcular_siguiente_generacion(tablero_actual)
        dibujar_tablero()
        ventana.after(VELOCIDAD_SIM, actualizar_simulacion)

def iniciar_pausar_simulacion():
    """Inicia o pausa la simulación continua."""
    global simulacion_activa
    simulacion_activa = not simulacion_activa
    if simulacion_activa:
        boton_iniciar.config(text="Pausar")
        actualizar_simulacion()
    else:
        boton_iniciar.config(text="Iniciar")

def reiniciar_simulacion(event=None):
    """Reinicia el tablero con el patrón seleccionado o con uno aleatorio."""
    global simulacion_activa, tablero_actual
    simulacion_activa = False
    boton_iniciar.config(text="Iniciar")
    
    patron_seleccionado = combo_patrones.get()
    
    if patron_seleccionado == "Aleatorio":
        prob_label.pack(side=tk.LEFT, padx=(10, 0))
        prob_slider.pack(side=tk.LEFT, padx=5)
    else:
        prob_label.pack_forget()
        prob_slider.pack_forget()

    if patron_seleccionado == "Aleatorio":
        probabilidad = prob_variable.get() / 100.0
        tablero_actual = logica.crear_tablero_aleatorio(FILAS, COLUMNAS, probabilidad)
    else:
        tablero_actual = logica.crear_tablero(FILAS, COLUMNAS)
        patron = PATRONES[patron_seleccionado]
        
        if patron and patron[0]:
            pos_fila = (FILAS - len(patron)) // 2
            pos_col = (COLUMNAS - len(patron[0])) // 2
            logica.insertar_patron(tablero_actual, patron, pos_fila, pos_col)
    
    dibujar_tablero()

def manejar_click_celda(event):
    """Activa o desactiva una célula al hacer clic si la simulación está pausada."""
    if simulacion_activa:
        return  
    
    col = event.x // TAM_CELDA
    fila = event.y // TAM_CELDA

    if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
        tablero_actual[fila][col] = not tablero_actual[fila][col]
        dibujar_tablero()  


canvas.pack()
canvas.bind("<Button-1>", manejar_click_celda)

frame_controles = ttk.Frame(ventana, padding="10")
frame_controles.pack()

boton_iniciar = ttk.Button(frame_controles, text="Iniciar", command=iniciar_pausar_simulacion)
boton_iniciar.pack(side=tk.LEFT, padx=5)

boton_reiniciar = ttk.Button(frame_controles, text="Reiniciar", command=reiniciar_simulacion)
boton_reiniciar.pack(side=tk.LEFT, padx=5)

ttk.Label(frame_controles, text="Patrón inicial:").pack(side=tk.LEFT, padx=(10, 5))
combo_patrones = ttk.Combobox(frame_controles, values=list(PATRONES.keys()), state="readonly")
combo_patrones.current(0)
combo_patrones.pack(side=tk.LEFT)
combo_patrones.bind("<<ComboboxSelected>>", reiniciar_simulacion)

prob_label = ttk.Label(frame_controles, text="Prob (%):")
prob_variable = tk.DoubleVar(value=20)
prob_slider = ttk.Scale(
    frame_controles, 
    from_=0, 
    to=100, 
    orient=tk.HORIZONTAL, 
    variable=prob_variable,
    command=lambda e: reiniciar_simulacion() if combo_patrones.get() == "Aleatorio" else None
)


if __name__ == "__main__":
    reiniciar_simulacion() 
    ventana.mainloop()
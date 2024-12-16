from pyswip import Prolog
import time

# Inicializa Prolog y consulta el archivo
prolog = Prolog()
prolog.consult("traffic_logic.pl")

try:
    while True:
        # Avanzar al siguiente estado
        list(prolog.query("avanzar_estado."))  # Avanzar estado
        time.sleep(0.5)  # Pausa entre transiciones

except KeyboardInterrupt:
    print("\nPrograma interrumpido.")

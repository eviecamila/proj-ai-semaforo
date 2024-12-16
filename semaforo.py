from pyswip import Prolog
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from datetime import datetime

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_pins = {
    'red': [18, 27, 22, 23],
    'yellow': [24, 25, 8, 11],
    'green': [12, 16, 20, 21]
}

# Inicialización de pines GPIO
for color in led_pins:
    for pin in led_pins[color]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# Configuración de la cámara
cap = cv2.VideoCapture(0)
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')

# Inicializar Prolog
prolog = Prolog()
prolog.consult("traffic_logic.pl")

# Función para obtener el estado actual de los semáforos
def obtener_estados():
    consulta = list(prolog.query("estado_actual([sem1, sem2, sem3, sem4], Estados)"))
    if consulta:
        return consulta[0]['Estados']
    return ['rojo', 'rojo', 'rojo', 'rojo']  # Default en caso de error

# Función para actualizar el hardware de los semáforos
def actualizar_semaforos(estados):
    for i, estado in enumerate(estados):
        if estado == 'verde':
            GPIO.output(led_pins['green'][i], GPIO.HIGH)
            GPIO.output(led_pins['yellow'][i], GPIO.LOW)
            GPIO.output(led_pins['red'][i], GPIO.LOW)
        elif estado == 'amarillo':
            GPIO.output(led_pins['yellow'][i], GPIO.HIGH)
            GPIO.output(led_pins['red'][i], GPIO.LOW)
            GPIO.output(led_pins['green'][i], GPIO.LOW)
        elif estado == 'rojo':
            GPIO.output(led_pins['red'][i], GPIO.HIGH)
            GPIO.output(led_pins['yellow'][i], GPIO.LOW)
            GPIO.output(led_pins['green'][i], GPIO.LOW)

# Función principal del programa
try:
    print("Iniciando control de semáforos...")
    while True:
        # Avanzar el estado en Prolog
        list(prolog.query("avanzar_estado."))

        # Obtener el estado actualizado de los semáforos
        estados = obtener_estados()
        print(f"Estados actualizados: {estados}")

        # Actualizar el hardware de los semáforos
        actualizar_semaforos(estados)

        # Simulación de pausa entre transiciones
        time.sleep(3)

except KeyboardInterrupt:
    print("\nInterrupción detectada. Limpiando recursos...")
finally:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()

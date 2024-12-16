import sqlite3
from datetime import datetime
from pyswip import Prolog
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_pins = {
    'red': [18, 27, 22, 23],
    'yellow': [24, 25, 8, 11],
    'green': [12, 16, 20, 21]
}

# Inicialización de pines como salida
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

# Función para sincronizar el semáforo basado en Prolog
def sincronizar_cruce(cruce):
    print(f"Sincronizando cruce: {cruce}")
    for sol in prolog.query(f"sincronizar_cruce({cruce})"):
        print(f"Prolog actualizado: {sol}")
    estados = list(prolog.query(f"estado_cruce({cruce}, Estados)"))
    if estados:
        return estados[0]['Estados']
    return None

# Actualiza el semáforo en hardware
def actualizar_semaforos(cruce, estados):
    semaforos = {
        'sem1': 0, 'sem2': 1, 'sem3': 2, 'sem4': 3,
        'sem5': 0, 'sem6': 1, 'sem7': 2, 'sem8': 3,
        'sem9': 0, 'sem10': 1, 'sem11': 2, 'sem12': 3
    }
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
            GPIO.output(led_pins['green'][i], GPIO.LOW)
            GPIO.output(led_pins['yellow'][i], GPIO.LOW)

try:
    while True:
        # Capturar vehículos usando OpenCV
        ret, frame = cap.read()
        if not ret:
            continue
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)
        num_vehiculos = len(cars)

        # Obtener la fecha actual y consultar datos fijos
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Sincronizar cada cruce dinámicamente
        for cruce in ['cruce1', 'cruce2', 'cruce3']:
            estados = sincronizar_cruce(cruce)
            if estados:
                print(f"Estados del cruce {cruce}: {estados}")
                actualizar_semaforos(cruce, estados)
            time.sleep(5)  # Tiempo de espera entre sincronizaciones

except KeyboardInterrupt:
    print("\nInterrupción detectada. Limpiando recursos...")
finally:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()

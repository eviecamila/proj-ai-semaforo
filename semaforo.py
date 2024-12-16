import sqlite3
from datetime import datetime
from pyswip import Prolog
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)

led_pins = {
    'red': [18, 27, 22, 23],
    'yellow': [24, 25, 8, 7],
    'green': [12, 16, 20, 21]
}

for color in led_pins:
    for pin in led_pins[color]:
        GPIO.setup(pin, GPIO.OUT)

# Configuración de la cámara
cap = cv2.VideoCapture(0)
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')

# Inicializar Prolog
prolog = Prolog()
prolog.consult("traffic_logic.pl")

# Función para ajustar el tiempo del semáforo
def ajustar_tiempo_semaforo(num_vehiculos):
    tiempos = []
    for sol in prolog.query(f"ajustar_tiempo({num_vehiculos}, Tiempo)"):
        tiempos.append(sol["Tiempo"])
    return tiempos[0] if tiempos else 5

# Consultar datos de tráfico de la base de datos fija
def consultar_datos_trafico(fecha):
    conn = sqlite3.connect('trafico_anual.db')
    c = conn.cursor()
    c.execute("SELECT num_vehiculos FROM datos_trafico WHERE fecha = ?", (fecha,))
    resultado = c.fetchone()
    conn.close()
    return resultado[0] if resultado else 0

try:
    while True:
        # Capturar frame por frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar vehículos
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)
        num_vehiculos = len(cars)
        
        # Obtener la fecha actual
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Consultar datos de tráfico de la base de datos fija
        num_vehiculos_fijo = consultar_datos_trafico(current_date)
        
        # Ajustar tiempo del semáforo basado en los datos de la base de datos fija
        tiempo_verde = ajustar_tiempo_semaforo(num_vehiculos_fijo)
        
        # Control del semáforo
        GPIO.output(led_pins['red'][0], GPIO.HIGH)
        time.sleep(5)
        GPIO.output(led_pins['red'][0], GPIO.LOW)

        GPIO.output(led_pins['yellow'][0], GPIO.HIGH)
        time.sleep(2)
        GPIO.output(led_pins['yellow'][0], GPIO.LOW)

        GPIO.output(led_pins['green'][0], GPIO.HIGH)
        time.sleep(tiempo_verde)
        GPIO.output(led_pins['green'][0], GPIO.LOW)

        GPIO.output(led_pins['yellow'][0], GPIO.HIGH)
        time.sleep(2)
        GPIO.output(led_pins['yellow'][0], GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
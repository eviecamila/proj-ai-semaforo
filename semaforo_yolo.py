import cv2
import RPi.GPIO as GPIO
import time
from ultralytics import YOLO
from pyswip import Prolog

# CONFIGURACIÓN DE GPIO PARA SEMÁFOROS
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pines GPIO para semáforos
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

# FUNCIONES PARA CONTROLAR LOS SEMÁFOROS
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

# INICIALIZACIÓN DEL MODELO YOLO Y PROLOG
model = YOLO('runs/detect/train6/weights/best.pt')  # Ruta a tu modelo YOLO entrenado
prolog = Prolog()
prolog.consult("traffic_logic.pl")  # Lógica de Prolog

# CAPTURA DE LA WEBCAM
cap = cv2.VideoCapture(0)

# FUNCIÓN PARA DETECTAR CARROS Y ACTUALIZAR SEMÁFOROS
def procesar_deteccion():
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Realizar detección de carros
            results = model(frame, conf=0.3)
            annotated_frame = results[0].plot()

            # Contar carros detectados
            detecciones = results[0].boxes.cls
            num_carros = len(detecciones)

            # Lógica de semáforos basada en cantidad de carros
            if num_carros > 3:
                print("Muchos carros detectados. Cambiando semáforo...")
                list(prolog.query("avanzar_estado."))  # Avanzar lógica de Prolog
            elif num_carros > 0:
                print("Carros detectados. Estado normal...")
            else:
                print("Sin carros detectados. Manteniendo estado actual...")

            # Obtener el estado actualizado de los semáforos desde Prolog
            consulta = list(prolog.query("estado_actual([sem1, sem2, sem3, sem4], Estados)"))
            estados = consulta[0]['Estados'] if consulta else ['rojo'] * 4

            # Actualizar semáforos físicos
            actualizar_semaforos(estados)

            # Mostrar detecciones
            cv2.imshow("Detección de Carros", annotated_frame)

            # Salir con la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrumpido manualmente.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()
        print("Recursos liberados.")

# EJECUTAR PROGRAMA PRINCIPAL
if __name__ == "__main__":
    print("Iniciando sistema de semáforo inteligente...")
    procesar_deteccion()

import RPi.GPIO as GPIO
import time
import threading

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)  # Modo BCM (números GPIO)
GPIO.setwarnings(False)

# Definición de pines GPIO para cada semáforo
led_pins = {
    'red': [18, 27, 22, 23],       # Semáforos rojos
    'yellow': [24, 25, 8, 11],      # Semáforos amarillos
    'green': [12, 16, 20, 21]      # Semáforos verdes
}

# Configurar todos los pines como salida
for color in led_pins:
    for pin in led_pins[color]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# Variable global para controlar el hilo
stop_thread = False

# Función para togglear LEDs de un semáforo específico
def toggle_leds(semaforo_num):
    global stop_thread
    stop_thread = False  # Reiniciar bandera
    
    print(f"Iniciando toggling del semáforo {semaforo_num}...")
    red_pin = led_pins['red'][semaforo_num - 1]
    yellow_pin = led_pins['yellow'][semaforo_num - 1]
    green_pin = led_pins['green'][semaforo_num - 1]

    while not stop_thread:
        # Toggle LEDs
        GPIO.output(red_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(red_pin, GPIO.LOW)

        GPIO.output(yellow_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(yellow_pin, GPIO.LOW)

        GPIO.output(green_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(green_pin, GPIO.LOW)

    print(f"Toggling del semáforo {semaforo_num} detenido.")

# Función principal
def main():
    global stop_thread
    current_thread = None

    try:
        while True:
            # Pedir número del semáforo
            print("\nSelecciona un semáforo (1-4) para togglear los LEDs:")
            print("Presiona '1' nuevamente para detener el toggling.")
            semaforo_num = input("Ingresa el número (1-4): ")

            if semaforo_num == '1' and current_thread:
                print("Deteniendo el hilo actual...")
                stop_thread = True
                current_thread.join()
                current_thread = None
                print("Hilo detenido.")
                continue

            if semaforo_num in ['1', '2', '3', '4']:
                semaforo_num = int(semaforo_num)
                stop_thread = True  # Detener cualquier hilo activo
                if current_thread:
                    current_thread.join()

                # Iniciar nuevo hilo
                stop_thread = False
                current_thread = threading.Thread(target=toggle_leds, args=(semaforo_num,))
                current_thread.start()
            else:
                print("Número inválido. Ingresa un valor entre 1 y 4.")

    except KeyboardInterrupt:
        print("\nSaliendo... Limpiando GPIO.")
        stop_thread = True
        if current_thread:
            current_thread.join()
        GPIO.cleanup()

# Ejecutar la función principal
if __name__ == "__main__":
    main()

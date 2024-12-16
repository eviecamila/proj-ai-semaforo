import os
import cv2

# Ruta absoluta
current_dir = os.path.dirname(os.path.abspath(__file__))
haar_path = os.path.join(current_dir, "haarcascade_car.xml")

# Cargar clasificador
car_cascade = cv2.CascadeClassifier(haar_path)

if car_cascade.empty():
    print("Error: No se pudo cargar el clasificador.")
    exit()
else:
    print("Clasificador cargado correctamente.")

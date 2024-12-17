import cv2
from ultralytics import YOLO

# Cargar el modelo entrenado
model = YOLO('runs/detect/train7/weights/best.pt')  # Ruta al modelo entrenado

# Capturar video desde la webcam (0 = primera cámara disponible)
cap = cv2.VideoCapture(0)

# Configurar resolución de la cámara (opcional)
cap.set(3, 1280)  # Ancho
cap.set(4, 720)  # Alto

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el video.")
        break

    # Realizar la predicción con el modelo YOLOv8
    results = model(frame, conf=0.3)  # conf=0.3 para filtrar detecciones de baja confianza
    annotated_frame = results[0].plot()  # Dibujar las predicciones en el frame

    # Mostrar el resultado en tiempo real
    cv2.imshow('Detección en Vivo', annotated_frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Modelo base

# Entrenar el modelo con más épocas
model.train(data="data.yaml", epochs=100, imgsz=640, batch=8, augment=True)

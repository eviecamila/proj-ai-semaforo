import cv2
import os

# Ruta del video y carpeta destino
video_path = 'video.mp4'
output_dir = './frames/'
os.makedirs(output_dir, exist_ok=True)

# Cargar video
cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Guardar frame cada X frames (ajusta este valor)
    if frame_count % 5 == 0:
        frame_filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_filename, frame)
    frame_count += 1

cap.release()
print(f"Frames extraídos: {frame_count // 5}")

import cv2
from pathlib import Path

video_path = "mlbb-video/live.mp4"

output_dir = Path("dataset/auto_frames")
output_dir.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open the video")
    exit()

ret, frame = cap.read()

if not ret:
    print("Error: Could not open the video")
    exit()

print("Select the hero with your mouse.")
print("Press ENTER after selecting.")
print("Press C to cancel.")

box = cv2.selectROI(
    "select Hero",
    frame,
    fromCenter = False,
    showCrosshair = True

)

cv2.destroyWindow("select Hero ")

x, y, w, h = box

if w == 0 or h == 0:
    print("No hero selected")
    cap.release()
    exit()

print("Hero Selected: ")
print(f"x={x}, y={y}, w={w}, h={h}")
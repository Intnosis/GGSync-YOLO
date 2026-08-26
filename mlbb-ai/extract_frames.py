import cv2
from pathlib import Path

video_path = "mlbb-video/live.mp4"
output_dir = Path("dataset/raw_frames")

output_dir.mkdir(parents=True, exist_ok=True)

video = cv2.VideoCapture(video_path)

if not video.isOpened():
    print("ERROR: Could not open the video.")
    exit()

frame_number = 0
saved_number = 0

while True:
    success, frame = video.read()

    if not success:
        break

    
    if frame_number % 10 == 0:
        filename = output_dir / f"frame_{saved_number:05d}.jpg"

        cv2.imwrite(str(filename), frame)

        saved_number += 1

    frame_number += 1

video.release()

print(f"Finished!")
print(f"Total video frames: {frame_number}")
print(f"Frames saved: {saved_number}")
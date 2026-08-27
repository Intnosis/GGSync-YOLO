import cv2
import numpy as np

frame = cv2.imread("crop/minimap_crop_test.png")
h, w = frame.shape[:2]

if frame is None:
    print("File not found, please recheck it")

circular_mask =  np.zeros((h,w), dtype=np.uint8)
center = (w // 2, h // 2)
radius = min(w,h) // 2
cv2.circle(circular_mask, center, radius, 255, -1)

final_mask = cv2.bitwise_and(frame,frame, mask=circular_mask)
cv2.imwrite("minimap_circle/minimap_circle.png", final_mask)

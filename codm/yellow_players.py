import cv2
import numpy as np

frame = cv2.imread("minimap_circle/minimap_circle.png")
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

lower_bound = np.array([8, 119, 104])
upper_bound = np.array([24, 207, 234])

mask = cv2.inRange(hsv, lower_bound, upper_bound)

cv2.imwrite("team/team_a_crop.png", mask)



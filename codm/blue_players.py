import cv2
import numpy as np

frame = cv2.imread("crop/minimap_crop_test.png")
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

lower_bound = np.array([98,69,129])
upper_bound = np.array([116,150,184])

mask = cv2.inRange(hsv, lower_bound, upper_bound)

cv2.imwrite("team_a/team_a.png",mask)


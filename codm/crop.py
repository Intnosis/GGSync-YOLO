import cv2

frame = cv2.imread("frames/frame_0001.png")

MINIMAP_ROI = {"x1":0, "y1": 434, "x2":353, "y2":743}
PLAYER_BAR_ROI = {"x1": 7, "y1": 0, "x2": 1333, "y2":156}

minimap_frame = frame[
    MINIMAP_ROI["y1"]:MINIMAP_ROI["y2"],
    MINIMAP_ROI["x1"]:MINIMAP_ROI["x2"]
]

player_bar_frame = frame[
    PLAYER_BAR_ROI["y1"]:PLAYER_BAR_ROI["y2"],
    PLAYER_BAR_ROI["x1"]:PLAYER_BAR_ROI["x2"]
]

cv2.imwrite("crop/minimap_crop_test.png", minimap_frame)
cv2.imwrite("crop/player_crop_test.png",player_bar_frame)
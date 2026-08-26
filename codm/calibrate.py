import cv2

frame = cv2.imread("frames/frame_0001.png")
clone = frame.copy()

def click_event(event, x,y,flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"clicked_at: ({x}), ({y})")
        cv2.circle(clone, (x,y), 3, (0,255,0), -1)
        cv2.imshow("frame", clone)

def player_click_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"clicked at: ({x}), ({y})")
        cv2.circle(clone, (x,y), 3, (0,255,0), -1)
        cv2.imshow("frame",clone)

cv2.imshow("frame",clone)
cv2.setMouseCallback("frame", player_click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()


# MINMAP_ROI = {"x1":0, "y1": 434, "x2":353, "y2":743}
# PLAYER_BAR_ROI = {"x1": 7, "y1": 0, "x2": 1333, "y2":156}

# minimap_crop=frame[434:743, 0:353]
# player_bar_crop=frame[0:156, 0:1333]

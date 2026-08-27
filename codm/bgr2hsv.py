import cv2

frame = cv2.imread("crop/minimap_crop_test.png")

def color_click_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr_pixel = frame[y,x]
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_pixel = hsv_frame[y,x]
        print(f"Clicked at ({x}), ({y}) BGR: {bgr_pixel}, HSV: {hsv_pixel}")

cv2.imshow("minimap", frame)
cv2.setMouseCallback("minimap", color_click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
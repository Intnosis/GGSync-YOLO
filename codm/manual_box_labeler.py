import cv2
import json

IMAGE_PATH = "minimap_circle_only.png"
OUTPUT_JSON = "labels.json"
BOX_SIZE = 14  

frame = cv2.imread(IMAGE_PATH)
if frame is None:
    raise SystemExit(f"Could not load {IMAGE_PATH} -- check the path.")

clone = frame.copy()
boxes = []


def redraw():
    global clone
    clone = frame.copy()
    for b in boxes:
        cv2.rectangle(
            clone,
            (b["x"], b["y"]),
            (b["x"] + b["w"], b["y"] + b["h"]),
            (0, 0, 255),
            1
        )
    cv2.imshow("label", clone)


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        half = BOX_SIZE // 2
        box = {
            "x": max(0, x - half),
            "y": max(0, y - half),
            "w": BOX_SIZE,
            "h": BOX_SIZE,
            "class": "player"
        }
        boxes.append(box)
        print(f"Box added at ({x}, {y}) -> {box}")
        redraw()


cv2.imshow("label", clone)
cv2.setMouseCallback("label", click_event)

print("Click each player dot's center. Press 'u' to undo, 's' to save, 'q' to quit.")

while True:
    key = cv2.waitKey(0) & 0xFF

    if key == ord('u'):
        if boxes:
            removed = boxes.pop()
            print(f"Removed last box: {removed}")
            redraw()
        else:
            print("No boxes to undo.")

    elif key == ord('s'):
        with open(OUTPUT_JSON, "w") as f:
            json.dump(boxes, f, indent=2)
        print(f"Saved {len(boxes)} boxes to {OUTPUT_JSON}")
        break

    elif key == ord('q'):
        print("Quit without saving.")
        break

cv2.destroyAllWindows()

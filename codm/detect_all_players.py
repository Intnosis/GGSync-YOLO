# can be still change this is for automatic detecting player

import cv2
import numpy as np


# Hough Circle detection settings
MIN_DIST_BETWEEN_CIRCLES = 8   # minimum pixel distance between two detected circle centers
EDGE_SENSITIVITY = 80          # param1 -- edge detection sensitivity, higher = stricter edges
CIRCLE_CONFIDENCE = 14         # param2 -- lower = more circles detected (more false positives too)
MIN_RADIUS = 4
MAX_RADIUS = 10

# Saturation filter -- separates real (colored) player badges from
# gray/desaturated UI elements like site markers
MIN_SATURATION = 45


def detect_players(bgr_image):
    gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    gray_blur = cv2.medianBlur(gray, 3)

    circles = cv2.HoughCircles(
        gray_blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=MIN_DIST_BETWEEN_CIRCLES,
        param1=EDGE_SENSITIVITY,
        param2=CIRCLE_CONFIDENCE,
        minRadius=MIN_RADIUS,
        maxRadius=MAX_RADIUS
    )

    detected = []
    if circles is None:
        return detected

    circles = np.round(circles[0, :]).astype("int")

    for (x, y, r) in circles:
        x1, y1 = max(0, x - r), max(0, y - r)
        x2, y2 = min(bgr_image.shape[1], x + r), min(bgr_image.shape[0], y + r)

        region_hsv = hsv[y1:y2, x1:x2]
        if region_hsv.size == 0:
            continue

        mean_saturation = region_hsv[:, :, 1].mean()
        if mean_saturation < MIN_SATURATION:
            continue  # gray UI element (e.g. site marker), not a player

        detected.append({
            "x": int(x), "y": int(y), "radius": int(r),
            "saturation": round(float(mean_saturation), 1)
        })

    return detected


def main():
    frame = cv2.imread("minimap_circle_only.png")
    if frame is None:
        print("Could not load minimap_circle_only.png -- check the path.")
        return

    detected = detect_players(frame)

    output = frame.copy()
    for d in detected:
        cv2.circle(output, (d["x"], d["y"]), d["radius"], (0, 0, 255), 1)
        print(d)

    cv2.imwrite("players_detected.png", output)
    print(f"\nDetected {len(detected)} player(s) -- saved players_detected.png")


if __name__ == "__main__":
    main()

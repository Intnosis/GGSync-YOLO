import cv2
import numpy as np
import json

IMAGE_PATH = "minimap_circle_only.png"
LABELS_PATH = "labels.json"
LOCAL_STD_KERNEL = 7


def compute_local_contrast_map(gray_image):
    gray_f = gray_image.astype(np.float32)
    mean = cv2.blur(gray_f, (LOCAL_STD_KERNEL, LOCAL_STD_KERNEL))
    mean_sq = cv2.blur(gray_f * gray_f, (LOCAL_STD_KERNEL, LOCAL_STD_KERNEL))
    variance = mean_sq - mean * mean
    variance[variance < 0] = 0
    return np.sqrt(variance)


def main():
    frame = cv2.imread(IMAGE_PATH)
    if frame is None:
        print(f"Could not load {IMAGE_PATH}")
        return

    with open(LABELS_PATH, "r") as f:
        boxes = json.load(f)

    if not boxes:
        print("No boxes found in labels.json -- label some players first.")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    local_std_map = compute_local_contrast_map(gray)

    print("=== Measurements from YOUR labeled player boxes ===\n")

    areas, aspect_ratios, contrasts, saturations = [], [], [], []

    for i, b in enumerate(boxes):
        x, y, w, h = b["x"], b["y"], b["w"], b["h"]

        region_std_map = local_std_map[y:y + h, x:x + w]
        region_hsv = hsv[y:y + h, x:x + w]

        area = w * h
        aspect_ratio = w / float(h)
        avg_contrast = region_std_map.mean()
        avg_saturation = region_hsv[:, :, 1].mean()

        areas.append(area)
        aspect_ratios.append(aspect_ratio)
        contrasts.append(avg_contrast)
        saturations.append(avg_saturation)

        print(f"Box {i+1} at ({x},{y}) size {w}x{h}:")
        print(f"  area={area}  aspect_ratio={aspect_ratio:.2f}")
        print(f"  avg_local_contrast={avg_contrast:.1f}  avg_saturation={avg_saturation:.1f}\n")

    print("=== Suggested threshold ranges (based on your real badges) ===\n")
    print(f"MIN_AREA / MAX_AREA:        {min(areas)} to {max(areas)}  (consider padding +/- 20%)")
    print(f"MIN_ASPECT_RATIO / MAX:     {min(aspect_ratios):.2f} to {max(aspect_ratios):.2f}")
    print(f"Average local contrast:     {np.mean(contrasts):.1f}  (set CONTRAST_THRESHOLD comfortably below this)")
    print(f"Average saturation:         {np.mean(saturations):.1f}  (set MIN_SATURATION comfortably below this)")

    # ---- Sample background/terrain corners for comparison ----
    print("\n=== Measurements from background corners (for comparison) ===\n")
    h_img, w_img = gray.shape
    corner_size = 20
    corners = {
        "top_left": (0, 0),
        "top_right": (w_img - corner_size, 0),
        "bottom_left": (0, h_img - corner_size),
        "bottom_right": (w_img - corner_size, h_img - corner_size),
    }

    for name, (cx, cy) in corners.items():
        region_std_map = local_std_map[cy:cy + corner_size, cx:cx + corner_size]
        region_hsv = hsv[cy:cy + corner_size, cx:cx + corner_size]
        print(f"{name}: avg_contrast={region_std_map.mean():.1f}  avg_saturation={region_hsv[:,:,1].mean():.1f}")

    print("\nCompare these corner numbers against your badge numbers above --")
    print("set CONTRAST_THRESHOLD and MIN_SATURATION somewhere in between the two groups.")


if __name__ == "__main__":
    main()

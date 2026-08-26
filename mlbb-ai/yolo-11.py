from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model.track(
    source ="mlbb-video/live.mp4",
    tracker = "botsort.yaml",
    conf = 0.15,
    save=True,
    show=True
)
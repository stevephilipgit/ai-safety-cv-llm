from ultralytics import YOLO
import cv2

CLASS_NAMES = [
    "Gloves",
    "Hard_hat",
    "Mask",
    "Person",
    "Safety_boots",
    "Vest"
]

class SafetyDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image not found or invalid")

        results = self.model(img)[0]
        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = CLASS_NAMES[cls_id]

            detections.append({
                "violation": label,
                "confidence": round(conf, 3),
                "category": "person" if label == "Person" else "ppe"
            })

        return detections

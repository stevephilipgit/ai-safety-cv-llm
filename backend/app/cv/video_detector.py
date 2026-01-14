import cv2
import os
from app.cv.detector import SafetyDetector
from app.logic.violations import evaluate_violations


class VideoSafetyAnalyzer:
    def __init__(self, model_path: str):
        self.detector = SafetyDetector(model_path)

    def analyze(self, video_path: str, frame_skip: int = 10):
        if not os.path.exists(video_path):
            raise ValueError("Video file does not exist")

        cap = cv2.VideoCapture(video_path)
        frame_id = 0
        events = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_id += 1
            if frame_id % frame_skip != 0:
                continue

            temp_img = "temp_frame.jpg"
            cv2.imwrite(temp_img, frame)

            detections = self.detector.detect(temp_img)

            # 🔹 Unified violation evaluation
            result = evaluate_violations(detections)

            # 🔹 Store only meaningful frames
            if result["status"] != "No person detected":
                events.append({
                    "frame": frame_id,
                    "detections": detections,
                    "violations": result["violations"],  # always list
                    "status": result["status"]
                })

        cap.release()

        return events

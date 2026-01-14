import cv2
from ultralytics import YOLO
import os

class VideoAnnotator:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def annotate(self, input_video: str, output_video: str):
        if not os.path.exists(input_video):
            raise ValueError("Input video does not exist")

        cap = cv2.VideoCapture(input_video)
        if not cap.isOpened():
            raise ValueError("Could not open video")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25

        # ✅ Safer FOURCC for Windows
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        out = cv2.VideoWriter(
            output_video,
            fourcc,
            fps,
            (width, height)
        )

        if not out.isOpened():
            raise RuntimeError("VideoWriter failed to open")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame)[0]

            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, max(y1 - 10, 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            out.write(frame)

        cap.release()
        out.release()

        return output_video

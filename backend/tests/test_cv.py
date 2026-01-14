from app.cv.detector import SafetyDetector
from app.logic.violations import evaluate_violations

detector = SafetyDetector("models/best.pt")

detections = detector.detect("C:\\Users\\Steve\\Desktop\\Safety_CV&LLM\\assets\\test_image.jpg")
violations = evaluate_violations(detections)

print("Detections:", detections)
print("Violations:", violations)

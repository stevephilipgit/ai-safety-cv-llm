# backend/app/logic/violations.py

PERSON_CONF_THRESHOLD = 0.3     # allow distant / small persons
PPE_CONF_THRESHOLD = 0.5        # stricter for PPE items

REQUIRED_PPE = {"Hard_hat", "Vest", "Mask"}

def evaluate_violations(detections):
    """
    detections: List[{
        "violation": <label>,
        "confidence": <float>
    }]
    """

    persons = [
        d for d in detections
        if d["violation"] == "Person" and d["confidence"] >= PERSON_CONF_THRESHOLD
    ]

    ppe_items = [
        d for d in detections
        if d["violation"] != "Person" and d["confidence"] >= PPE_CONF_THRESHOLD
    ]

    # 🚫 No person → no safety context
    if not persons:
        return {
            "violations": [],
            "status": "No person detected"
        }

    detected_ppe = {d["violation"] for d in ppe_items}
    violations = []

    # 🚨 Absence-based safety inference
    if "Hard_hat" not in detected_ppe:
        violations.append({
            "violation": "No Hard Hat",
            "severity": "High"
        })

    if "Vest" not in detected_ppe:
        violations.append({
            "violation": "No Safety Vest",
            "severity": "Medium"
        })

    if "Mask" not in detected_ppe:
        violations.append({
            "violation": "No Mask",
            "severity": "Medium"
        })

    if not violations:
        return {
            "violations": [],
            "status": "All required PPE detected"
        }

    return {
        "violations": violations,
        "status": "Violation detected"
    }

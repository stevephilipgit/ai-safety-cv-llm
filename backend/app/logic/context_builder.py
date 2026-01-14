REQUIRED_PPE = {"Hard_hat", "Mask", "Vest"}

def build_safety_context(detections):
    detected_labels = {d["violation"] for d in detections}

    detected_ppe = list(detected_labels & REQUIRED_PPE)
    missing_ppe = list(REQUIRED_PPE - detected_labels)

    return detected_ppe, missing_ppe

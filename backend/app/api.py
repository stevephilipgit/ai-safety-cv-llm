from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
import traceback

from fastapi.responses import FileResponse

from app.cv.detector import SafetyDetector
from app.cv.video_annotator import VideoAnnotator
from app.cv.video_detector import VideoSafetyAnalyzer

from app.logic.aggregator import aggregate_violations
from app.logic.violations import evaluate_violations
from app.logic.context_builder import build_safety_context

from app.llm.reasoner import (
    explain_safety_context,
    explain_aggregated_violation
)

from app.reports.pdf_reports import generate_pdf
from app.utils.zipper import create_zip

# --------------------------------------------------
app = FastAPI(title="AI Safety Monitoring System")

# ----------------- INIT -----------------
detector = SafetyDetector("models/best.pt")
video_analyzer = VideoSafetyAnalyzer("models/best.pt")
video_annotator = VideoAnnotator("models/best.pt")

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================================================
# IMAGE ANALYSIS
# ==================================================
@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        contents = await file.read()
        if not contents:
            raise ValueError("Uploaded file is empty")

        with open(file_path, "wb") as f:
            f.write(contents)

        # 1️⃣ Detect objects
        detections = detector.detect(file_path)

        # 2️⃣ Build safety context
        detected_ppe, missing_ppe = build_safety_context(detections)

        # 3️⃣ LLM reasoning (single call)
        llm_explanation = explain_safety_context(
            detected_ppe=detected_ppe,
            missing_ppe=missing_ppe
        )

        return {
            "detections": detections,
            "detected_ppe": detected_ppe,
            "missing_ppe": missing_ppe,
            "llm_explanation": llm_explanation
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ==================================================
# VIDEO ANALYSIS (JSON)
# ==================================================
@app.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    video_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    events = video_analyzer.analyze(video_path)

    response = []
    for e in events:
        detected_ppe, missing_ppe = build_safety_context(e["detections"])

        explanation = explain_safety_context(
            detected_ppe=detected_ppe,
            missing_ppe=missing_ppe
        )

        response.append({
            "frame": e["frame"],
            "detections": e["detections"],
            "detected_ppe": detected_ppe,
            "missing_ppe": missing_ppe,
            "llm_explanation": explanation
        })

    return {
        "total_events": len(response),
        "events": response
    }

# ==================================================
# VIDEO EXPORT (ZIP)
# ==================================================
@app.post("/analyze-video-export")
async def analyze_video_export(file: UploadFile = File(...)):
    try:
        video_path = f"{UPLOAD_DIR}/{file.filename}"
        contents = await file.read()
        if not contents:
            raise ValueError("Uploaded video is empty")

        with open(video_path, "wb") as f:
            f.write(contents)

        # 1️⃣ Annotated video
        annotated_video = f"{OUTPUT_DIR}/annotated_video.mp4"
        video_annotator.annotate(video_path, annotated_video)

        # 2️⃣ Analyze video
        events = video_analyzer.analyze(video_path)

        # 3️⃣ Build report summary
        if not events:
            summary = [{
                "violation": "Analysis Summary",
                "occurrences": 0,
                "explanation": (
                    "The video was processed, but no valid worker detections "
                    "were found. Safety assessment could not be performed."
                )
            }]
        else:
            aggregated = aggregate_violations(events)
            summary = []

            if not aggregated:
                summary.append({
                    "violation": "PPE Compliance",
                    "occurrences": len(events),
                    "explanation": (
                        "All detected workers appear to be compliant with the "
                        "required personal protective equipment (PPE). "
                        "No safety violations were consistently observed."
                    )
                })
            else:
                for violation, frames in aggregated.items():
                    summary.append({
                        "violation": violation,
                        "occurrences": len(frames),
                        "explanation": explain_aggregated_violation(
                            violation,
                            frames
                        )
                    })

        # 4️⃣ PDF report
        pdf_path = f"{OUTPUT_DIR}/safety_report.pdf"
        generate_pdf(pdf_path, summary)

        # 5️⃣ ZIP export
        zip_path = f"{OUTPUT_DIR}/safety_audit.zip"
        create_zip(zip_path, [
            annotated_video,
            pdf_path,
            video_path
        ])

        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="safety_audit.zip"
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

 AI Safety Monitoring System (Computer Vision + LLM)
An end-to-end AI-powered workplace safety auditing system that combines Computer Vision (YOLO) and a Local Large Language Model (Gemma via Ollama) to detect PPE compliance, explain safety risks, and generate audit-ready reports.
This project demonstrates real-world AI system design, not just model inference.

🚀 Key Capabilities

🧍 Person & PPE detection (Helmet, Mask, Vest, Gloves, Boots)
🧠 Context-aware LLM safety reasoning (no hallucination)
🖼️ Image-based safety analysis
🎥 Video-based safety auditing with frame sampling
🎯 Absence-based PPE violation inference
📄 Clean, professional PDF safety reports
🎞️ Annotated safety audit videos
📦 Exportable ZIP audit package
🌐 REST API (FastAPI)
🖥️ Interactive UI (Streamlit)



🧠 Why This Project Is Different

Most CV safety demos only detect objects.
This system:
Separates detection from decision logic
Uses rule-based reasoning for safety compliance
Invokes an LLM only for explanation, not decision-making
Prevents hallucination by design
Produces human-readable audit reports
This mirrors how real industrial safety systems are built.

🏗️ System Architecture
Image / Video Input
        ↓
YOLO Object Detection
        ↓
Safety Rule Engine
(Person detected → PPE presence/absence)
        ↓
Safety Context Builder
(Detected PPE vs Missing PPE)
        ↓
Local LLM (Gemma via Ollama)
        ↓
Human-Readable Safety Explanation
        ↓
PDF Report + Annotated Video
        ↓
ZIP Safety Audit Package


🔍 How CV + LLM Work Together
Computer Vision (YOLO)
Detects objects with confidence
Never guesses missing PPE
Outputs only what is visible
Safety Rule Engine
If Person is detected:
Required PPE is inferred
Missing PPE becomes a violation
Absence-based logic avoids false confidence
LLM (Gemma)
Triggered once per image or frame
Receives structured safety context

Explains:
What PPE is correctly worn
What PPE is missing
Why missing PPE is risky
What should be done immediately

No punishment, legal, or policy enforcement language



📂 Project Structure
Safety_CV&LLM/
│
├── backend/
│   ├── app/
│   │   ├── api.py
│   │   ├── cv/
│   │   │   ├── detector.py
│   │   │   ├── video_detector.py
│   │   │   └── video_annotator.py
│   │   ├── logic/
│   │   │   ├── violations.py
│   │   │   ├── context_builder.py
│   │   │   └── aggregator.py
│   │   ├── llm/
│   │   │   └── reasoner.py
│   │   ├── reports/
│   │   │   └── pdf_reports.py
│   │   └── utils/
│   │       └── zipper.py
│   └── main.py
│
├── frontend/
│   └── ui/
│       └── app.py   (Streamlit UI)
│
├── models/
│   └── best.pt     (trained YOLO model)
│
├── results_tested/ (screenshots for demo)
├── requirements.txt
├── README.md
└── .gitignore


🧰 Tech Stack
Backend
Python 3.10+
FastAPI
Ultralytics YOLO
OpenCV
ReportLab (PDF generation)
LangChain
Ollama (local LLM runtime)
Frontend
Streamlit
Requests
Pillow

Models
YOLO (custom PPE dataset)  
Gemma 2B (local inference via Ollama)



📦 Installation
1️⃣ Clone Repository
git clone https://github.com/stevephilipgit/Safety_CV_LLM.git
cd Safety_CV_LLM

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt


▶️ Running the System

1️⃣ Start Ollama (LLM)
first download ollama in local system
ollama pull gemma:2b
ollama run gemma:2b

2️⃣ Start Backend (FastAPI)
uvicorn backend.app.api:app --reload

API Docs:
http://127.0.0.1:8000/docs


3️⃣ Start Frontend (Streamlit)
streamlit run frontend/ui/app.py


🧪 Example Outputs

Image Safety Analysis
Detected PPE shown clearly
Missing PPE inferred correctly
Single LLM explanation per image
Video Safety Audit
Frame-based analysis
Aggregated violations
Annotated output video


Downloadable ZIP:
Annotated video
PDF audit report
Original input video


🎥 Demo & Screenshots
UI Screenshots 


Image Analysis UI
results_tested/ai_safety_image_ui.png


Video Audit UI
results_tested/ai_safety_video_ui.png


Demo Videos (
Image Safety Demo: (YouTube / Drive link)
Video Safety Audit Demo: (YouTube / Drive link)



🏭 Real-World Applications
Construction site safety monitoring
Manufacturing floor compliance
Industrial PPE audits
Workplace risk analysis
Safety officer decision support


👨‍💻 Author
Name: Steve Philip
GitHub: https://github.com/stevephilipgit
Email: stevephilip.me86@gmail.com 

⭐ Notes

Designed to avoid LLM hallucination
Separation of concerns (CV ≠ Reasoning)
Suitable for enterprise-grade safety systems
Portfolio & interview ready

🙌 Feedback & Contributions
Feel free to open issues, fork the repository, or suggest improvements.
If you found this project useful, please ⭐ star the repo.

---


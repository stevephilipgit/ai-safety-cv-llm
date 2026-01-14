import streamlit as st
import requests
from PIL import Image

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
BACKEND_URL = "http://127.0.0.1:8000"
TIMEOUT = 300  # seconds (for long video processing)

st.set_page_config(
    page_title="AI Safety Monitoring System",
    layout="wide"
)

st.subheader("🦺 AI Safety Monitoring System")
st.subheader("Computer Vision + LLM-based Safety Audit")

tab_image, tab_video = st.tabs(["🖼️ Image Analysis", "🎥 Video Safety Audit"])

# ==================================================
# IMAGE ANALYSIS TAB
# ==================================================
with tab_image:
    st.subheader("Image Safety Analysis")

    image_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"],
        key="image_uploader"
    )

    if image_file:
        try:
            img = Image.open(image_file)
            st.image(img, caption="Uploaded Image", width=700)
        except Exception as e:
            st.error(f"Failed to load image: {e}")
                        
        if st.button("Analyze Image", key="analyze_image_btn"):
            if image_file is None:
                st.warning("Please upload an image before analyzing.")
            else:
                # 🔑 RESET FILE POINTER
                image_file.seek(0)

                with st.spinner("Analyzing image for safety violations..."):
                    try:
                        files = {"file": image_file}
                        res = requests.post(
                            f"{BACKEND_URL}/analyze",
                            files=files,
                            timeout=TIMEOUT
                        )
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend is not running.")
                        st.stop()

                if res.status_code != 200:
                    st.error(f"Backend error: {res.text}")
                else:
                    data = res.json()
                    # ----------------- RESULTS -----------------
                    st.subheader("🧾 Detection Results")
                    # 1️⃣ Raw detections
                    st.markdown("### 🔍 Detected Objects")
                    for d in data.get("detections", []):
                        st.write(
                            f"- **{d['violation']}** "
                            f"(confidence: {d.get('confidence', 'N/A')})"
                        )

                    # 2️⃣ PPE status
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### ✅ Detected PPE")
                        detected = data.get("detected_ppe", [])
                        if detected:
                            for ppe in detected:
                                st.success(ppe)
                        else:
                            st.info("No PPE detected")

                    with col2:
                        st.markdown("### ❌ Missing PPE")
                        missing = data.get("missing_ppe", [])
                        if missing:
                            for ppe in missing:
                                st.error(ppe)
                        else:
                            st.success("No missing PPE")

                    # 3️⃣ LLM explanation
                    st.markdown("### 🧠 Safety Explanation via LLM)")
                    st.info(data.get("llm_explanation", "No explanation available"))


# ==================================================
# VIDEO SAFETY AUDIT TAB
# ==================================================
with tab_video:
    st.header("Video Safety Audit (Exportable)")

    video_file = st.file_uploader(
        "Upload a safety video",
        type=["mp4", "avi", "mov"],
        key="video_uploader"
    )

    if video_file:
        st.video(video_file)  
    if st.button("Generate Safety Audit zipFile", key="analyze_video_btn"):
        if video_file is None:
            st.warning("Please upload a video before generating the audit.")
        else:
             # 🔑 RESET FILE POINTER
            video_file.seek(0)
            with st.spinner(
                "Processing video...\n"
                "This may take several minutes depending on video length."
            ):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/analyze-video-export",
                        files={"file": video_file},
                        timeout=TIMEOUT
                    )
                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend is not running. Please start FastAPI server.")
                    st.stop()
                except requests.exceptions.Timeout:
                    st.error("❌ Backend timed out while processing the video.")
                    st.stop()
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
                    st.stop()

            st.text(f"Status code: {res.status_code}")
            st.text(f"Content-Type: {res.headers.get('content-type')}")

            if res.status_code != 200:
                st.error(f"Backend error:\n{res.text}")
            else:
                st.success("✅ Safety audit package generated successfully.")

                st.download_button(
                    label="⬇️ Download Safety Audit ZIP",
                    data=res.content,
                    file_name="safety_audit.zip",
                    mime="application/zip"
                )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown("Visit github (https://github.com/stevephilipgit).")
st.caption(
    "Built with YOLO, FastAPI, Streamlit, and a local LLM for explainable safety auditing. - Steve Philip S"
)

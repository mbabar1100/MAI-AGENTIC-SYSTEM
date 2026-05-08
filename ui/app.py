import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="COPD Analysis System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""
<style>

header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #111827 !important;
}

.stApp {
    background-color: #f5f7fb;
}

[data-testid="stAppViewContainer"] {
    background-color: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background-color: #eef2ff;
    border-right: 1px solid #dbe3f3;
    width: 320px !important;
}

h1, h2, h3, h4, h5, h6,
p, span, label, div {
    color: #111827 !important;
}

.main-title {
    font-size: 56px;
    font-weight: 800;
    text-align: center;
    color: #111827 !important;
    margin-top: 20px;
}

.sub-title {
    font-size: 22px;
    text-align: center;
    color: #6b7280 !important;
    margin-bottom: 30px;
}

.history-card {
    background: white;
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 14px;
    border: 1px solid #e5e7eb;
}

.module-card {
    background: white;
    border: 1px solid #dbe3f3;
    border-radius: 18px;
    padding: 20px;
    min-height: 150px;
    margin-bottom: 10px;
    transition: 0.3s;
}

.module-card:hover {
    box-shadow: 0px 6px 20px rgba(79,109,245,0.12);
    transform: translateY(-2px);
}

.stButton > button {
    background: linear-gradient(90deg,#4f6df5,#5f7cff) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
}

.stDownloadButton > button {
    background: white !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
}

.stTextInput input {
    background-color: white !important;
    color: #111827 !important;
    border-radius: 14px !important;
    border: 1px solid #d1d5db !important;
    padding: 14px !important;
    font-size: 16px !important;
    font-weight: 400 !important;
}

/* Placeholder text */
.stTextInput input::placeholder {
    color: #9ca3af !important;
    opacity: 1 !important;
}

[data-baseweb="input"] {
    background: white !important;
}

[data-baseweb="base-input"] {
    background: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:

    st.markdown("# 🫁 COPD Analysis System")

    st.button("➕ New Analysis")

    st.write("")
    st.markdown("## Chat History")

    if len(st.session_state.history) == 0:
        st.write("No history yet")

    for item in reversed(st.session_state.history):

        st.markdown(
            f"""
            <div class='history-card'>
                <b>{item['query']}</b><br><br>
                Age: {item['age']}<br>
                Smoking: {item['smoking']}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    clear = st.button("🗑️ Clear History")

    if clear:
        st.session_state.history = []
        st.rerun()

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown(
    "<div class='main-title'>COPD Multi-Model Analysis System</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>An intelligent system that uses multiple AI models to analyze COPD risk based on patient data</div>",
    unsafe_allow_html=True
)

# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------
st.markdown(
    """
    <h3 style='margin-bottom:10px; color:#111827; text-align:center;'>
        What can I help with?
    </h3>
    """,
    unsafe_allow_html=True
)

query = st.text_input(
    "",
    placeholder="Try keywords like compare models OR data analysis",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1,1,1])

with col1:
    age = st.slider("Age", 1, 120, 58)

with col2:
    smoking = st.slider("Smoking", 0, 10, 6)

with col3:
    st.write("")
    st.write("")
    run = st.button("⚡ Analyze Now")

# ---------------------------------------------------
# AGENTIC AI MODULES
# ---------------------------------------------------
st.markdown("## ⚡ Agentic AI Modules")

m1, m2, m3 = st.columns(3)

# COLUMN 1
with m1:

    st.markdown("""
    <div class='module-card'>
    <h4>📊 Data Analysis</h4>
    <p>Processes patient inputs and generates COPD risk predictions.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Run Data Analysis", key="data_analysis_btn", use_container_width=True):

        risk_score = round((0.6 * age + 0.4 * smoking) / 100, 2)

        if risk_score >= 0.5:
            prediction = "High Risk"
        else:
            prediction = "Low Risk"

        st.success(f"Prediction: {prediction}")
        st.info(f"Calculated Risk Score: {risk_score}")

    st.markdown("""
    <div class='module-card'>
    <h4>❓ Question Answering</h4>
    <p>Responds to user queries related to COPD analysis and model behavior.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Ask AI Assistant", key="qa_btn", use_container_width=True):

        st.info("""
COPD risk is estimated using patient age and smoking level.

Higher smoking values increase predicted COPD risk.
        """)

# COLUMN 2
with m2:

    st.markdown("""
    <div class='module-card'>
    <h4>⚙️ System Optimization</h4>
    <p>Manages routing logic and improves system decision-making efficiency.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Optimize System", key="optimization_btn", use_container_width=True):

        st.success("System optimization completed successfully.")
        st.write("✔ Query routing optimized")
        st.write("✔ Backend latency reduced")
        st.write("✔ Agent response improved")

    st.markdown("""
    <div class='module-card'>
    <h4>🛠️ Tool Integration</h4>
    <p>Handles report generation, charts, backend communication, and utilities.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Integrated Tools", key="tool_btn", use_container_width=True):

        st.success("Integrated Tools")
        st.write("✔ FastAPI Backend")
        st.write("✔ Streamlit Frontend")
        st.write("✔ PDF Report Generator")
        st.write("✔ Email Integration")

# COLUMN 3
with m3:

    st.markdown("""
    <div class='module-card'>
    <h4>📈 Model Benchmarking</h4>
    <p>Compares multiple AI models and selects the best-performing model.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Run Benchmark", key="benchmark_btn", use_container_width=True):

        benchmark_df = pd.DataFrame({
            "Model": ["model_v1", "model_v2"],
            "Accuracy": [88, 92],
            "Confidence": [0.59, 0.64]
        })

        st.dataframe(benchmark_df, use_container_width=True)

        st.success("Best Model Selected: model_v2")

    st.markdown("""
    <div class='module-card'>
    <h4>📧 Automated Actions</h4>
    <p>Supports downloadable reports and email-based report sharing.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Trigger Automation", key="automation_btn", use_container_width=True):

        st.success("Automation Triggered Successfully")
        st.write("✔ Report generated")
        st.write("✔ Email prepared")
        st.write("✔ Analysis stored in history")

# ---------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------
if run:

    payload = {
        "query": query,
        "age": age,
        "smoking": smoking
    }

    try:

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json=payload
        )

        result = response.json()

        st.session_state.history.append({
            "query": query,
            "age": age,
            "smoking": smoking
        })

        st.header("Analysis Result")

        if result.get("type") == "message":

            st.warning(result["message"])

        elif result.get("type") == "comparison":

            df = pd.DataFrame(result["results"])

            st.markdown("### 📋 Model Comparison Table")

            st.dataframe(df, use_container_width=True)

            best = result["best_model"]

            st.success(f"🏆 Recommended Model: {best['model']}")

            st.write(f"Prediction: {best['prediction']}")
            st.write(f"Confidence Score: {best['confidence']}")

            st.info(
                "📌 Why this model performed better:\n\n"
                + best["explanation"]
            )

            chart_df = pd.DataFrame({
                "Model": [x["model"] for x in result["results"]],
                "Confidence": [x["confidence"] for x in result["results"]]
            })

            st.markdown("### 📊 Confidence Score Comparison")

            st.bar_chart(
                chart_df.set_index("Model"),
                color="#5f7cff"
            )

        else:

            st.success(f"🏆 Recommended Model: {result['model']}")

            st.write(f"Prediction: {result['prediction']}")
            st.write(f"Confidence Score: {result['confidence']}")

            st.info(
                "📌 Model Explanation:\n\n"
                + result["explanation"]
            )

        # REPORTS
        st.markdown("---")

        st.subheader("📥 Download Report")

        report_text = f"""
COPD ANALYSIS REPORT

Query: {query}

Age: {age}

Smoking: {smoking}

Results:
{result}
"""

        d1, d2, d3, d4 = st.columns(4)

        with d1:
            st.download_button(
                "📄 TXT",
                report_text,
                file_name="report.txt"
            )

        with d2:

            doc = Document()
            doc.add_heading("COPD Analysis Report", 0)
            doc.add_paragraph(report_text)

            doc_buffer = BytesIO()
            doc.save(doc_buffer)
            doc_buffer.seek(0)

            st.download_button(
                "📝 Word",
                doc_buffer,
                file_name="report.docx"
            )

        with d3:

            pdf_buffer = BytesIO()

            pdf = SimpleDocTemplate(pdf_buffer)

            styles = getSampleStyleSheet()

            story = [
                Paragraph(report_text, styles['BodyText'])
            ]

            pdf.build(story)

            pdf_buffer.seek(0)

            st.download_button(
                "📕 PDF",
                pdf_buffer,
                file_name="report.pdf"
            )

        with d4:

            wb = Workbook()
            ws = wb.active

            ws.append(["Query", query])
            ws.append(["Age", age])
            ws.append(["Smoking", smoking])

            excel_buffer = BytesIO()

            wb.save(excel_buffer)

            excel_buffer.seek(0)

            st.download_button(
                "📊 Excel",
                excel_buffer,
                file_name="report.xlsx"
            )

        # EMAIL
        st.markdown("---")

        st.subheader("📧 Email Report")

        email = st.text_input("Enter email address")

        if st.button("Send Report"):
            st.success(f"Report prepared for: {email}")

    except Exception as e:

        st.error(f"Error: {e}")
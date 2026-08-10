import streamlit as st
import subprocess
import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from datetime import datetime

# -------------------------------
# Load Environment Variables
# -------------------------------

load_dotenv()

# API key: Streamlit Cloud Secrets first, local .env as fallback
gemini_api_key = os.getenv("GEMINI_API_KEY")

try:
    if not gemini_api_key and "GEMINI_API_KEY" in st.secrets:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not gemini_api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=gemini_api_key)

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Toyota Production Planning Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS
# -------------------------------

st.markdown("""
<style>

.stApp{
    background:#f5f6fa;
}

section[data-testid="stSidebar"]{
    background:#202124;
}

.stButton>button{
    width:100%;
    height:55px;
    background:#EB0A1E;
    color:white;
    border:none;
    border-radius:12px;
    font-size:17px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#b00018;
}

[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 5px 12px rgba(0,0,0,.15);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:

    if os.path.exists("toyota-logo.png"):
        st.image("toyota-logo.png", width=170)

    st.title("Toyota")

    st.success("🟢 System Online")

    st.divider()

    st.write("### Modules")

    st.write("📈 Linear Programming")

    st.write("🧬 Genetic Algorithm")

    st.write("🤖 AI Assistant")

    st.divider()

    st.caption("Advanced Programming")

# -------------------------------
# Header
# -------------------------------

st.markdown("""
<div style="
background:linear-gradient(90deg,#EB0A1E,#A30017);
padding:30px;
border-radius:18px;
color:white;
">

<h1>
🚗 Toyota Production Planning Dashboard
</h1>

<h4>
AI Powered Manufacturing Optimization
</h4>

<p>

Linear Programming • Genetic Algorithm • Google Gemini AI

</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------
# Dashboard Metrics
# -------------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("🚗 Models","5")

with c2:
    st.metric("📈 Optimization","Ready")

with c3:
    st.metric("🧬 GA","Available")

with c4:
    st.metric("🤖 AI","Online")

st.write("")

# -------------------------------
# Tabs
# -------------------------------

tab1,tab2,tab3,tab4,tab5 = st.tabs(
[
"🏠 Dashboard",
"📈 Linear Programming",
"🧬 Genetic Algorithm",
"🤖 AI Assistant",
"ℹ About"
])

# -------------------------------
# Dashboard
# -------------------------------

with tab1:

    st.subheader("Dashboard")

    st.info(
        """
Welcome to Toyota Production Planning Dashboard.

This project combines:

• Linear Programming

• Genetic Algorithm

• Google Gemini AI

to optimize Toyota production.
"""
    )

    st.success(
        f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

# -------------------------------
# Linear Programming
# -------------------------------

with tab2:

    st.subheader("📈 Linear Programming Optimizer")

    st.write(
        "Optimize Toyota vehicle production using Linear Programming."
    )

    paint_capacity = st.number_input(
        "🎨 Paint Capacity",
        value=1500
     )

    body_capacity = st.number_input(
        "🏭 Body Capacity",
        value=1800
     )

    assembly_capacity = st.number_input(
        "🔧 Assembly Capacity",
        value=3500
     )

    if st.button("🚀 Solve Production Plan"):

        progress = st.progress(0)

        for i in range(100):
            progress.progress(i + 1)

        with st.spinner("Running Linear Programming..."):

            subprocess.run([
                "python",
                "lp_solver.py",
                str(paint_capacity),
                str(body_capacity),
                str(assembly_capacity)
            ])

        st.success("Optimization Completed Successfully!")

        if os.path.exists("outputs/production_plan.xlsx"):

            df = pd.read_excel(
                "outputs/production_plan.xlsx"
            )

            total = int(df["Production"].sum())

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🚗 Total Production",
                    total
                )

            with col2:
                st.metric(
                    "📦 Vehicle Types",
                    len(df)
                )

            with col3:
                st.metric(
                    "✅ Status",
                    "Completed"
                )

            st.subheader("📋 Production Plan")

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.error(
                "production_plan.xlsx not found."
            )

        if os.path.exists(
            "outputs/production_chart.png"
        ):

            st.subheader("📊 Production Chart")

            st.image(
                "outputs/production_chart.png",
                use_container_width=True
            )

        else:

            st.warning(
                "production_chart.png not found."
            )

    if os.path.exists("outputs/shadow_prices.xlsx"):

        shadow = pd.read_excel("outputs/shadow_prices.xlsx")

        st.subheader("📈 Shadow Prices")

        st.dataframe(
         shadow,
        use_container_width=True
        ) 

# -------------------------------
# Genetic Algorithm
# -------------------------------

with tab3:

    st.subheader("🧬 Genetic Algorithm Scheduler")

    population_size = st.slider(
        "👥 Population Size",
        min_value=10,
        max_value=100,
        value=30,
        step=5
    )

    generations = st.slider(
        "🔄 Generations",
        min_value=10,
        max_value=100,
        value=20,
        step=10
    )

    st.info(
        f"Population: {population_size} | "
        f"Generations: {generations}"
    )

    if st.button("🧬 Run Genetic Algorithm"):

        with st.spinner("Genetic Algorithm is running..."):

            result = subprocess.run(
                [
                    "python",
                    "ga_scheduler.py",
                    str(population_size),
                    str(generations)
                ],
                capture_output=True,
                text=True
            )

        if result.returncode == 0:

            st.success("✅ Genetic Algorithm Completed!")

            st.subheader("📊 Algorithm Result")

            if result.stdout:
                st.code(
                    result.stdout,
                    language="text"
                )
            else:
                st.warning(
                    "Algorithm finished but produced no output."
                )

        else:

            st.error("❌ Genetic Algorithm Error")

            st.code(
                result.stderr,
                language="text"
            )
   

# -------------------------------
# AI Assistant
# -------------------------------

with tab4:

    st.subheader("🤖 Toyota AI Assistant")

    question = st.text_input(
        "Ask a question about Production Planning:"
    )

    if st.button("Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            prompt = f"""
You are an AI assistant for Toyota Production Planning.

Answer questions about:
- Linear Programming
- Genetic Algorithm
- Toyota Production System
- Manufacturing Optimization

Question:
{question}
"""

            # Robust Gemini request:
            # Retry temporary 503/429 errors and fall back to another Flash model.
            import time

            def ask_gemini_with_retry(prompt_text):
                models = [
                    "gemini-flash-latest",
                    "gemini-2.5-flash",
                ]

                last_error = None

                for model_name in models:
                    for attempt in range(3):
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt_text
                            )
                            return response, model_name

                        except Exception as e:
                            last_error = e
                            error_text = str(e).lower()

                            # Retry only temporary capacity/rate-limit errors.
                            temporary_error = (
                                "503" in error_text
                                or "unavailable" in error_text
                                or "high demand" in error_text
                                or "429" in error_text
                                or "resource exhausted" in error_text
                                or "rate limit" in error_text
                            )

                            if not temporary_error:
                                raise

                            # Exponential backoff: 2s, 4s, 8s
                            if attempt < 2:
                                time.sleep(2 ** (attempt + 1))

                raise last_error

            try:
                with st.spinner("Gemini is thinking..."):
                    response, used_model = ask_gemini_with_retry(prompt)

                st.success("✅ Answer Ready!")
                st.write(response.text)

                if used_model != "gemini-flash-latest":
                    st.caption(
                        f"ℹ️ پاسخ با مدل جایگزین {used_model} تولید شد."
                    )

            except Exception as e:
                error_text = str(e).lower()

                if (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "high demand" in error_text
                ):
                    st.warning(
                        "⚠️ سرویس Gemini در حال حاضر ظرفیت کافی ندارد. "
                        "سیستم چند بار تلاش کرد و مدل جایگزین را هم بررسی کرد. "
                        "لطفاً چند لحظه بعد دوباره امتحان کنید."
                    )
                elif "429" in error_text or "resource exhausted" in error_text:
                    st.warning(
                        "⚠️ محدودیت موقت درخواست Gemini فعال شده است. "
                        "لطفاً کمی صبر کنید و دوباره سؤال را ارسال کنید."
                    )
                else:
                    st.error("❌ خطا در ارتباط با Gemini")
                    st.code(str(e))

# -------------------------------
# About
# -------------------------------

with tab5:

    st.subheader("ℹ About Project")

    st.markdown("""
### Toyota Production Planning Dashboard

This project was developed to optimize vehicle production using
Operations Research and Artificial Intelligence.

### Technologies

- Python
- Streamlit
- PuLP
- Pandas
- Google Gemini AI
- Genetic Algorithm

### Modules

✅ Linear Programming

✅ Genetic Algorithm

✅ AI Assistant

### Author

Aram Shafieha
""")

# -------------------------------
# Footer
# -------------------------------

st.divider()

left, right = st.columns([3,1])

with left:
    st.caption(
        "Toyota Production Planning Dashboard | Powered by Google Gemini"
    )

with right:
    st.caption("Version 1.0")
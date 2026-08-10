import streamlit as st
import subprocess
import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# -------------------------------
# Load Environment Variables
# -------------------------------

load_dotenv()

# API key: Streamlit Cloud Secrets first, local environment as fallback
gemini_api_key = os.getenv("GEMINI_API_KEY")

try:
    if not gemini_api_key and "GEMINI_API_KEY" in st.secrets:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

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

            # Direct REST call to Gemini.
            # This avoids Unicode/ASCII encoding problems that can occur
            # in some SDK/runtime combinations when the user enters Persian text.
            import time

            def ask_gemini_rest(prompt_text):
                # requests sends the JSON body as UTF-8 and avoids the
                # latin-1 header/body encoding path that caused the Cloud error.
                api_key = str(gemini_api_key).strip()

                # Gemini API keys are ASCII tokens. Remove accidental surrounding
                # whitespace but never transform the actual key.
                try:
                    api_key.encode("ascii")
                except UnicodeEncodeError:
                    raise RuntimeError(
                        "GEMINI_API_KEY contains non-ASCII characters. "
                        "Please replace it with the original Gemini API key."
                    )

                models = [
                    "gemini-2.5-flash",
                    "gemini-2.0-flash",
                ]

                last_error = None

                for model_name in models:
                    url = (
                        "https://generativelanguage.googleapis.com/"
                        f"v1beta/models/{model_name}:generateContent"
                    )

                    payload = {
                        "contents": [
                            {
                                "role": "user",
                                "parts": [{"text": str(prompt_text)}]
                            }
                        ],
                        "generationConfig": {
                            "temperature": 0.4,
                            "maxOutputTokens": 800
                        }
                    }

                    for attempt in range(3):
                        try:
                            response = requests.post(
                                url,
                                params={"key": api_key},
                                json=payload,
                                headers={
                                    "Content-Type": "application/json; charset=utf-8",
                                    "Accept": "application/json",
                                },
                                timeout=45,
                            )

                            if response.status_code in (429, 500, 502, 503, 504):
                                last_error = RuntimeError(
                                    f"Gemini HTTP {response.status_code}: "
                                    f"{response.text[:1000]}"
                                )
                                if attempt < 2:
                                    time.sleep(2 ** (attempt + 1))
                                    continue
                                break

                            if not response.ok:
                                raise RuntimeError(
                                    f"Gemini HTTP {response.status_code}: "
                                    f"{response.text[:2000]}"
                                )

                            data = response.json()
                            candidates = data.get("candidates", [])

                            if not candidates:
                                feedback = data.get("promptFeedback", {})
                                raise RuntimeError(
                                    "Gemini returned no candidate. "
                                    f"Prompt feedback: {feedback}"
                                )

                            parts = (
                                candidates[0]
                                .get("content", {})
                                .get("parts", [])
                            )

                            answer = "".join(
                                str(part.get("text", ""))
                                for part in parts
                                if part.get("text")
                            )

                            if not answer:
                                raise RuntimeError(
                                    "Gemini returned an empty response."
                                )

                            return answer, model_name

                        except requests.RequestException as e:
                            last_error = e
                            if attempt < 2:
                                time.sleep(2 ** (attempt + 1))
                                continue
                            break

                raise last_error or RuntimeError(
                    "Gemini did not return a response."
                )

            try:
                with st.spinner("Gemini is thinking..."):
                    answer, used_model = ask_gemini_rest(prompt)

                st.success("✅ Answer Ready!")
                st.write(answer)

                if used_model != "gemini-2.5-flash-lite":
                    st.caption(
                        f"ℹ️ پاسخ با مدل {used_model} تولید شد."
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
                        "سیستم چند بار تلاش کرد و مدل‌های جایگزین را هم بررسی کرد. "
                        "لطفاً چند لحظه بعد دوباره امتحان کنید."
                    )
                elif (
                    "429" in error_text
                    or "resource exhausted" in error_text
                    or "rate limit" in error_text
                ):
                    st.warning(
                        "⚠️ محدودیت موقت درخواست Gemini فعال شده است. "
                        "لطفاً کمی صبر کنید و دوباره سؤال را ارسال کنید."
                    )
                elif (
                    "ascii" in error_text
                    or "unicode" in error_text
                    or "latin-1" in error_text
                ):
                    st.error(
                        "❌ خطای encoding در ارتباط با Gemini. "
                        "این نسخه ارسال درخواست را با UTF-8 و requests انجام می‌دهد."
                    )
                    st.code(str(e))
                else:
                    st.error("❌ خطا در ارتباط با Gemini")
                    st.code(str(e))
                    st.info(
                        "اگر این خطا دوباره ظاهر شد، متن خطای بالا را برای بررسی دقیق نگه دارید."
                    )

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

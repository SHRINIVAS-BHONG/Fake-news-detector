import streamlit as st
from fact_checker import analyze_news
from ocr_utils import extract_text_from_image
from PIL import Image
import time

st.set_page_config(
    page_title="AI Fake News Detector",
    page_icon="🧠",
    layout="wide"
)

# -------------------------
# Styling
# -------------------------

st.markdown("""
<style>

.card {
    background:#111827;
    padding:22px;
    border-radius:12px;
    border:1px solid #1f2937;
    margin-bottom:25px;
}

.text-card {
    background:#0f172a;
    padding:18px;
    border-radius:10px;
    border:1px solid #374151;
    font-size:15px;
    line-height:1.7;
}

img {
    border-radius:10px;
    border:1px solid #374151;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Session History
# -------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Header
# -------------------------

st.title("🧠 AI Fake News Detector")
st.write("Verify news claims using AI and real web evidence.")

# -------------------------
# Text Input
# -------------------------

st.subheader("Enter News Claim")

news = st.text_area(
    "News Input",
    placeholder="Example: NASA confirms alien life on Mars",
    label_visibility="collapsed"
)

# -------------------------
# Upload Section
# -------------------------

st.subheader("Upload Screenshot")

uploaded_file = st.file_uploader(
    "Upload image containing a news claim",
    type=["png","jpg","jpeg"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    # Center column layout
    left, center, right = st.columns([1,2,1])

    with center:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("### 🖼 Uploaded Screenshot")

        st.image(
            image,
            use_column_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # OCR Extraction
        extracted_text = extract_text_from_image(image)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("### 📄 Extracted Text")

        st.markdown(
            f'<div class="text-card">{extracted_text}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        news = extracted_text

# -------------------------
# Analyze Button
# -------------------------

if st.button("Analyze Claim"):

    if news.strip() == "":
        st.warning("Please enter or upload a claim")

    else:

        with st.spinner("🔎 Searching evidence..."):
            result, evidence = analyze_news(news)

        fake_prob = ""
        verdict = ""
        explanation = ""
        sources = []

        for line in result.split("\n"):

            if "Fake Probability" in line:
                fake_prob = line.split(":")[-1].strip()

            elif "Verdict" in line:
                verdict = line.split(":")[-1].strip()

            elif "Explanation" in line:
                explanation = line.replace("Explanation:", "").strip()

            elif "Sources" in line:
                sources = line.replace("Sources:", "").split(",")

        prob = 0
        try:
            prob = int(fake_prob.replace("%",""))
        except:
            prob = 0

        st.session_state.history.append({
            "claim":news,
            "verdict":verdict,
            "prob":fake_prob
        })

        # -------------------------
        # AI Analysis
        # -------------------------

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("AI Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Fake Probability", fake_prob)
            st.progress(prob/100)

        with col2:

            if "fake" in verdict.lower():
                st.error(f"🚨 {verdict}")

            elif "misleading" in verdict.lower():
                st.warning(f"⚠️ {verdict}")

            else:
                st.success(f"✅ {verdict}")

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Explanation
        # -------------------------

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Explanation")

        box = st.empty()
        stream = ""

        for c in explanation:
            stream += c
            box.markdown(stream)
            time.sleep(0.01)

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Sources
        # -------------------------

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Sources")

        for s in sources:
            if s.strip():
                st.write("•", s.strip())

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Evidence
        # -------------------------

        st.subheader("Evidence")

        articles = evidence.split("Title:")

        for article in articles:

            if article.strip() == "":
                continue

            title = ""
            content = ""
            source = ""

            lines = article.split("\n")

            for line in lines:

                if "Content:" in line:
                    title = lines[0]

                if "Content:" in line:
                    content = line.replace("Content:", "").strip()

                if "Source:" in line:
                    source = line.replace("Source:", "").strip()

            st.markdown("---")

            st.markdown(f"### 📰 {title}")

            if content:
                st.write(content[:250] + "...")

            if source:
                st.markdown(f"[Read full article]({source})")

# -------------------------
# Sidebar History
# -------------------------

st.sidebar.title("🕘 History")

for item in reversed(st.session_state.history):

    st.sidebar.markdown(f"""
**{item['claim'][:40]}...**

Verdict: {item['verdict']}  
Probability: {item['prob']}

---
""")
import streamlit as st
from fact_checker import analyze_news
import time

st.set_page_config(
    page_title="AI Fake News Detector",
    page_icon="🧠",
    layout="wide"
)

# -------------------------
# Custom UI Styling
# -------------------------

st.markdown("""
<style>

.main-title {
    font-size:40px;
    font-weight:700;
    background: linear-gradient(90deg,#3b82f6,#22c55e);
    -webkit-background-clip:text;
    color:transparent;
}

.subtitle {
    color:#9ca3af;
    font-size:16px;
}

.card {
    background:#111827;
    padding:20px;
    border-radius:12px;
    border:1px solid #1f2937;
    margin-bottom:20px;
}

.news-card {
    background:#111827;
    padding:18px;
    border-radius:10px;
    border-left:4px solid #3b82f6;
    border:1px solid #1f2937;
    margin-bottom:15px;
}

.news-title {
    font-size:18px;
    font-weight:600;
}

.news-content {
    font-size:14px;
    color:#d1d5db;
    line-height:1.6;
}

.verdict-fake {
    color:#ef4444;
    font-weight:700;
    font-size:20px;
}

.verdict-real {
    color:#22c55e;
    font-weight:700;
    font-size:20px;
}

.verdict-misleading {
    color:#facc15;
    font-weight:700;
    font-size:20px;
}

/* Input Box Styling */

textarea {
    border-radius:12px !important;
    border:1px solid #374151 !important;
    padding:12px !important;
    font-size:16px !important;
    background-color:#111827 !important;
    color:#f9fafb !important;
}

textarea:focus {
    border:1px solid #3b82f6 !important;
    box-shadow:0 0 0 1px #3b82f6 !important;
}

textarea::placeholder {
    color:#9ca3af !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Session State (History)
# -------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Header
# -------------------------

st.markdown("<div class='main-title'>🧠 AI Fake News Detector</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze news claims using AI reasoning and real web evidence.</div>", unsafe_allow_html=True)

st.write("")

# -------------------------
# Input Section
# -------------------------

st.markdown("### 📰 Check a News Claim")

st.markdown(
"Paste a headline, tweet, or news message to analyze its credibility."
)

news = st.text_area(
    "Enter News",
    placeholder="Example: NASA confirms alien life on Mars",
    height=120,
    label_visibility="collapsed"
)

# Example suggestions

st.caption("Try examples:")

col1, col2, col3 = st.columns(3)

with col1:
    st.code("NASA confirms signs of life on Mars")

with col2:
    st.code("Scientists discover cure for cancer in mice")

with col3:
    st.code("India bans TikTok again in 2025")

# -------------------------
# Analyze Button
# -------------------------

if st.button("Analyze Claim"):

    if news.strip() == "":
        st.warning("Please enter text")

    else:

        with st.spinner("🔎 Extracting claim..."):
            time.sleep(0.5)

        with st.spinner("🌐 Searching evidence..."):
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

        # Save to history
        st.session_state.history.append({
            "claim":news,
            "verdict":verdict,
            "prob":fake_prob
        })

        # -------------------------
        # AI Analysis
        # -------------------------

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("AI Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.metric("Fake Probability", fake_prob)
            st.progress(prob/100)

        with col2:

            if "fake" in verdict.lower():
                st.markdown(f"<div class='verdict-fake'>🚨 {verdict}</div>", unsafe_allow_html=True)

            elif "misleading" in verdict.lower():
                st.markdown(f"<div class='verdict-misleading'>⚠️ {verdict}</div>", unsafe_allow_html=True)

            else:
                st.markdown(f"<div class='verdict-real'>✅ {verdict}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # Explanation
        # -------------------------

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("Explanation")

        text_box = st.empty()
        stream=""

        for c in explanation:
            stream += c
            text_box.markdown(stream)
            time.sleep(0.01)

        st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # Sources
        # -------------------------

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("Sources")

        for s in sources:
            if s.strip():
                st.write("•",s.strip())

        st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # Evidence Section
        # -------------------------

        st.subheader("📰 Evidence from Web")

        articles = evidence.split("Title:")

        for article in articles:

            if article.strip()=="":
                continue

            title=""
            content=""
            source=""

            lines = article.split("\n")

            for line in lines:

                if "Content:" in line:
                    title = lines[0]

                if "Content:" in line:
                    content = line.replace("Content:","").strip()

                if "Source:" in line:
                    source = line.replace("Source:","").strip()

            st.markdown("<div class='news-card'>", unsafe_allow_html=True)

            st.markdown(f"<div class='news-title'>📰 {title}</div>", unsafe_allow_html=True)

            if content:
                st.markdown(f"<div class='news-content'>{content[:250]}...</div>", unsafe_allow_html=True)

            if source:
                st.markdown(f"[Read full article]({source})")

            st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Sidebar History
# -------------------------

st.sidebar.title("🕘 Previous Checks")

if len(st.session_state.history)==0:

    st.sidebar.write("No checks yet")

else:

    for item in reversed(st.session_state.history):

        icon="❌"

        if "real" in item["verdict"].lower():
            icon="✅"

        elif "misleading" in item["verdict"].lower():
            icon="⚠️"

        st.sidebar.markdown(f"""
**{icon} {item['claim'][:45]}...**

Verdict: {item['verdict']}  
Probability: {item['prob']}

---
""")
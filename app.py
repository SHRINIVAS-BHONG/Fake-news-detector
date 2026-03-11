import streamlit as st
from fact_checker import analyze_news

st.set_page_config(
    page_title="AI Fake News Detector",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI Fake News Detector")
st.write("Paste a news headline or message and the system will analyze whether it may be fake.")

news = st.text_area("Enter a news headline or message")


if st.button("Analyze"):

    if news.strip() == "":
        st.warning("Please enter text")
    else:

        with st.spinner("Checking facts..."):
            result, evidence = analyze_news(news)

        # -----------------------------
        # Parse LLM Output (robust)
        # -----------------------------

        fake_prob = ""
        verdict = ""
        explanation_text = ""
        sources = []

        lines = result.split("\n")

        for line in lines:

            if "Fake Probability" in line:
                fake_prob = line.split(":")[-1].strip()

            elif "Verdict" in line:
                verdict = line.split(":")[-1].strip()

            elif "Explanation" in line:
                explanation_text = line.replace("Explanation:", "").strip()

            elif "Sources" in line:
                source_line = line.replace("Sources:", "").strip()
                sources = [s.strip() for s in source_line.split(",")]

        # -----------------------------
        # Display AI Analysis
        # -----------------------------

        st.subheader("🧠 AI Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Fake Probability", fake_prob)

        with col2:
            st.metric("Verdict", verdict)

        # -----------------------------
        # Explanation
        # -----------------------------

        st.subheader("📖 Explanation")

        if explanation_text:
            st.markdown(
                f"""
                <div style="font-size:16px; line-height:1.8">
                {explanation_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("No explanation generated.")

        # -----------------------------
        # Sources
        # -----------------------------

        st.subheader("🔗 Sources")

        if sources:
            for s in sources:
                if s:
                    st.write("•", s)
        else:
            st.write("No sources extracted.")

        # -----------------------------
        # Evidence Section
        # -----------------------------

        with st.expander("🔎 Evidence from Web"):

            st.markdown("### Articles used for fact-checking")

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
                        title = lines[0].strip()

                    if "Content:" in line:
                        content = line.replace("Content:", "").strip()

                    if "Source:" in line:
                        source = line.replace("Source:", "").strip()

                st.markdown("---")

                st.markdown(f"### 📰 {title}")

                if content:
                    short_text = content[:350] + "..."
                    st.markdown(
                        f"""
                        <p style="font-size:15px; line-height:1.7">
                        {short_text}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

                if source:
                    st.markdown(f"[Read full article]({source})")
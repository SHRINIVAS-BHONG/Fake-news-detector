import streamlit as st
from news_analyzer import analyze_news

st.set_page_config(page_title="AI Fake News Detector")

st.title("📰 AI Fake News Detector")

st.write("Paste a news headline or message to check if it might be fake.")

news_input = st.text_area("Enter News Text")

if st.button("Analyze"):

    if news_input.strip() == "":
        st.warning("Please enter news text")

    else:

        with st.spinner("Checking sources and analyzing..."):

            result = analyze_news(news_input)

            st.subheader("Result")

            st.write(result)
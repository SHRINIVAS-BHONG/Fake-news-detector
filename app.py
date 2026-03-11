import streamlit as st
from news_analyzer import analyze_news

st.set_page_config(page_title="AI Fake News Detector")

st.title("Fake News Detector")

news_input = st.text_area("Enter news article")

if st.button("Analyze"):

    with st.spinner("Checking sources..."):
        result = analyze_news(news_input)

    st.subheader("Verdict")
    st.write(result["verdict"])

    st.subheader("Explanation")
    st.write(result["explanation"])

    st.subheader("Confidence")
    st.write(result["confidence"])
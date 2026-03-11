import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

from prompt_template import fake_news_prompt
from parser import parser

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

search = TavilySearch(max_results=5)

chain = fake_news_prompt | llm | parser


def analyze_news(news_text):

    search_results = search.invoke({"query": news_text})

    sources = ""
    if "results" in search_results:
        for r in search_results["results"]:
            sources += r["content"] + "\n"

    result = chain.invoke({
        "news": news_text,
        "sources": sources
    })

    return result
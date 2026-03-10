import os
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chains import LLMChain
from langchain_huggingface import HuggingFaceEndpoint

from prompt_template import fake_news_prompt

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    temperature=0.2,
    max_new_tokens=512
)

search = TavilySearchResults(max_results=3)


def analyze_news(news_text):

    search_results = search.invoke({"query": news_text})

    sources = ""
    for r in search_results:
        sources += r["content"] + "\n"

    chain = LLMChain(
        llm=llm,
        prompt=fake_news_prompt
    )

    result = chain.invoke({
        "news": news_text,
        "sources": sources
    })

    return result["text"]
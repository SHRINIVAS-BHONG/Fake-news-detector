from groq import Groq
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_news(query):

    results = tavily.search(query=query, max_results=5)

    evidence = ""

    for r in results["results"]:
        evidence += f"Title: {r['title']}\n"
        evidence += f"Content: {r['content']}\n"
        evidence += f"Source: {r['url']}\n\n"

    return evidence


def analyze_news(news_text):

    evidence = search_news(news_text)

    prompt = f"""
You are an expert fact checker.

Claim:
{news_text}

Evidence:
{evidence}

Tasks:
1. Determine if the claim is fake or real.
2. Give fake probability (0-100%).
3. Explain reasoning.
4. Mention credible sources.

Return format:

Fake Probability:
Verdict:
Explanation:
Sources:
"""

    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    return result, evidence
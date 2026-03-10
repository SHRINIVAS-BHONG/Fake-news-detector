from langchain.prompts import PromptTemplate

fake_news_prompt = PromptTemplate(
    input_variables=["news", "sources"],
    template="""
You are an AI fact-checking assistant.

Analyze the following news headline or message.

News:
{news}

Supporting information from web sources:
{sources}

Tasks:
1. Determine if the news is Real, Fake, or Misleading
2. Provide a fake probability score (0-100)
3. Give a short explanation

Return JSON format:

{{
"verdict": "",
"fake_probability": "",
"reason": ""
}}
"""
)
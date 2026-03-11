from langchain_core.prompts import ChatPromptTemplate
from parser import parser

prompt = ChatPromptTemplate.from_template(
"""
You are a professional fact-checker.

Analyze the news and determine if it is FAKE or REAL.

NEWS:
{news}

WEB SOURCES:
{sources}

Return JSON.

{format_instructions}
"""
)

fake_news_prompt = prompt.partial(
    format_instructions=parser.get_format_instructions()
)
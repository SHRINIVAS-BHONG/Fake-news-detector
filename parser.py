from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


class NewsResult(BaseModel):
    verdict: str = Field(description="Fake or Real")
    explanation: str = Field(description="Reasoning")
    confidence: str = Field(description="Confidence percentage")


parser = JsonOutputParser(pydantic_object=NewsResult)
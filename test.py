from google import genai
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# create client
client = genai.Client(api_key=api_key)

# generate response
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain fake news detection in simple terms"
)

print(response.text)
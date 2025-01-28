from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("API_KEY")

today = date.today()
formatted_date = today.strftime("%Y-%m-%d")

client = genai.Client(api_key=API_KEY)
model_id = "gemini-2.0-flash-exp"

google_search_tool = Tool(
    google_search=GoogleSearch()
)

response = client.models.generate_content(
    model=model_id,
    contents="Find the latest articles about DeepSeek " + formatted_date + ", and summarize the 5 latest articles.",
    # The formatted_date is included in the contents string to ensure the search is for the latest articles as of today.
    config=GenerateContentConfig(
        tools=[google_search_tool],
        response_modalities=["TEXT"]
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)

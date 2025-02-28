from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from datetime import date

app = Flask(__name__)

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)
model_id = "gemini-2.0-flash-exp"
google_search_tool = Tool(google_search=GoogleSearch())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        response = client.models.generate_content(
            model=model_id,
            contents=query,
            config=GenerateContentConfig(
                tools=[google_search_tool],
                response_modalities=["TEXT"]
            )
        )
        result = "\n".join([part.text for part in response.candidates[0].content.parts])
        return render_template('index.html', query=query, result=result)
    return render_template('index.html', query='', result='')

if __name__ == '__main__':
    app.run(debug=True)

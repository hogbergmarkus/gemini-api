from flask import Flask, request, render_template, flash
import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

app = Flask(__name__)
app.secret_key = os.urandom(24) # For flash messages.

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)
model_id = "gemini-2.0-flash-exp"
google_search_tool = Tool(google_search=GoogleSearch())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=query,
                config=GenerateContentConfig(
                    tools=[google_search_tool],
                    response_modalities=["TEXT"]
                )
            )
            result = "\n\n".join([f"{part.text.replace('<p>', '').replace('</p>', '').replace('**', '')}" for part in response.candidates[0].content.parts])
            return render_template('index.html', query=query, result=result)
        except Exception as e:
            flash(f"An error occurred: {e}") # Display the error to the user
            return render_template('index.html', query=query, result="") # Show empty result
    return render_template('index.html', query='', result='')

if __name__ == '__main__':
    app.run(debug=True)

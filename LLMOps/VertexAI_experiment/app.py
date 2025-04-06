from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.language_models import ChatModel

load_dotenv()

app = Flask(__name__)

# Load environment variables
project_id = os.getenv("project_id")
region = os.getenv("region")

# Initialize Vertex AI
vertexai.init(project=project_id, location=region)

# Try loading Gemini model, fall back to chat-bison if necessary
model = None
gemini_available = True

try:
    model = GenerativeModel("gemini-1.5-pro-002")
except Exception as e:
    print(f"⚠️ Gemini model load failed: {e}")
    gemini_available = False
    try:
        # fallback model
        chat_model = ChatModel.from_pretrained("chat-bison")
        chat = chat_model.start_chat()
    except Exception as fallback_e:
        print(f"❌ Failed to load fallback model: {fallback_e}")

@app.route("/")
def home():
    return render_template("index.html")  # Make sure you have an index.html template

@app.route('/gemini', methods=['GET', 'POST'])
def vertex_ai_route():
    user_input = ""

    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form.get('user_input')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        if gemini_available and model:
            responses = model.generate_content(user_input, stream=True)
            res = [resp.candidates[0].content.parts[0].text for resp in responses]
            final_res = "".join(res)
        else:
            response = chat.send_message(user_input)
            final_res = response.text

        return jsonify({"content": final_res})

    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return jsonify({"error": "Failed to generate response", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

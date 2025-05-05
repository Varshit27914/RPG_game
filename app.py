from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import openai

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# OpenAI API setup
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize game state
messages = [{"role": "system", "content": "You're a helpful assistant in an RPG game."}]

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_msg = data.get("message")

        if not user_msg:
            return jsonify({"error": "No message provided"}), 400

        messages.append({"role": "user", "content": user_msg})

        # Get OpenAI completion
        completion = openai.ChatCompletion.create(
            model="gpt-4-mini",  # You can use "gpt-3.5-turbo" for a more cost-efficient model
            messages=messages
        )

        response = completion.choices[0].message['content']
        messages.append({"role": "assistant", "content": response})

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

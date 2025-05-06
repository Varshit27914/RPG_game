from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# OpenAI API setup
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize conversation state
messages = [{"role": "system", "content": (
    "You're an AI Dungeon Master for a text-based RPG game. "
    "When the player sends an action or selects an option, respond with a JSON object containing:\n"
    "- story_text: describing what happens\n"
    "- options: 3-4 action choices for the player\n"
    "- inventory: a list of current inventory items\n"
    "- money: total money the player has\n"
    "- player_stats: { health, mana } values\n"
    "- missions: list of active missions (only updated by NPCs, not by player actions)\n\n"
    "Example response:\n"
    "{\n"
    "  \"story_text\": \"You enter the ancient cave...\",\n"
    "  \"options\": [\"Light a torch\", \"Proceed in the dark\", \"Call out\"],\n"
    "  \"inventory\": [\"Sword\", \"Potion\"],\n"
    "  \"money\": 120,\n"
    "  \"player_stats\": {\"health\": 90, \"mana\": 40},\n"
    "  \"missions\": [\"Find the ancient artifact\"]\n"
    "}\n"
    "Respond ONLY in JSON format."
)}]

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

        # Get OpenAI chat completion
        completion = openai.ChatCompletion.create(
            model="gpt-4o",  # or "gpt-4-mini" if you prefer
            messages=messages,
            temperature=0.7
        )

        response_content = completion.choices[0].message['content']

        # Optional: log for debugging
        print("AI Response:", response_content)

        # Append assistant message
        messages.append({"role": "assistant", "content": response_content})

        return jsonify({"response": response_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

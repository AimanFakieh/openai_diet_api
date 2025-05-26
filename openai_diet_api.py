from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Use new OpenAI Client interface
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/generate_diet", methods=["POST"])
def generate_diet():
    data = request.get_json()
    fitness_goal = data.get("fitness_goal")
    gender = data.get("gender")
    weight = data.get("weight")
    motivation_type = data.get("motivation_type")
    extra_input = data.get("extra_input", "")

    prompt = (
        f"Create a simple one-day diet plan for a {gender} weighing {weight} kg, "
        f"aiming for {fitness_goal}. Their motivation is {motivation_type}. "
        f"Additional notes: {extra_input}. "
        "List only breakfast, lunch, and dinner. Add portion sizes in grams. Be concise."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful nutritionist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        result = response.choices[0].message.content
        return jsonify({"diet_plan": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

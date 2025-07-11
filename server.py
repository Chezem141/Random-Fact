from flask import Flask, jsonify
from openai import OpenAI
import random

app = Flask(__name__, template_folder='./templates', static_folder='./static')

@app.route('/')
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.route('/get_fact')
def get_fact():

    with open("../.venv/OpenRouterKey", "r", encoding="utf-8") as f:
        api_key = f.read().strip()

    randomTheme = [
        "из истории",
        "из астрономии",
        "из физики",
        "из спорта",
        "из географии",
        "из биологии",
        "из науки",
        "про какую-нибудь страну",
        "из природы",
        "из мира животных",
        "из автоспорта",
        "из велоспорта",
        "про технологии"
    ]

    message = "Расскажи один любой факт или теорию " + random.choice(randomTheme)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    answer = completion.choices[0].message.content
    print(answer)
    return jsonify({"fact": answer})


if __name__ == '__main__':
    app.run(debug=True)
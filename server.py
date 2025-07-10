from flask import Flask, jsonify
import re
from gigachat import GigaChat
from gigachat.exceptions import GigaChatException

app = Flask(__name__, template_folder='./templates', static_folder='./static')

models = {
    "Max": "GigaChat-2-Max",
    "Pro": "GigaChat-2-Pro",
    "Lite": "GigaChat-2"

}

def ask_gigachat(question: str, api_key: str, model: str) -> str:
    """Отправляет запрос в GigaChat и возвращает ответ."""
    try:
        giga = GigaChat(
            credentials=api_key,
            model=model,
            verify_ssl_certs=False
        )

        response = giga.chat(question)
        return response.choices[0].message.content

    except GigaChatException as e:
        return f"Ошибка GigaChat: {e}"
    except Exception as e:
        return f"Общая ошибка: {e}"


def check_balance(api_key: str) -> str:
    try:
        giga = GigaChat(
            credentials=api_key,
            verify_ssl_certs=False
        )

        balance = str(giga.get_balance()).split("balance=", 1)[-1].strip()

        match = re.search(r"GigaChat-Pro', value=(\d+\.\d+)", balance)
        if match:
            pro_value = float(match.group(1))

        match = re.search(r"GigaChat-Max', value=(\d+\.\d+)", balance)
        if match:
            max_value = float(match.group(1))

        match = re.search(r"GigaChat', value=(\d+\.\d+)", balance)
        if match:
            lite_value = float(match.group(1))

        result = {
            "Max": max_value,
            "Pro": pro_value,
            "Lite": lite_value
        }

        def get_result():
            print(result)
        check_balance.result = get_result

        if result['Lite'] >= 1000:
            return 'Lite'
        elif result['Pro'] >= 1000:
            return 'Pro'
        elif result['Max'] >= 1000:
            return 'Max'
        else: return 'No more tokens'

    except GigaChatException as e:
        return f"Ошибка GigaChat: {e}"
    except Exception as e:
        return f"Общая ошибка: {e}"


@app.route('/')
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.route('/get_fact')
def get_fact():
    with open("../.venv/Authorization Key", "r", encoding="utf-8") as f:
        api_key = f.read().strip()

    model = check_balance(api_key)
    if model == 'No more tokens':
        return jsonify({"error": "Лимит запросов исчерпан"})

    question = "Расскажи случайный мировой факт"
    answer = ask_gigachat(question, api_key, models[model])
    return jsonify({"fact": answer})


if __name__ == '__main__':
    app.run(debug=True)
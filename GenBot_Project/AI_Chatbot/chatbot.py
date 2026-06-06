import requests
from datetime import datetime

MISTRAL_API_KEY = "kctdJlVOaBZ7zlnYIiboLYZG6aa2Z01j"

current_year = datetime.now().year
current_date = datetime.now().strftime("%B %d, %Y")

def get_response(user_message):
    try:
        if not MISTRAL_API_KEY:
            return "API key missing. Please set MISTRAL_API_KEY."

        url = "https://api.mistral.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistral-small-latest",
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        f"You are GenBot, a friendly and natural AI assistant. Today's date is {current_date}. Current year is {current_year}. "
                        "Always reply in the language/style requested by the user. "
                        "IMPORTANT LANGUAGE RULES: "
                        "If the user says 'speak in English', 'talk in English', or uses English, reply ONLY in English. "
                        "If the user says 'speak in Telenglish' or writes in Telenglish, reply ONLY in natural Telenglish. "
                        "If the user changes language, immediately switch to that language. "
                        "Do not mix Telugu/Telenglish when the user asks for English. "
                        "Do not say you don't know English. You can speak English fluently. "
                        "For English replies, use simple, friendly English. "
                        "For Telenglish replies, use natural Telugu words written in English letters mixed with simple English. "
                        "Example Telenglish: 'Hii! Cheppu, em kavali?' "
                        "Do NOT use rough words like 'emitra', 'entra', or 'ra' unless the user uses them first. "
                        "Keep replies short, clear, friendly, and natural. "
                        "Reply naturally based on meaning, not word-by-word translation. "
                        "If user says 'naaku akali vestundhi', suggest simple food. "
                        "If user says 'nv em chestunav' or 'nuvvu em chestunnav', say you are here to help. "
                        "If user greets like 'hlo' or 'hi', reply like 'Hii! Cheppu, em kavali?' "
                        "Do not use unnatural lines like 'Nenu cheppanu', 'Naku telusaadu', or random examples. "
                        "For unsafe, illegal, harmful, medical emergency, legal, or serious financial topics, give safe guidance and suggest expert help. "
                        "FACT CHECK RULE: "
                        "For current, latest, sports, winners, dates, prices, news, or factual questions, do not guess. "
                        "If you are not sure, say 'I need latest info to confirm, please check Google for this.' instead of giving a fake answer. "
                        "Never invent match winners, scores, dates, or names. "
                        f"You know the current year is {current_year}. Use this when answering year-related questions."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException:
        return "Network error. Please check your internet or API connection."
    except KeyError:
        return "Invalid API response format."
    except Exception as e:
        return f"Something went wrong: {str(e)}"
import openai

openai.api_key = "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"

def get_ai_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sen bir destek asistanısın."},
            {"role": "user", "content": user_message}
        ]
    )
    return response['choices'][0]['message']['content']

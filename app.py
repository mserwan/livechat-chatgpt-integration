from flask import Flask, request, jsonify
from openai_utils import get_ai_response
from livechat_utils import send_livechat_message

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    LiveChat webhook'undan gelen isteği işler:
    1. Kullanıcı mesajını alır.
    2. OpenAI API'ye gönderip yanıt alır.
    3. Yanıtı LiveChat API'ye gönderir.
    """
    try:
        # Gelen JSON verisini al
        data = request.json
        print("Gelen veri:", data)

        # Webhook'tan gelen mesajı işle
        chat_id = data.get("chat", {}).get("id", None)
        messages = data.get("chat", {}).get("messages", [])
        
        if not chat_id:
            raise ValueError("Geçersiz chat_id: chat_id bulunamadı.")

        # Kullanıcı mesajını al
        if messages and len(messages) > 0:
            user_message = messages[-1].get("text", "Mesaj bulunamadı.")
        else:
            user_message = "Mesaj bulunamadı."

        print(f"Kullanıcı mesajı: {user_message}, Chat ID: {chat_id}")

        # OpenAI API'den yanıt al
        ai_reply = get_ai_response(user_message)
        print(f"OpenAI Yanıtı: {ai_reply}")

        # LiveChat API'ye yanıt gönder
        success = send_livechat_message(chat_id, ai_reply)
        if success:
            print("Yanıt LiveChat'e başarıyla gönderildi.")
            return jsonify({"status": "success"}), 200
        else:
            print("Yanıt gönderimi sırasında hata oluştu.")
            return jsonify({"status": "error", "details": "LiveChat mesaj gönderimi başarısız"}), 500

    except Exception as e:
        print("Hata:", str(e))
        return jsonify({"status": "error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

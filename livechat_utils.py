import requests
import json

# LiveChat API bilgileri
BASE64_TOKEN = "MGQzMmY2MmUtZDI3My00OGY4LWFkMzktNTNiZWFiOWFmYjRiOmRhbDo0TnBoNnp1ZXJ0TFU0emRhT2NwNHk4eFhhM0U="
LIVECHAT_API_URL = "https://api.livechatinc.com/v3.3/agent/action/send_event"
LIST_THREADS_URL = "https://api.livechatinc.com/v3.3/agent/action/list_threads"

# HTTP yetkilendirme başlıkları
headers = {
    "Authorization": f"Basic {BASE64_TOKEN}",
    "Content-Type": "application/json"
}

def list_active_chats():
    """
    LiveChat API'den aktif sohbetleri listele.
    """
    payload = {
        "filters": {
            "status": "active"
        }
    }
    try:
        response = requests.post(LIST_THREADS_URL, headers=headers, json=payload)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        threads = response.json().get("threads", [])
        return threads
    except requests.exceptions.RequestException as e:
        print("Sohbet listeleme sırasında hata:", str(e))
        return []

def send_livechat_message(chat_id, ai_reply):
    """
    Belirtilen chat_id'ye OpenAI yanıtını gönder.
    Eğer chat_id geçersizse, aktif sohbetlerden yeni bir chat_id alır.
    """
    payload = {
        "chat_id": chat_id,
        "event": {
            "type": "message",
            "text": ai_reply
        }
    }

    print(f"İstek Gövdesi: {payload}")  # İstek gövdesini yazdır

    try:
        response = requests.post(LIVECHAT_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # HTTP hatalarını kontrol et

        print(f"API Yanıtı: {response.status_code}")  # API yanıtını yazdır
        print(f"API Yanıtı İçeriği: {response.text}")  # API yanıtını yazdır

        if response.status_code == 200:
            return True
        elif response.status_code == 422 and "Invalid `chat_id`" in response.text:
            print("Geçersiz chat_id, aktif sohbetlerden yeni bir chat_id alınıyor...")
            active_chats = list_active_chats()
            if active_chats:
                new_chat_id = active_chats[0]['id']
                print(f"Yeni chat_id: {new_chat_id}")
                return send_livechat_message(new_chat_id, ai_reply)  # Fonksiyonu yeni chat_id ile tekrar çağır
            else:
                print("Aktif sohbet bulunamadı.")
                return False
        else:
            print(f"LiveChat Hatası: {response.status_code}, {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print("Mesaj gönderimi sırasında hata:", str(e))
        print(f"Hata içeriği: {e.response.text}")  # Hata içeriğini yazdır
        return False

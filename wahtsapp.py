from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


ACCESS_TOKEN = "EAAVau3ZAHEmoBO47nmrf1rj0FfabA6SoHKTiAbGDEHAimQdBeuHOKiCAemZCKGah3fJU7cpzNPMVjqFcs6t2L3rzNi8rIfZA2kDKj5jR1ZBGz90mS872XuAIqjTuT2ZBtCiI0B6yeuQH785E4aUMfTkvjnV2DZChMwOuvCxzpYl00snPXFLY4NZBY7aAedmXHzU6AZDZD"
PHONE_NUMBER_ID = "526125860582825"
CHATBOT_API_URL = "https://jec-chatbot.goodwish.com.np/assistant/query/"

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
       
        VERIFY_TOKEN = "12345"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "Forbidden", 403

    if request.method == "POST":
      
        data = request.json
        print("Incoming webhook:", data)

        if data.get("entry"):
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    if change.get("value"):
                        message = change["value"].get("messages", [{}])[0]
                        sender = message.get("from")  
                        message_text = message.get("text", {}).get("body", "")  

                        print(f"Message from {sender}: {message_text}")

                       
                        chatbot_response = query_chatbot(message_text)

                  
                        if chatbot_response:
                            send_whatsapp_message(sender, chatbot_response)

        return jsonify({"status": "received"}), 200

def query_chatbot(query):
    """Query the chatbot API and return the response."""
    payload = {"query": query}
    try:
        response = requests.post(CHATBOT_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from chatbot.")
        else:
            print(f"Chatbot error: {response.status_code}, {response.text}")
            return "Error communicating with the chatbot."
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "Error communicating with the chatbot."

def send_whatsapp_message(recipient, message_text):
    """Send a message via WhatsApp's Cloud API."""
    url = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": message_text}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)

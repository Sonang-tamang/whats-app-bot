from flask import Flask, request, jsonify

app = Flask(__name__)

ACCESS_TOKEN = "EAAVau3ZAHEmoBOZCpmK11JBxisFRBxKy41YWyIRpbX4uFraDTihQBRJ6mmHmLzZARcCW4hsWb42naMyjHzQmrDTFaSDt3l4gb5mglzgqeOeN4BgA0gNn58PAIZAZAllvBrMjRIKJwQDntUXMpmksspG13xZCwFKoNbycFkQZAzJSZCn1m2jyWUfeyksYtCQZCqxovIbtHDPHZBqKvyplj2zCtNqs9UFsU6ZBOUT0GkZD"
PHONE_NUMBER_ID = "526125860582825"  # From Meta Developer Console
CHATBOT_API_URL = "https://jec-chatbot.goodwish.com.np/assistant/query/"

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        # Verification challenge for WhatsApp
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
        # Handle incoming messages
        data = request.json
        print("Incoming webhook:", data)

        # Extract message details
        if data.get("entry"):
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    if change.get("value"):
                        message = change["value"].get("messages", [{}])[0]
                        sender = message.get("from")  # Sender's phone number
                        message_text = message.get("text", {}).get("body", "")  # Message text
                        
                        print(f"Message from {sender}: {message_text}")

                        

                        # Optional: Send the message to your chatbot API here
                        # response = requests.post("http://your-chatbot-api-endpoint", json={"message": message_text})
                        # print("Chatbot response:", response.json())

        return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)

from flask import Flask, request, jsonify
import requests
import json  # For formatting JSON in debug logs

app = Flask(__name__)

# Replace with your actual credentials
VERIFY_TOKEN = "12345"
ACCESS_TOKEN = 'EAAVau3ZAHEmoBO3lSQt6L1wYhhEEQzcpK8BvZC3UcXjx6T4KHGljBxcttDsOWpds1hKY2ZBX6np3D6dEFZBZADjk0B7glM6uJZBLthg14OdpIM2MZAHsSwhmuL6Ad4kZBnllzKUkcEVHfwrv3jUsZATbF3b19cZC5XhsUlnPgIG8h8PAwKo1hAh2p3wFlAmk0AjO95DyBl0tVh2ao9ASh8ZAZBWMmPrFbPolcq1rOu6dOwZDZD'
PHONE_NUMBER_ID = '+9779805134917'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Debug log for verification requests
        print("[DEBUG] Received GET request for webhook verification.")
        
        hub_mode = request.args.get('hub.mode')
        hub_challenge = request.args.get('hub.challenge')
        hub_verify_token = request.args.get('hub.verify_token')

        print(f"[DEBUG] hub.mode: {hub_mode}, hub.challenge: {hub_challenge}, hub.verify_token: {hub_verify_token}")

        if hub_mode == 'subscribe' and hub_verify_token == VERIFY_TOKEN:
            print("[DEBUG] Verification successful.")
            return hub_challenge, 200
        else:
            print("[DEBUG] Verification failed. Invalid verify token.")
            return 'Verification failed', 403

    elif request.method == 'POST':
        print("[DEBUG] Received POST request with potential webhook data.")
        try:
            data = request.get_json()
            print(f"[DEBUG] Incoming webhook data: {json.dumps(data, indent=4)}")  # Pretty-print JSON

            # Extracting message payload
            entry = data.get("entry", [])
            if not entry:
                print("[DEBUG] No 'entry' in webhook payload.")
                return jsonify({"status": "No entry found in payload"}), 200

            changes = entry[0].get("changes", [])
            if not changes:
                print("[DEBUG] No 'changes' in entry.")
                return jsonify({"status": "No changes found in payload"}), 200

            messages = changes[0].get("value", {}).get("messages", [])
            if not messages:
                print("[DEBUG] No 'messages' found in changes.")
                return jsonify({"status": "No messages found in payload"}), 200

            # Process the first message
            message = messages[0]
            sender = message.get('from')  # Sender's phone number
            text = message.get('text', {}).get('body', '')  # Message text

            print(f"[DEBUG] Message from {sender}: {text}")

            # Send a response back to the sender
            send_message(sender, "Hello! How can I assist you today?")
            print("[DEBUG] Response sent to the sender.")

            return jsonify({"status": "Message received"}), 200

        except Exception as e:
            print(f"[ERROR] Exception occurred while handling POST request: {e}")
            return jsonify({"status": "Error occurred"}), 500

# Function to send a message via WhatsApp API
def send_message(recipient_id, message_text):
    print(f"[DEBUG] Preparing to send message to {recipient_id}: {message_text}")
    url = f'https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages'
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "text": {"body": message_text}
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"[DEBUG] WhatsApp API response: {response.status_code} {response.text}")

        if response.status_code == 200:
            print(f"[DEBUG] Message successfully sent to {recipient_id}.")
        else:
            print(f"[ERROR] Failed to send message. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception occurred while sending message: {e}")

if __name__ == '__main__':
    print("[DEBUG] Starting Flask server...")
    app.run(port=5000, debug=True)

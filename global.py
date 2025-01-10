from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


VERIFY_TOKEN = "12345"
CHATBOT_API_URL = "https://jec-chatbot.goodwish.com.np/assistant/query/"
ACCESS_TOKEN = 'EAAS7RHRiHFkBOZCrtda0EQv7IHNHYmiuWZCZCnCtR82QYUZB4TxbNBpaj7ZAZAZCrgnzVBAfFwKpZCW2tUFUg2pO3ZBmbvtyZA5VAwbPP8sQVbHZCq4Un3aS5Y8SD4eesna6ra1CNjEavZCVPOEOXQQYFfnqCm4lU91O93NJbFNUqRqGuG4L5CmUL442qaroU5dpTmEY5W6Nnotmpksg3ZBBOL3ScSW0T'


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Verify the webhook during the setup phase.
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("Webhook verified!")
        return challenge, 200
    else:
        return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Handle incoming Instagram messages and print them to the console.
    """
    data = request.get_json()

    # Filter out echo messages for debugging
    filtered_entries = []
    if 'entry' in data:
        for entry in data['entry']:
            if 'messaging' in entry:
                entry['messaging'] = [
                    msg for msg in entry['messaging']
                    if not msg['message'].get('is_echo', False)
                ]
                filtered_entries.append(entry)

    print("Webhook received:", {"object": data["object"], "entry": filtered_entries})

    if 'entry' in data:
        for entry in data['entry']:
            if 'messaging' in entry:
                for messaging_event in entry['messaging']:
                    # Ignore echo messages
                    if messaging_event['message'].get('is_echo', False):
                        continue

                    if 'message' in messaging_event:
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text', 'No text message')

                        # Print sender and message
                        print(f"Message from {sender_id}: {message_text}")

    return jsonify({'status': 'received'}), 200

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




if __name__ == '__main__':
    app.run(port=5000, debug=True)

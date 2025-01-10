from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

processed_events = {}

# Configuration
VERIFY_TOKEN = "12345"
CHATBOT_API_URL = "https://jec-chatbot.goodwish.com.np/assistant/query/"
ACCESS_TOKEN = 'EAAS7RHRiHFkBOZBQU922yDy3TbOGuHsULf9DJSqJNFgUqi8TBkOxSawWcSFm4UgQ3z4oJI8JZAXfHFI2qpbaczu52O8TYUz7uXgy4MjUEM55i07W3ZBW1nOuwa9sLUkuKRXiRIoeC4wm3q9sZA3UgevZAWzf15GSLEttDZA6ml1P9BK9v2QA7cKDJJbFj5wo23nU0DEU5ZBNOdCkCrOBn0cZBc1k'

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
    Handle incoming Instagram messages and respond via the chatbot API.
    """
    data = request.get_json()
    if 'entry' in data:
        for entry in data['entry']:
            if 'messaging' in entry:
                for messaging_event in entry['messaging']:
                    # Check if the 'message' key exists
                    if 'message' in messaging_event:
                        # Ignore echo messages
                        if messaging_event['message'].get('is_echo', False):
                            continue

                        # Process user messages
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text', 'No text message')

                        # Get the unique event ID (Facebook provides this in 'message_id' or 'event_id')
                        event_id = messaging_event['message'].get('mid', None)

                        if event_id in processed_events:
                            print(f"Ignoring duplicate event with ID {event_id} from {sender_id}")
                            continue  # Skip sending a response for this event

                        # Mark this event as processed
                        processed_events[event_id] = time.time()

                        # Print the received message for logging
                        print(f"Message from {sender_id}: {message_text}")

                        # Query chatbot and send response
                        chatbot_response = query_chatbot(message_text)
                        send_instagram_message(ACCESS_TOKEN, sender_id, chatbot_response)

    return jsonify({'status': 'received'}), 200

def query_chatbot(query):
    """
    Query the chatbot API and return the response.
    """
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

def send_instagram_message(access_token, recipient_psid, message):
    """
    Send a text message to the user on Instagram.
    """
    url = f"https://graph.facebook.com/v21.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": recipient_psid},
        "message": {"text": message},
        "messaging_type": "RESPONSE"
    }
    params = {"access_token": access_token}
    
    try:
        response = requests.post(url, headers=headers, json=payload, params=params)
        if response.status_code == 200:
            print(f"Message sent successfully to {recipient_psid}!")
        else:
            print(f"Failed to send message to {recipient_psid}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the message: {e}")

if __name__ == '__main__':
    app.run(port=5000, debug=True)

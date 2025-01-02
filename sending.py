import requests

# Replace with your details
ACCESS_TOKEN = "EAAVau3ZAHEmoBOZCpmK11JBxisFRBxKy41YWyIRpbX4uFraDTihQBRJ6mmHmLzZARcCW4hsWb42naMyjHzQmrDTFaSDt3l4gb5mglzgqeOeN4BgA0gNn58PAIZAZAllvBrMjRIKJwQDntUXMpmksspG13xZCwFKoNbycFkQZAzJSZCn1m2jyWUfeyksYtCQZCqxovIbtHDPHZBqKvyplj2zCtNqs9UFsU6ZBOUT0GkZD"
PHONE_NUMBER_ID = "526125860582825"  # From Meta Developer Console
RECIPIENT_PHONE_NUMBER = "+9779805134917"  # Use format: "+1234567890"
MESSAGE_TEXT = "Hello, this is a message from Sonang"

# URL for the Cloud API
url = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"

# API headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Message payload
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE_NUMBER,
    "type": "text",
    "text": {
        "body": MESSAGE_TEXT
    }
}

# Send the message
response = requests.post(url, headers=headers, json=payload)

# Check response
if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}")
    print(response.json())

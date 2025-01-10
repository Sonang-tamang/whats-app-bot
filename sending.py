import requests

# Replace these with your details
ACCESS_TOKEN = 'EAAS7RHRiHFkBOZCrtda0EQv7IHNHYmiuWZCZCnCtR82QYUZB4TxbNBpaj7ZAZAZCrgnzVBAfFwKpZCW2tUFUg2pO3ZBmbvtyZA5VAwbPP8sQVbHZCq4Un3aS5Y8SD4eesna6ra1CNjEavZCVPOEOXQQYFfnqCm4lU91O93NJbFNUqRqGuG4L5CmUL442qaroU5dpTmEY5W6Nnotmpksg3ZBBOL3ScSW0T'

RECIPIENT_PSID = '1260363568412248'  # Obtain this via API

def send_instagram_message(access_token, recipient_psid, message):
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
    
    response = requests.post(url, headers=headers, json=payload, params=params)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.json())

# Example usage
send_instagram_message(ACCESS_TOKEN, RECIPIENT_PSID, "Hello! This is a test message ttt.")

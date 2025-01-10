import requests

# Page Access Token from Facebook App
PAGE_ACCESS_TOKEN = "your_page_access_token"

# Recipient ID (User ID from Messenger)
recipient_id = "user_psid"

# Message Content
message = "Hello! This is a message from my Python script."

# API Endpoint
url = "https://graph.facebook.com/v15.0/me/messages"

# Headers and Payload
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}",
}
payload = {
    "recipient": {"id": recipient_id},
    "message": {"text": message},
}

# Send the Message
response = requests.post(url, headers=headers, json=payload)

# Check Response
if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Error: {response.status_code}, {response.text}")

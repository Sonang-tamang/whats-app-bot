import requests
import json

def get_instagram_account_id(access_token, facebook_page_id):
    """Get Instagram Business Account ID connected to your Facebook Page"""
    url = f"https://graph.facebook.com/v19.0/{facebook_page_id}?"
    params = {
        'access_token': access_token,
        'fields': 'instagram_business_account'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Instagram Account Response: {response.json()}")
        data = response.json()
        return data.get('instagram_business_account', {}).get('id')
    except Exception as e:
        print(f"Error getting Instagram account ID: {e}")
        return None

def verify_permissions(access_token):
    """Verify token permissions"""
    url = "https://graph.facebook.com/v19.0/me/permissions"
    params = {'access_token': access_token}
    
    try:
        response = requests.get(url, params=params)
        print(f"Permissions Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return None

def send_instagram_message(access_token, ig_user_id, recipient_id, message_text):
    """Send a message to an Instagram user using the Graph API"""
    url = f"https://graph.facebook.com/v19.0/{ig_user_id}/messages"
    
    payload = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': message_text
        },
        'access_token': access_token
    }
    
    print(f"\nSending message with payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(url, json=payload)
        print(f"\nFull Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        return response.json() if response.ok else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Error details: {e.response.text}")
        return None

if __name__ == "__main__":
    # Your credentials
    ACCESS_TOKEN = "your_access_token"
    PAGE_ID = "516688734865370"  # Your Facebook Page ID
    RECIPIENT_USERNAME = "17841471908744933"  # The Instagram username of recipient
    MESSAGE = "Hello! This is a test message."
    
    # Step 1: Verify permissions
    print("\nVerifying permissions...")
    permissions = verify_permissions(ACCESS_TOKEN)
    
    # Step 2: Get Instagram Business Account ID
    print("\nGetting Instagram Business Account ID...")
    ig_account_id = get_instagram_account_id(ACCESS_TOKEN, PAGE_ID)
    print(f"Instagram Business Account ID: {ig_account_id}")
    
    if ig_account_id:
        # Step 3: Send message
        result = send_instagram_message(ACCESS_TOKEN, ig_account_id, RECIPIENT_USERNAME, MESSAGE)
        
        if result:
            print("\nMessage sent successfully!")
            print(f"Response: {result}")
        else:
            print("\nFailed to send message. Check the error details above.")
    else:
        print("\nFailed to get Instagram Business Account ID. Cannot proceed.")
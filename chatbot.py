import requests

# Define the API endpoint
api_url = "https://jec-chatbot.goodwish.com.np/assistant/query/"

# Define the query payload
payload = {
    "query": "tell jec"
}

# Make the POST request
try:
    response = requests.post(api_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print("Response:", data.get("response"))
    else:
        print("Error:", response.status_code, response.text)
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)

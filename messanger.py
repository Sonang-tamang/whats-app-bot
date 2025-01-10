from flask import Flask, request, jsonify

app = Flask(__name__)

# Verify Token (use your own secure token)
VERIFY_TOKEN = "12345"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "Forbidden", 403
    elif request.method == 'POST':
        # Handle incoming messages
        data = request.json
        print("Received webhook data:", data)
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)

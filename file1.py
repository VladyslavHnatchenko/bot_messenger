from flask import request


@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    entry = data['entry'][0]
    if entry.get("messaging"):
        messaging_event = entry['messaging'][0]
        sender_id = messaging_event['sender']['id']
        message_text = messaging_event['message']['text']
        send_text_message(sender_id, message_text)
    return 'ok', 200

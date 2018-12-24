import json
import requests
from flask import Flask, request

VERIFY_TOKEN = "giphy"

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # Once the endpoint is addede as a webhook, is must return back
    # the 'hub.challenge' value is receives in the request arguments
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        print("Verified")
        return request.args.get('hub.challenge', '')
    else:
        print('wrong verification token')
        return "Error, Verification Failed"


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


def send_text_message(recipient_id, message):
    data = json.dumps({
        "recepient": {"id": recipient_id},
        "message": {"text": message}
    })

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params, headers=headers, data=data
    )


def search_gif(text):
    # get a GIF that is similar to text sent
    payload = {'s': text, 'api_key': '<GIPHY_API_KEY>'}
    r = requests.get('http://api.giphy.com/v1/gifs/translate', params=payload)
    r = r.json()
    url = r['data']['images']['original']['url']

    return url


def send_gif_message(recipient_id, message):
    gif_url = search_gif(message)

    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": gif_url
                }
            }}
    })

    params = {
                 "access_token": PAGE_ACCESS_TOKEN
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params, headers=headers, data=data
    )


if __name__ == '__main__':
    app.run(debug=True)

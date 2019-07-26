import random
import os

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == "GET":
        token_sent = request.args.get('hub.verify_token')
        return verify_facebook_token(token_sent)
    else:
        # get message sent by the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # get the user id so we can send back reponse
                    user_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(user_id, response_sent_text)
                    # if user sends a picture, GIF
                    if message['message'].get('attachments'):
                        response_sent_text = get_message()
                        send_message(user_id, response_sent_text)
    return "message processed"


def verify_facebook_token(token_sent):
    # verify is token sent by FB matches the verify token you sent
    if token_sent == VERIFY_TOKEN:
        print(token_sent)
        return request.args.get("hub.challenge")
    return "Invalid verification token"


def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


def get_message():
    responses = ['Bey Hive', 'Stunning', 'Halo', 'Free',
                 'What is free?', 'Mandhi', "Baller"]
    return random.choice(responses)


if __name__ == '__main__':
    app.run()

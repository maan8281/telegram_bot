from flask import Flask, request
import telegram
import re
from telebot.credentials import bot_token, bot_user_name, URL

global TOKEN
global bot

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

#start the flask app

app = Flask(__name__)

#creating routes
@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()

    # for debugging purposes only
    print('got text message:', text)

    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
       Welcome to coolAvatar bot, the bot is using the service from
       https://api.dicebear.com/7.x/lorelei/svg?seed= to generate cool looking avatars based
       on the name you enter so please enter a name and the bot will reply with an avatar for your name.
       """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"/W", "_", text)
            # create the api link for the avatar based on https://www.gravatar.com/avatar/
            url = "https://api.dicebear.com/7.x/lorelei/png?seed={}".format(text.strip())
            print(url)

            # reply with a photo to the name the user sent,
            #note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id=chat_id, photo="https://snmtechnologies.com/style/images/logo.png", reply_to_msg_id=msg_id)
            print(a)
        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
    return "ok"

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
        # we use the bot object to link the bot to our app which live
        # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
        # something to let us know things work
    if s:
        return 'things went well'
    else:
        return 'webhook setup failed'

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)

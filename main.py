import os
import telebot
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Firebase initialize
cred = credentials.Certificate("firebase_key.json")  # Your downloaded key
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get("FIREBASE_DB_URL")  # e.g. https://your-app.firebaseio.com
})

# /start command
@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, "Hello World 👋")

# /users command to show firebase user data
@bot.message_handler(commands=['users'])
def show_users(message):
    ref = db.reference('users')
    data = ref.get()

    if not data:
        bot.send_message(message.chat.id, "Koi user data nahi mila.")
        return

    text = "📋 User List:\n"
    for key, user in data.items():
        name = user.get("name", "No Name")
        email = user.get("email", "No Email")
        text += f"\n👤 {name}\n📧 {email}\n"

    bot.send_message(message.chat.id, text)

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

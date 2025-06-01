import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Firebase key file ka naam yahaan likhna hai (jo aapne upload kiya)
cred = credentials.Certificate("tele-73749-firebase-adminsdk-fbsvc-74bb9599a7.json")

# Firebase Realtime Database URL yahaan daalna hai
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tele-73749-default-rtdb.firebaseio.com//'
})

# Telegram Bot Token yahaan daalna hai
BOT_TOKEN = "7074759528:AAEP1WBtIp7-IQM6T72owwRSVmVVYKlaSYQ"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello World! 👋")

# /users command
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = db.reference("/users")  # Firebase ke users path ka reference
    data = ref.get()

    if data:
        msg = "📋 Firebase Users:\n\n"
        for key, user in data.items():
            msg += f"🧑 {user.get('name', 'No Name')}\n"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ Koi user nahi mila.")

# Bot run karne ka function
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users))

    app.run_polling()

if __name__ == "__main__":
    run_bot()

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests
import os

# Get the Telegram Bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to fetch download link using Ironman API
def get_terabox_download_link(url):
    api_url = f"https://ironman.koyeb.app/ironman/dl/terabox?link={url}"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data.get("download", "⚠️ Failed to get download link.")
    except:
        return "⚠️ Error contacting Ironman API."

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ഹായ്! TeraBox link അയക്കൂ, ഞാൻ download link തരാം.")

# Handle normal messages (TeraBox links)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "terabox" in url:
        await update.message.reply_text("🔄 Link process ചെയ്യുന്നു...")
        download_link = get_terabox_download_link(url)
        await update.message.reply_text(f"✅ Download Link:\n{download_link}")
    else:
        await update.message.reply_text("⚠️ ശരിയായ TeraBox link അയക്കൂ.")

# Main app entry
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()

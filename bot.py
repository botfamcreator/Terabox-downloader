import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

def get_terabox_download_link(url):
    api_url = f"https://teraboxdownloader.com/api/download?url={url}"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data.get("download_url", "⚠️ Failed to extract download link.")
    except:
        return "⚠️ Error contacting API."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ഹായ്! TeraBox link അയക്കൂ, ഞാൻ download link തരാം.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "terabox" in url:
        await update.message.reply_text("🔄 Link process ചെയ്യുന്നു...")
        download_link = get_terabox_download_link(url)
        await update.message.reply_text(f"✅ Download Link:\n{download_link}")
    else:
        await update.message.reply_text("⚠️ ശരിയായ TeraBox link അയക്കൂ.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
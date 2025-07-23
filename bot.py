import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests
import os
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

def get_terabox_download_link_scraper(url):
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        text = resp.text
        # match JSON dlink field
        m = re.search(r'"dlink":"(https://[^"]+)"', text)
        if m:
            link = m.group(1).encode('utf-8').decode('unicode_escape')
            return link
        return "⚠️ Couldn't extract direct link."
    except Exception as e:
        logging.error("Scraper error: %s", e)
        return "⚠️ Error contacting TeraBox page."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 TeraBox link അയക്കൂ, ഞാൻ scrap ചെയ്ത് direct download link തരാം.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "terabox.com" in url:
        await update.message.reply_text("🔄 Scraping link, please wait...")
        direct_link = get_terabox_download_link_scraper(url)
        await update.message.reply_text(f"✅ Download link:\n{direct_link}")
    else:
        await update.message.reply_text("⚠️ Valid TeraBox shared link അയക്കൂ.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()

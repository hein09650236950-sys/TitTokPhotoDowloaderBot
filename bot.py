import os
import logging
import asyncio
from flask import Flask
from threading import Thread
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging အခြေအနေကြည့်ရန်
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Web Server အတွက် Flask ဆောက်ခြင်း (Uptime အတွက်)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Bot Logic ---
TOKEN = "8796001046:AAHyVU5N785MfIBEDhDZb4zM1iFIKEOSSmk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 TikTok Link ပေးပါ၊ Logo မပါတဲ့ ပုံနဲ့ ဗီဒီယိုတွေကို ဒေါင်းပေးပါ့မယ်။")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        return

    msg = await update.message.reply_text("⏳ လုပ်ဆောင်နေပါတယ်...")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Slideshow (Images) ဖြစ်လျှင်
            if 'entries' in info:
                for entry in info['entries']:
                    await update.message.reply_photo(photo=entry['url'])
            # Video ဖြစ်လျှင်
            else:
                video_url = info.get('url')
                await update.message.reply_video(video=video_url, caption="Done! ✅")
            
            await msg.delete()

    except Exception as e:
        logging.error(f"Error: {e}")
        await msg.edit_text("❌ အဆင်မပြေပါ။ TikTok Link မှန်ကန်ကြောင်း ပြန်စစ်ပေးပါ။")

def main():
    # Web Server စတင်ခြင်း
    keep_alive()

    # Telegram Bot စတင်ခြင်း
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()

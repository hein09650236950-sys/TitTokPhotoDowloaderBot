import os
import logging
import asyncio
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token ကို Environment Variable ကနေယူမယ်
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 မင်္ဂလာပါ။ TikTok Link ပေးလိုက်ရင် Logo မပါတဲ့ ပုံနဲ့ ဗီဒီယိုတွေကို ထုတ်ပေးပါ့မယ်။")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        return

    status_msg = await update.message.reply_text("⏳ လုပ်ဆောင်နေပါတယ်၊ ခဏစောင့်ပေးပါ...")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Slideshow (Images) ဖြစ်ခဲ့လျှင်
            if 'entries' in info or (info.get('type') == 'playlist'):
                images = info.get('entries', [])
                for img in images:
                    await update.message.reply_photo(photo=img['url'])
            # ပုံမှန် Video ဖြစ်ခဲ့လျှင်
            else:
                video_url = info.get('url')
                await update.message.reply_video(video=video_url, caption="Done! ✅")
            
            await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ အဆင်မပြေဖြစ်သွားပါတယ်။ Link မှန်မမှန် ပြန်စစ်ပေးပါ။")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN not found in environment variables!")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

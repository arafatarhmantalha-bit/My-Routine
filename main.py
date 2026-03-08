import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# 2. Get Token from Railway Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 4-day study cycle logic
SCHEDULE = {
    0: ("সাধারণ গণিত", "সাধারণ বিজ্ঞান"),
    1: ("বাংলা", "ইংরেজি"),
    2: ("ধর্ম", "কৃষিশিক্ষা"),
    3: ("বা.ও বিশ্ব প.", "তথ্য ও যোগাযোগ প্রযুক্তি")
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("➡️ /list", callback_data="show_list")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📚 Ramadan Study Routine Bot\nClick the button below to see the routine.",
        reply_markup=reply_markup
    )

async def list_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()

    keyboard = []
    row = []
    for i in range(1, 31):
        row.append(InlineKeyboardButton(f"Ramadan {i:02d}", callback_data=f"day_{i}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_text = "📅 Select a day to see the routine:"
    
    if query:
        await query.edit_message_text(msg_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(msg_text, reply_markup=reply_markup)

async def day_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    day_num = int(query.data.split("_")[1])
    cycle_idx = (day_num - 1) % 4
    sub1, sub2 = SCHEDULE[cycle_idx]
    
    text = (
        f"🌙 *Ramadan {day_num:02d} Routine*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🌅 7:00–8:00 AM — {sub1}\n"
        f"☀️ 2:00–3:00 PM — {sub2}\n"
        f"🌙 9:00–10:00 PM — রিভিশন\n"
        f"━━━━━━━━━━━━━━━"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to List", callback_data="show_list")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    if not BOT_TOKEN:
        print("Error: Please set BOT_TOKEN in Railway Variables!")
        return

    # In v20+, we use Application instead of Updater
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_days))
    app.add_handler(CallbackQueryHandler(list_days, pattern="^show_list$"))
    app.add_handler(CallbackQueryHandler(day_details, pattern="^day_"))

    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
    

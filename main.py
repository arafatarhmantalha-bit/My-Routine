import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 4 Day Routine Cycle
ROUTINE = {
    0: ("সাধারণ গণিত", "সাধারণ বিজ্ঞান"),
    1: ("বাংলা", "ইংরেজি"),
    2: ("ধর্ম", "কৃষিশিক্ষা"),
    3: ("বা.ও বিশ্ব প.", "তথ্য ও যোগাযোগ প্রযুক্তি")
}


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📅 View Ramadan Routine", callback_data="routine")]
    ]

    await update.message.reply_text(
        "📚 Ramadan Study Routine Bot\n\nClick the button below to see your routine.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# SHOW LIST
async def show_days(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = []
    row = []

    for i in range(1, 31):

        row.append(
            InlineKeyboardButton(
                f"Ramadan {i:02d}",
                callback_data=f"day_{i}"
            )
        )

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    await query.edit_message_text(
        "📅 Select a Ramadan day:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# DAY HANDLER
async def routine_day(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    day = int(query.data.split("_")[1])

    index = (day - 1) % 4
    sub1, sub2 = ROUTINE[index]

    text = f"""
🌙 Ramadan {day:02d} Routine

🌅 7:00–8:00 AM — {sub1}
☀️ 2:00–3:00 PM — {sub2}
🌙 9:00–10:00 PM — রিভিশন
"""

    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data="routine")]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# MAIN FUNCTION
def main():

    if not BOT_TOKEN:
        print("BOT_TOKEN not found!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_days, pattern="routine"))
    app.add_handler(CallbackQueryHandler(routine_day, pattern="day_"))

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()

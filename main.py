import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Load token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Define the 4-day repeating schedule cycle
SCHEDULE_CYCLE = {
    0: ("সাধারণ গণিত", "সাধারণ বিজ্ঞান"),      # Day 1, 5, 9...
    1: ("বাংলা", "ইংরেজি"),                   # Day 2, 6, 10...
    2: ("ধর্ম", "কৃষিশিক্ষা"),                  # Day 3, 7, 11...
    3: ("বা.ও বিশ্ব প.", "তথ্য ও যোগাযোগ প্রযুক্তি") # Day 4, 8, 12...
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with a button to open the list."""
    keyboard = [[InlineKeyboardButton("➡️ /list", callback_data="show_list")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📚 Ramadan Study Routine Bot\nClick the button below to see the routine.",
        reply_markup=reply_markup
    )

async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows the 30 days of Ramadan as buttons."""
    query = update.callback_query
    await query.answer()

    keyboard = []
    # Create 30 buttons, 3 buttons per row
    row = []
    for i in range(1, 31):
        day_str = f"{i:02d}"
        row.append(InlineKeyboardButton(f"Ramadan {day_str}", callback_data=f"day_{i}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("📅 Select a day to see the routine:", reply_markup=reply_markup)

async def handle_day_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles clicks on specific Ramadan days."""
    query = update.callback_query
    await query.answer()
    
    day_num = int(query.data.split("_")[1])
    
    # Calculate which subjects apply based on the 4-day cycle
    # We use (day_num - 1) % 4 to map 1->0, 2->1, 3->2, 4->3, 5->0...
    cycle_index = (day_num - 1) % 4
    subject1, subject2 = SCHEDULE_CYCLE[cycle_index]
    
    # Exception for Ramadan 09, 10, 18, 19, 27, 28 (Math/Science blocks in image)
    # The image shows some specific double-ups, but the logic below follows 
    # the 4-day pattern provided in your prompt and the image's general flow.
    
    response = (
        f"🌙 *Ramadan {day_num:02d} Routine*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🌅 7:00–8:00 AM — {subject1}\n"
        f"☀️ 2:00–3:00 PM — {subject2}\n"
        f"🌙 9:00–10:00 PM — রিভিশন\n"
        f"━━━━━━━━━━━━━━━"
    )

    # Add a back button to return to the list
    keyboard = [[InlineKeyboardButton("🔙 Back to List", callback_data="show_list")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=response, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    """Start the bot."""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in environment variables.")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list", show_list)) # Also support /list command
    application.add_handler(CallbackQueryHandler(show_list, pattern="^show_list$"))
    application.add_handler(CallbackQueryHandler(handle_day_click, pattern="^day_"))

    # Run the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()

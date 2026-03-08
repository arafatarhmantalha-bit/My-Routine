Ramadan Study Routine Telegram Bot

A simple Telegram bot that shows a Ramadan study routine using inline buttons.

Features

- /start command
- Inline button menu
- Ramadan 01 – Ramadan 30 routine
- Clean Python code
- Railway deploy compatible

Tech Used

- Python
- python-telegram-bot v20
- Railway
- GitHub

Project Structure

ramadan-routine-bot/

- main.py
- requirements.txt
- Procfile
- README.md

Setup

1. Clone the repository

git clone https://github.com/yourusername/ramadan-routine-bot.git

2. Install requirements

pip install -r requirements.txt

3. Add your Telegram Bot Token

Set environment variable:

BOT_TOKEN=your_bot_token

4. Run the bot

python main.py

Deployment

This bot can be deployed easily on Railway.

Procfile:

worker: python main.py

Bot Commands

/start – Start the bot
/list – Show Ramadan routine list

Author

Created by Saa'Fe

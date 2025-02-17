# Telegram QR Code Bot

This is a Telegram bot that extracts QR codes from images and PDFs, then stores the extracted links in an Excel file. The bot supports multiple image uploads from both mobile and desktop devices.

## Features
- Extracts QR codes from images and PDF files.
- Supports multiple image uploads at once.
- Stores extracted QR links in an Excel file.
- Sends back extracted links to the user.
- Provides the updated Excel file with all stored links.

## Requirements
- Python 3.6+
- Telegram Bot API token
- Required libraries:
  ```sh
  pip install pyTelegramBotAPI opencv-python pandas numpy pyzbar pymupdf
  ```

## Setup and Usage
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/telegram-qr-bot.git
   cd telegram-qr-bot
   ```

2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your Telegram bot token:
   ```sh
   BOT_TOKEN=your_telegram_bot_token
   ```

4. Run the bot:
   ```sh
   python bot.py
   ```

## Deployment Options
### **1. Using PythonAnywhere (Free & Simple)**
- Upload `bot.py` to PythonAnywhere.
- Install dependencies via Bash console:
  ```sh
  pip install --user pyTelegramBotAPI opencv-python pandas numpy pyzbar pymupdf
  ```
- Use `nohup` to keep the bot running:
  ```sh
  nohup python3 bot.py &
  ```

### **2. Using Railway (For Continuous Running)**
- Deploy the bot to [Railway](https://railway.app/).
- Set up an environment variable `BOT_TOKEN`.
- Use a worker service to keep it running.

### **3. Using Render (Simple Deployment)**
- Connect your repository to [Render](https://render.com/).
- Deploy it as a web service with `python bot.py` as the start command.

## Contributions
Feel free to fork this repository and submit pull requests.

## License
MIT License


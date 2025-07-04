# 🛍️ Affiliate Marketing Automation Tool

This Python-based tool automates affiliate marketing workflows by scraping product data from websites, extracting links, and sending product details to a Telegram channel using a bot.

---

## 📁 Project Structure

affiliate-marketing/
├── scrapper.py # Extracts product name, image, price, and discount from product pages
├── link_extractor.py # Extracts product links from source pages
├── bot1.py # Sends the extracted data to a Telegram channel using a bot
├── requirements.txt # Python dependencies for the project



## 🚀 Features

- 🔗 Extract product links from e-commerce websites
- 📦 Scrape product details: name, image, price, and discount
- 📤 Automatically send product information to Telegram channels via bot
- 🔒 Securely integrates Groq API and Telegram credentials using environment variables or manual entry

---

## ⚙️ Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/Ambujkumar909/affiliate-marketing.git
cd affiliate-marketing
Step 2: Install Python dependencies

pip install -r requirements.txt
Step 3: Install Playwright browsers

playwright install
🔑 API Keys & Tokens Setup
Before running bot1.py, open the file and replace the following with your actual values:


# bot1.py (line examples)

groq_api_key = "YOUR_GROQ_API_KEY"       # Replace with your Groq API key
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"    # Replace with your Telegram bot token
chat_id = "YOUR_TELEGRAM_CHANNEL_ID"     # Replace with your Telegram channel or group ID
✅ Important: Never share your API keys publicly. Use .env files for production setups.

📦 How to Use
1. Extract Product Links
Run this script to collect affiliate product links:

python link_extractor.py
2. Scrape Product Details
After extracting links, run this to scrape product info like name, image, price, and discount:

python scrapper.py
3. Send to Telegram
Finally, run the bot script to send the scraped product data to your Telegram channel:

python bot1.py
🌐 Requirements Summary
Python 3.8+

playwright

pymysql

python-telegram-bot

groq (or use HTTP-based integration)

python-dotenv (optional, for secure environment variable loading)

🔒 Security Best Practices
Do not hardcode your API keys or tokens in production.

Use .env files and python-dotenv to manage secrets.

GitHub push protection will block you if you accidentally commit secrets.

📬 Author
Made by Ambuj Kumar

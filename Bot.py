import token
import pymysql
from groq import Groq  # Groq's official Python client
import time
import random
import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

Bot_token = os.getenv("bot_token")
bot = Bot(token=Bot_token)
chat_id = '@budget_loot_deals_hub'
BUTTON_TEXTS = [
    "🛍️ Shop Now",
    "💸 Buy Now",
    "🔥 Grab Now",
    "📦 Order Now",
    "🧾 Check Deal"
]


async def send_promo(bot, chat_id, image_url, message_text, product_link):
    """
    Sends a promo post with:
    - 📷 Image
    - 📝 Multi-line message
    - 🔘 A dynamic single button (e.g., Shop Now, Buy Now, etc.)
    """

    # Randomly choose a button label
    button_label = random.choice(BUTTON_TEXTS)

    # Add spacing between message and button
    caption = f"{message_text}\n\n👇"

    # Create inline keyboard with one dynamic button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(button_label, url=product_link)]
    ])

    # Send photo with caption and inline button
    await bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=caption,
        reply_markup=keyboard,
        parse_mode="HTML"  # HTML preserves message structure & emojis
    )


def format_llm_message(text):
    # Step 1: Remove unwanted lines
    lines = text.strip().split("\n")
    useful_lines = [line.strip() for line in lines if not line.lower().startswith(('here', '✅', 'prompt', 'message'))]

    # Step 2: If it's a single line joined by "|", split it
    if len(useful_lines) == 1 and '|' in useful_lines[0]:
        split_lines = [part.strip() for part in useful_lines[0].split('|')]
        return "\n".join(split_lines[:4])  # Limit to 4 lines
    else:
        return "\n".join(useful_lines[:4])  # Still limit to 4 lines if needed


# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Ambuj@123kr",
    database="affiliate",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

# Initialize Groq client
client = Groq(api_key=os.getenv("groq_api"))  

# Fetch rows
# Set limit HERE#####
cursor.execute("SELECT name, cashback_url, image_url, price, percent FROM products where percent > 85")
rows = cursor.fetchall()

for row in rows:
    name = row['name']
    price = row['price']
    discount = row['percent']
    image_url = row['image_url']
    cashback_url = row['cashback_url']
    # Create prompt for LLM
    prompt = f"""
You are a creative marketing copywriter for Telegram deals.

Your job is to create a short, engaging 4-line promotional message from product info:

Generate only a catchy 4-line promotional message from the info below. 
⚠️ Do NOT include any intro text like “Here’s your message” or “Generated:”
- Product: {name}
- Price: ₹{price}
- Discount: {discount}%

🎯 RULES:
1. Output must be 4 lines only.
2. The tone should be exciting, casual, and human — use emojis sparingly but impactfully.

3. Don't always use the same discount phrase. Mix it up:
   - Save {discount}% now!
   - Steal deal: {discount}% OFF!
   - {discount}% off madness!
   - Price slashed by {discount}%!
   - Grab it at {discount}% less!
4. Don't reveal original price.
5. Avoid always starting with "Only ₹XYZ" — be creative:
   - Just ₹{price}
   - Yours for ₹{price}
   - Pick it up at ₹{price}
   - Steal it at ₹{price}
6. Message should be in 4 line and make sure each line should not be much longer end each line as short as possible. 
7. no content should be missing in each line. 
8. End line should be an urgency message like:
   - Don’t miss out!
   - Deal ends soon!
   - Hurry — limited stock!
   - Grab it before it's gone!
9. Generate only a catchy 4-line promotional message from the info below. 
⚠️ Do NOT include any intro text like “Here’s your message” or “Generated:”

10. make sure each line should be finished in maximum of 6-7 words strictly.

11. strictly generate 4 line message. 

✳️ Message must feel different for each product but follow this style.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a catchy product copywriter."},
            {"role": "user", "content": prompt}
        ]
    )

    message = response.choices[0].message.content
    formated_message = format_llm_message(message)
    print(f"\n{formated_message}\n")

    # Here: send to Telegram bot (optional)
    # requests.post(TELEGRAM_URL, data={"text": message})
    send_promo(bot, chat_id, formated_message, image_url, cashback_url)
    print("\nSent\n")
    # Small sleep to avoid hammering API
    time.sleep(0.5)

# Cleanup
conn.close()

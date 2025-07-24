import token
import pymysql
from groq import Groq
import time
import random
import asyncio  # Import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import os
random.seed()
Bot_token = os.getenv("bot_token") 
bot = Bot(token=Bot_token)
chat_id = '@budget_loot_deals_hub'
BUTTON_TEXTS = [
    "🛍️ Shop Now",
    "💸 Buy Now",
    "🔥 Grab Now",
    "📦 Order Now",
    
]


async def send_promo(bot, chat_id, image_url, message_text, product_link):
    """
    Sends a promo post with:
    - 📷 Image
    - 📝 Multi-line message
    - 🔘 A dynamic single button
    """
    
    button_label = random.choice(BUTTON_TEXTS)
    caption = f"{message_text}\n\n{button_label}: {product_link}"
    
    response = await bot.send_photo(# Use await here
        chat_id=chat_id,
        photo=image_url,
        caption=caption,
        
    )
    return response


def format_llm_message(text, line):
    lines = text.strip().split("\n")
    useful_lines = [line.strip() for line in lines if not line.lower().startswith(('here', '✅', 'prompt', 'message'))]
    if len(useful_lines) == 1 and '|' in useful_lines[0]:
        split_lines = [part.strip() for part in useful_lines[0].split('|')]
        return "\n".join(split_lines[:line])
    else:
        return "\n".join(useful_lines[:line])


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
cursor.execute("SELECT id, name, cashback_url, image_url, price, percent FROM products WHERE category = 'super_seller' And status = 'unsent'")
rows = cursor.fetchall()


async def main():
    post_no = 0
    for row in rows:
        name = row['name']
        price = row['price']
        discount = row['percent']
        image_url = row['image_url']
        cashback_url = row['cashback_url']
        if post_no == 5:
            print("stop")
            break
        # Create prompt for LLM
        if discount > 69:
            prompt = f"""
    You are a creative marketing copywriter for Telegram deals.
    Generate only a catchy 4-line promotional message from the info below. 
    ⚠️ Do NOT include any intro text like “Here’s your message” or “Generated:”
    - Product: {name}
    - Price: ₹{price}
    - Discount: {discount}%

    🎯 RULES:
    1. Output must be 3 lines only.
    2. The tone should be exciting, casual, and human — use emojis sparingly.
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
    6. Each line should be 6-7 words max.
    7. No content should be missing.
    8. End with urgency message:
    - Don’t miss out!
    - Deal ends soon!
    - Hurry — limited stock!
    - Grab it before it's gone!
    9. Generate only a 3-line message.
    10. Each line max 6-7 words.
    11. Strictly 3 lines.
    """
            response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a catchy product copywriter."},
                {"role": "user", "content": prompt}
            ]
            )

            message = response.choices[0].message.content
            formated_message = format_llm_message(message, 3)
        else:
            prompt = f"""
    You are a creative marketing copywriter for Telegram deals.
    Generate only a catchy 4-line promotional message from the info below. 
    ⚠️ Do NOT include any intro text like “Here’s your message” or “Generated:”
    - Product: {name}
    - Price: ₹{price}
    - Discount: {discount}%

    🎯 RULES:
    1. Output must be 4 lines only.
    2. The tone should be exciting, casual, and human — use emojis sparingly.
    
    3. Don't reveal original price.
    4. Avoid always starting with "Only ₹XYZ" — be creative:
    - Just ₹{price}
    - Yours for ₹{price}
    - Pick it up at ₹{price}
    - Steal it at ₹{price}
    5. Each line should be 6-7 words max.
    6. No content should be missing.
    7. End with urgency message:
    - Don’t miss out!
    - Deal ends soon!
    - Hurry — limited stock!
    - Grab it before it's gone!
    8. Generate only a 3-line message.
    9. Each line max 6-7 words.
    10. Strictly 3 lines.
    """
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a catchy product copywriter."},
                    {"role": "user", "content": prompt}
                ]
            )

            message = response.choices[0].message.content
            formated_message = format_llm_message(message, 3)

        try:
            await send_promo(bot, chat_id, image_url, formated_message, cashback_url)  # Use await
            print("Sent successfully.")
            cursor.execute("UPDATE products SET status = %s WHERE id = %s", ("sent", row['id']))

            conn.commit()
            post_no = post_no + 1
        except Exception as e:
            print("❌ Failed to send:", e)

        time.sleep(3)  # Increased to avoid rate limits

    # Cleanup
    conn.close()


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

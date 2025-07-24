import asyncio
import csv
from pathlib import Path
from playwright.async_api import async_playwright
import re
import pymysql

STORAGE_FILE = "twitter_login.json"


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Divyanshi@1",
        database="tweets",
        cursorclass=pymysql.cursors.DictCursor
    )

    
# Step 1: Save cookies after manual login
async def save_login_state():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("🔐 Please log into Twitter manually in the browser window.")
        await page.goto("https://twitter.com/login")
        await page.wait_for_timeout(60000)  # 60 seconds to log in manually

        await context.storage_state(path=STORAGE_FILE)
        print(f"✅ Login session saved to {STORAGE_FILE}")
        await browser.close()


def clean_tweet(tweet: str) -> str:
    tweet = tweet.strip()

    # Case-insensitive removal of "📝 BREAKING:" or "BREAKING:"
    tweet = re.sub(r"^📝\s*breaking:\s*", "", tweet, flags=re.IGNORECASE)
    tweet = re.sub(r"^breaking:\s*", "", tweet, flags=re.IGNORECASE)

    # Replace line breaks, tabs, etc. with space
    tweet = tweet.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Collapse multiple spaces into a single space
    tweet = ' '.join(tweet.split())

    return tweet


# Step 2: Scrape tweets
async def scrape_tweets():
    tweets = []
    count = 0
    scroll_increment = 700
    seen_tweet = set()
    loop_count = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    notfound_count = 0
    queries = ["WarMonitors", "SaketGokhale", "EndWokeness", "sentdefender", "wetrustinanonym", "haaretzcom", "ReutersWorld", "SpaceX", "muskonomy", "IndiaToday", "TIME", "the_hindu", "cb_doge"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        context = await browser.new_context(
            storage_state=STORAGE_FILE,
            user_agent=user_agent,
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()
        
        for i in queries:
            url = f"https://x.com/{i}"
            table_name = f"tweets_{i}"
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tweet TEXT,
                result INT
                )
            """)
        
            await page.goto(url)
            await page.wait_for_timeout(3000)

            while True:
                await page.wait_for_selector('div[data-testid="cellInnerDiv"]')
                tweet_divs = await page.query_selector_all('div[data-testid="cellInnerDiv"]')

                for tweet in tweet_divs:
                    tweet_text_div = await tweet.query_selector('div[data-testid="tweetText"]')
                    
                    if tweet_text_div:
                        tweet_text = await tweet_text_div.inner_text()
                        tweet_text = tweet_text.strip()

                        if tweet_text not in seen_tweet:
                            seen_tweet.add(tweet_text)
                            processed_tweet = clean_tweet(tweet_text)
                            cursor.execute(f"insert into {table_name} (tweet) values(%s)", processed_tweet)
                        
                            # Optional: Keep seen_tweet from growing too big
                            if len(seen_tweet) > 60:
                                seen_tweet.pop()
                    
                    else:
                        print("not found")
                        notfound_count += 1
                        
                    if notfound_count > 40:
                            break      
                    conn.commit()     
                if notfound_count > 40:
                            break  
                await page.evaluate(f"window.scrollBy(0, {scroll_increment});")
                await page.wait_for_timeout(4000)
                
        conn.close()
        await browser.close()


# Run the scraper
if _name_ == "_main_":
    if not Path(STORAGE_FILE).exists():
        asyncio.run(save_login_state())
    asyncio.run(scrape_tweets())

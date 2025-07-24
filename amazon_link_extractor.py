from playwright.async_api import async_playwright
import asyncio
from urllib.parse import urlparse, parse_qs, unquote
import time
import amazon_functions


def extract_clean_amazon_url(sponsored_url: str) -> str:
    """
    Extracts the clean product URL from a sponsored Amazon tracking link.
    
    Args:
        sponsored_url (str): The full sponsored ad URL (with /sspa/click).
        
    Returns:
        str: Clean product URL, or the original if not found.
    """
    parsed = urlparse(sponsored_url)  # Parse URL into components
    query = parse_qs(parsed.query)  # Parse query string into dictionary

    if "url" in query:
        raw_path = query["url"][0]  # Get encoded product path
        decoded_path = unquote(raw_path)  # Decode special characters
        return f"https://www.amazon.in{decoded_path}"  # Append to Amazon base
    else:
        return sponsored_url 


async def run_scraper():
    count = 0
    total_count = 0
    product_count = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )

        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()
        await page.goto("https://www.amazon.in", timeout=40000)
        await page.wait_for_selector("select#searchDropdownBox", timeout=8000)
        # Select 'Electronics' from dropdown
        await amazon_functions.Electronics(page, total_count, product_count, count)
        await browser.close()
        

# Run the script using asyncio
asyncio.run(run_scraper())

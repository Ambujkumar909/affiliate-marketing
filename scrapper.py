from playwright.sync_api import sync_playwright
import json

import pymysql


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ambuj@123kr",
        database="affiliate",
        cursorclass=pymysql.cursors.DictCursor
    )


def scrape_and_build_product_links():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page_num = 2
        super_seller = "https://earnkaro.com/product/trending-offers"
        Accesories = "https://earnkaro.com/product/accessories"
        electronics = "https://earnkaro.com/product/electronics"
        men_fashion = "https://earnkaro.com/product/men-fashion"
        personal_care = "https://earnkaro.com/product/health-personal-care"
        men_footwear = "https://earnkaro.com/product/men-footwear"
        women_fashion = "https://earnkaro.com/product/women-fashion"
        women_footware = "https://earnkaro.com/product/women-footwear"
        grocery = "https://earnkaro.com/product/grocery-daily-essentials"
        beauty = "https://earnkaro.com/product/beauty"
        home_kitchen = "https://earnkaro.com/product/home-kitchen"
        baby_product = "https://earnkaro.com/product/baby-products"
        luggage = "https://earnkaro.com/product/bags-luggage"
        product_link = [super_seller, home_kitchen, women_footware, baby_product, men_footwear, men_fashion, women_fashion, grocery, luggage, Accesories, beauty, electronics, personal_care]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # 1️⃣ Go to login
        page.goto("https://www.earnkaro.com/login")

        # 2️⃣ Fill username
        page.fill('#uname', 'ambujkr8@gmail.com')
        page.click('#btnLayoutContinue')

        # 3️⃣ Fill password
        page.fill('#pwd', 'Ambuj@123kr')
        page.click('#btnLayoutSignInPass')

        # 4️⃣ Close any popup if exists
        try:
            page.click('#wzrk-cancel')
        except:
            pass

        # 5️⃣ Wait for dashboard
        page.wait_for_timeout(5000)

        # 6️⃣ Loop pages
        for i in product_link:
            
            url = f"{i}?paging={page_num}"

            print(f"Scraping: {url}")

            # ✅ Use longer timeout, wait for DOM only
            page.goto(url, timeout=35000)
            page.wait_for_load_state("domcontentloaded")

            # ✅ Small extra wait for JS (optional)
            page.wait_for_timeout(3000)

            # 7️⃣ Extract the JSON directly
            script_content = page.locator("#__NEXT_DATA__").inner_html()
            json_data = json.loads(script_content)

            # 8️⃣ Access product data
            page_props = json_data["props"]["pageProps"]
            products = page_props.get("data", [])

            print(f"✅ Found {len(products)} products on page {page_num}.")

            # 9️⃣ Add products to dict
            for p in products:
                
                attr = p.get("attributes", {})
                name = attr.get("name", "").strip()
                image_url = attr.get("image_url", "").strip()
                price = attr.get("price", {})
                product_id = p.get("id", "").strip()
                percent = float(price.get("discount_percentage", 0))
                price_dis = float(price.get("discounted_price", 0))
                merchant = (attr.get("merchant_name") or "").strip()
                if merchant:
                    cursor.execute("""insert into products (name,image_url,price,percent,product_id) values (%s,%s,%s,%s,%s) """, (name, image_url, price_dis, percent, product_id))
                   
            conn.commit()

        # 10️⃣ Save once at the end
        conn.close()
        browser.close()


if __name__ == "__main__":
    scrape_and_build_product_links()

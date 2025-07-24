from playwright.sync_api import sync_playwright
import json


def save_essential_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1️⃣ Go to EarnKaro login
        page.goto("https://www.earnkaro.com/login")

        # 2️⃣ Fill username/email
        page.fill('#uname', 'ambujkr8@gmail.com')

        # 3️⃣ Click Continue
        page.click('#btnLayoutContinue')

        # 4️⃣ Fill password
        page.fill('#pwd', 'Ambuj@123kr')

        # 5️⃣ Click Sign In
        page.click('#btnLayoutSignInPass')

        # 6️⃣ Close any popup (WebEngage)
        try:
            page.click('#wzrk-cancel')
        except:
            pass  # Ignore if popup does not appear

        # 7️⃣ Wait for dashboard to confirm login
        # Use a simple wait if dashboard element is uncertain
        page.wait_for_timeout(5000)

        # 8️⃣ Get all cookies
        all_cookies = page.context.cookies()

        # 9️⃣ Filter only important ones
        essential_cookies = {}
        for cookie in all_cookies:
            name = cookie['name']
            if name.startswith('pps_') or name in ['X-PPS-Status', 'RID']:
                essential_cookies[name] = cookie['value']
        print(essential_cookies)
        # 10️⃣ Save only essential cookies
        with open("cookies.json", "w") as f:
            json.dump(essential_cookies, f, indent=2)

        print("✅ Saved only essential cookies to cookies.json")
        print(essential_cookies)

        browser.close()


if __name__ == "__main__":
    save_essential_cookies()

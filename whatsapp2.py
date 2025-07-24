from playwright.sync_api import sync_playwright
import time
import os


def main():
    with sync_playwright() as p:
        user_data_dir = 'playwright/.auth'  # Full persistent session
        os.makedirs(user_data_dir, exist_ok=True)

        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--start-maximized"],
            viewport=None,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )

        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com/")

        try:
            # Wait until QR is scanned or user is logged in
            page.wait_for_selector('div[aria-label="Search input textbox"]', timeout=60000)
            print("🟢 Successfully logged in!")
            time.sleep(2)
            # Click on 'Channels'
            page.wait_for_selector('button[aria-label="Channels"]', timeout=10000)
            page.click('button[aria-label="Channels"]')
            print("📺 Clicked on Channels tab.")
            time.sleep(2)
            # Click specific channel
            page.wait_for_selector('div[aria-label="loot deals India Channel"]', timeout=10000)
            page.click('div[aria-label="loot deals India Channel"]')
            print("📢 Selected channel: loot deals India")

            # Send message
            page.wait_for_selector('div[aria-label="Type an update"]', timeout=10000)
            page.focus('div[aria-label="Type an update"]')

            for char in "Hello, this is an automated message to my WhatsApp Channel!":
                page.keyboard.insert_text(char)
                time.sleep(0.06)
            time.sleep(1)
            page.click('button[aria-label="Send"]')
            print("📨 Message sent successfully.")

            time.sleep(4)

        except Exception as e:
            print(f"❌ Error: {e}")
            print("⚠️ Please scan the QR code again if asked.")

        finally:
            context.close()


if __name__ == "__main__":
    main()

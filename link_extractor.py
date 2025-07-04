from playwright.sync_api import sync_playwright
import re
import pymysql


def login(page):
    """Log in to the EarnKaro website."""
    page.goto("https://www.earnkaro.com/login")
    page.fill('#uname', 'ambujkr8@gmail.com')
    page.click('#btnLayoutContinue')
    page.fill('#pwd', 'Ambuj@123kr')
    page.click('#btnLayoutSignInPass')
    
    # Close any popups if they exist
    close_popup(page)


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ambuj@123kr",
        database="affiliate",
        cursorclass=pymysql.cursors.DictCursor
    )


def slugify_offer_title(text):
    # Convert to lowercase
    text = text.lower()
    
    # Replace all non-alphanumeric characters (except spaces) with a hyphen
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Remove multiple hyphens
    text = re.sub(r'-+', '-', text)
    
    # Trim leading/trailing hyphens
    return text.strip('-')


def close_popup(page):
    """Close any visible popups."""
    try:
        page.click('#wzrk-cancel')
    except Exception:
        pass


def extract_copied_link(page):
    """Extract the copied link from the clipboard or other sources."""
    try:
        copied_url = page.evaluate("() => navigator.clipboard.readText()")
        if copied_url:
            return copied_url
        
        # Check Branch.io data or local storage
        copied_url = page.evaluate("""
            () => {
                if (window.branch && typeof window.branch.getLatestReferringParams === 'function') {
                    return window.branch.getLatestReferringParams();
                }
                if (window.localStorage) {
                    return window.localStorage.getItem('branch_session');
                }
                return null;
            }
        """)
        
        if copied_url and ("myntr.it" in str(copied_url) or "myntr.in" in str(copied_url)):
            return copied_url
        
        # Return None if no URL is found
        return None
    
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return None


def get_final_link():
    """Main function to get the final link."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        base_url = "https://earnkaro.com"
        login(page)
        page.wait_for_timeout(5000)  # Wait for dashboard to load
        
        # Go to the product search page and extract the link
        conn = get_db_connection()
        cursor = conn.cursor() 
        cursor.execute("select name, id, product_id from products where cashback_url is null And percent > 70")
        rows = cursor.fetchall() 
        for row in rows:
            id_new = row['id']
            name = slugify_offer_title(row['name'])
            product_id = row['product_id']
            tracking_url = f"{base_url}/{name}/{product_id}"
            page.goto(tracking_url, timeout=20000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)
            
            # Click the "Copy Link" button
            try:
                page.click(f"#copylink_products_{tracking_url.split('/')[-1]}")
                page.wait_for_timeout(2000)  # Wait for network request and copy action
            except Exception as e:
                print(f"Could not find or click the Copy Link button: {e}")
                continue
            
            # Extract the final URL
            copied_url = extract_copied_link(page)
            if copied_url:
                cursor.execute("""UPDATE products SET cashback_url = %s WHERE id = %s""", (copied_url, id_new))
                print("copied")
            else:
                print("No URL extracted.")
                
            conn.commit()
        
        conn.close()
        browser.close()


if __name__ == "__main__":
    get_final_link()

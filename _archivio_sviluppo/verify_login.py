from playwright.sync_api import sync_playwright
import time

def check_login():
    try:
        with sync_playwright() as p:
            print("[TEST] Avvio browser...")
            browser = p.chromium.launch_persistent_context(
                "./tiktok_profile",
                headless=True,
                executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            print("[TEST] Vado su TikTok.com...")
            page.goto("https://www.tiktok.com/", timeout=60000)
            time.sleep(5)
            
            # Check if login button is present
            is_logged_in = False
            try:
                # If there's a button saying "Log in" or "Accedi", they might not be logged in.
                # A more reliable way is to check for the user profile icon or upload button
                upload_btn = page.locator('a[href*="/upload"]')
                if upload_btn.count() > 0:
                    is_logged_in = True
            except:
                pass
                
            page.screenshot(path="tiktok_login_status.png")
            print(f"[RISULTATO] Loggato: {'SI' if is_logged_in else 'NO (o caricamento parziale)'}")
            browser.close()
            return is_logged_in
    except Exception as e:
        print(f"[ERRORE] {e}")

if __name__ == "__main__":
    check_login()

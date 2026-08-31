import time
from playwright.sync_api import sync_playwright

def debug():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            "./tiktok_profile",
            headless=True,
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        print("Navigating to upload page...")
        page.goto("https://www.tiktok.com/creator-center/upload?from=upload", timeout=60000)
        time.sleep(10)
        
        page.screenshot(path="debug_tiktok_upload.png")
        print("Screenshot saved to debug_tiktok_upload.png")
        
        # Stampa gli iframe disponibili
        print("\nIFRAMES TROVATI:")
        for frame in page.frames:
            print(f"- URL: {frame.url}")
            
        # Stampa i selettori di file
        print("\nINPUT TYPE=FILE TROVATI (Main page):")
        inputs = page.locator('input[type="file"]').element_handles()
        for i in inputs:
            print(f"- {i.get_attribute('accept')}")
            
        print("\nCERCO IN TUTTI GLI IFRAME...")
        for frame in page.frames:
            try:
                f_inputs = frame.locator('input[type="file"]').element_handles()
                for i in f_inputs:
                    print(f"- [In iframe {frame.url[:40]}] accept={i.get_attribute('accept')}")
            except:
                pass
                
        browser.close()

if __name__ == "__main__":
    debug()

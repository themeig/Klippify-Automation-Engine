import time
from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            "./tiktok_profile",
            headless=True,
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.tiktok.com/tiktokstudio/upload?from=upload", timeout=60000)
        time.sleep(15)  # give it time to load the studio UI
        
        print("\n=== DEBUG TIKTOK STUDIO UPLOAD ===")
        # Check if there is an iframe
        frames = page.frames
        upload_frame = None
        for f in frames:
            if "tiktokstudio/upload" in f.url or "tiktokstudio/uplo" in f.url:
                upload_frame = f
                break
        
        target = upload_frame if upload_frame else page
        print(f"Target is iframe: {target != page}")
        
        # Check draft editor
        editor = target.locator('.public-DraftEditor-content, .DraftEditor-root, [contenteditable="true"]')
        print(f"Editor trovati: {editor.count()}")
        
        # Check buttons
        buttons = target.locator('button').all_inner_texts()
        print(f"Bottoni trovati ({len(buttons)}):")
        for b in buttons:
            if b.strip():
                print(f" - '{b.strip()}'")
                
        browser.close()

if __name__ == "__main__":
    inspect()

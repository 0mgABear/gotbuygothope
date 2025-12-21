import os
import re
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

def lambda_handler(event, context):
    token = os.environ.get("BROWSERLESS_TOKEN")
    if not token:
        return {"statusCode": 500, "body": "Missing Browserless token"}

    ws = f"wss://chrome.browserless.io?token={token}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws)
            context = browser.new_context()
            page = context.new_page()

            url = "https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx"
            page.goto(url)

            text = page.inner_text("body")
            browser.close()

    except Exception as e:
        print("ERROR:", e)
        return {"statusCode": 500, "body": str(e)}

    # Extract Jackpot
    jackpot_match = re.search(r"Next Jackpot\s*(\$\d[\d,]*)", text)
    jackpot = jackpot_match.group(1) if jackpot_match else None

    # Extract Next Draw date
    draw_match = re.search(r"Next Draw\s*([\w, ]+\d{4}\s*,\s*\d{1,2}\.\d{2}pm)", text)
    draw_date = draw_match.group(1) if draw_match else None

    return {
        "statusCode": 200,
        "body": {
            "Next Jackpot": jackpot,
            "Next Draw": draw_date
        }
    }

# Local test
if __name__ == "__main__":
    result = lambda_handler({}, {})
    print("\n=== Result ===")
    print(result)

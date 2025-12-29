import os
import re
import requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from datetime import date

load_dotenv()

def send_telegram(text):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={"chat_id": chat_id, "text": text})
    r.raise_for_status()

def lambda_handler(event, context):
    token = os.environ.get("BROWSERLESS_TOKEN")
    if not token:
        return {"statusCode": 500, "body": "Missing Browserless token"}

    ws = f"wss://chrome.browserless.io?token={token}"

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws)
        context_pw = browser.new_context()
        page = context_pw.new_page()

        url = "https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx"
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        text = page.inner_text("body")
        browser.close()

    jackpot_match = re.search(r"Next Jackpot\s*(\$\d[\d,]*)", text)
    jackpot = jackpot_match.group(1) if jackpot_match else "N/A"

    draw_match = re.search(r"Next Draw\s*([\w, ]+\d{4}\s*,\s*\d{1,2}\.\d{2}pm)", text)
    draw_date = draw_match.group(1) if draw_match else "N/A"
    parts = draw_date.split(",")
    date_part = parts[1].strip()
    time = parts[2].strip()

    if date_part ==  date.today().strftime('%d %b %Y'):
        msg = f"🎰 TOTO Update\nNext Jackpot: {jackpot}\nNext Draw: Tonight, {time}"
    else:
        msg = f"🎰 TOTO Update\nNext Jackpot: {jackpot}\nNext Draw: {draw_date}"
    
    send_telegram(msg)

    return {"statusCode": 200}

if __name__ == "__main__":
    lambda_handler({}, None)
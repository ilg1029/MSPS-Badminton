import feedparser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

FEED_URL = "RSS_FEED_URL"  # 填入布告欄的 RSS URL
KEYWORDS = ["羽球", "抽籤", "場地租借", "暑假"]

def clean_text(text):
    return text.replace("\n","").replace("\r","").replace("\t","").replace(" ","").lower()

def fetch_feed():
    feed = feedparser.parse(FEED_URL)
    matches = []

    print("🔹 RSS 共抓到 %d 筆公告" % len(feed.entries))
    
    for i, entry in enumerate(feed.entries, start=1):
        title = entry.title
        link = entry.link

        cleaned = clean_text(title)

        print(f"\n[{i}] 原始標題: {repr(title)}")
        print(f"[{i}] 清理後文字: {repr(cleaned)}")

        matched_keywords = [k for k in KEYWORDS if k.lower() in cleaned]
        if matched_keywords:
            print(f"[{i}] ✅ 匹配到關鍵字: {matched_keywords}")
            matches.append((title, link))
        else:
            print(f"[{i}] ❌ 沒有匹配到關鍵字")
    
    return matches

def send_email(new_announcements):
    if not new_announcements:
        print("ℹ️ 沒有符合的公告，Email 不會寄出")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "🏸 民生國小羽球場公告通知"

    body = "<h3>最新公告：</h3><ul>"
    for title, link in new_announcements:
        body += f'<li><a href="{link}">{title}</a></li>'
    body += "</ul>"

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"✅ 發現 {len(new_announcements)} 則新公告，已寄出通知！")

if __name__ == "__main__":
    matches = fetch_feed()
    send_email(matches)

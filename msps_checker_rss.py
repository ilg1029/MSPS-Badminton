import feedparser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

FEED_URL = "RSS_FEED_URL"  # 替換成布告欄的訂閱連結
KEYWORDS = ["羽球", "抽籤", "場地租借", "暑假"]

def fetch_feed():
    feed = feedparser.parse(FEED_URL)
    matches = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link

        clean_text = title.replace("\n","").replace(" ","").lower()
        if any(k.lower() in clean_text for k in KEYWORDS):
            matches.append((title, link))
    
    return matches

def send_email(new_announcements):
    if not new_announcements:
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

if __name__ == "__main__":
    matches = fetch_feed()
    if matches:
        send_email(matches)
        print(f"✅ 發現 {len(matches)} 則新公告，已寄出通知！")
    else:
        print("ℹ️ 沒有符合的公告")

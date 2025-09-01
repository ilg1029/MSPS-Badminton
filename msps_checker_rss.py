import feedparser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 環境變數 ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

FEED_URL = "RSS_FEED_URL"  # 替換成布告欄的 RSS 訂閱連結
KEYWORDS = ["羽球", "抽籤", "場地租借", "暑假"]

# --- 清理文字函數 ---
def clean_text(text):
    # 去掉換行、制表符、前後空白，統一小寫
    return text.replace("\n","").replace("\r","").replace("\t","").replace(" ","").lower()

# --- 取得公告 ---
def fetch_feed():
    feed = feedparser.parse(FEED_URL)
    matches = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link

        # debug: 印出抓到的原始標題
        print("抓到標題:", repr(title))
        print("清理後:", clean_text(title))

        # 關鍵字匹配
        if any(k.lower() in clean_text(title) for k in KEYWORDS):
            matches.append((title, link))

    return matches

# --- 發 Email ---
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

# --- 主程式 ---
if __name__ == "__main__":
    matches = fetch_feed()
    if matches:
        send_email(matches)
        print(f"✅ 發現 {len(matches)} 則新公告，已寄出通知！")
    else:
        print("ℹ️ 沒有符合的公告")

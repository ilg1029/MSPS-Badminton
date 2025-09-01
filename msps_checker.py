import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 環境變數 ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

ANNOUNCE_PAGE = "https://msps.tp.edu.tw/nss/p/xingzhengbugaolan"

KEYWORDS = ["羽球", "抽籤", "場地租借", "暑假"]

# --- 抓公告 ---
def fetch_announcements():
    res = requests.get(ANNOUNCE_PAGE)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    matches = []

    for ann in soup.find_all("a"):
        text = ann.get_text(strip=True)
        link = ann.get("href")

        # 確保文字和連結存在
        if not text or not link:
            continue

        # debug: 印出抓到的文字，確認抓到公告
        print("抓到公告標題:", repr(text))

        # 清理文字，去掉空格、換行，統一小寫
        clean_text = text.replace("\n","").replace(" ","").lower()

        # 關鍵字匹配
        if any(k.lower() in clean_text for k in KEYWORDS):
            matches.append((text, link))

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
    matches = fetch_announcements()
    if matches:
        send_email(matches)
        print(f"✅ 發現 {len(matches)} 則新公告，已寄出通知！")
    else:
        print("ℹ️ 沒有符合的公告")

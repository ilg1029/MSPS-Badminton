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

BASE_URL = "https://msps.tp.edu.tw"
ANNOUNCE_PAGE = BASE_URL + "/nss/p/xingzhengbugaolan"
KEYWORDS = ["羽球", "抽籤", "場地租借", "暑假"]

# --- 抓公告 ---
def fetch_announcements():
    res = requests.get(ANNOUNCE_PAGE)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    
    announcements = []
    for ann in soup.find_all("a"):
        text = ann.get_text(strip=True)
        link = ann.get("href")
        if not link:
            continue
        # ✅ 避免重複加 BASE_URL
        if not link.startswith("http"):
            link = BASE_URL + link
        # 篩選關鍵字
        if any(k in text for k in KEYWORDS):
            announcements.append((text, link))
    return announcements

# --- 發 Email ---
def send_email(new_announcements):
    if not new_announcements:
        return
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "🏸 民生國小羽球場公告通知"

    # HTML 內容
    body = "<h3>最新公告：</h3><ul>"
    for title, link in new_announcements:
        body += f'<li><a href="{link}">{title}</a></li>'
    body += "</ul>"

    msg.attach(MIMEText(body, "html"))

    # SMTP 寄信
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

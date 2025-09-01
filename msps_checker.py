import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# === 設定 ===
URL = "https://www.msps.tp.edu.tw/nss/p/xingzhengbugaolan"  # 民生國小行政公告頁
KEYWORDS = ["羽球", "抽籤", "場地租借"]

SMTP_SERVER = "smtp.gmail.com"  # 如果用 Gmail
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# === 爬蟲檢查公告 ===
def check_announcements():
    res = requests.get(URL)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    announcements = soup.find_all("a")
    matches = []

    for ann in announcements:
        text = ann.get_text(strip=True)
        link = ann.get("href")
        if any(keyword in text for keyword in KEYWORDS):
            matches.append(f"{text}\n👉 {link}")

    return matches

# === 發送 Email ===
def send_email(matches):
    body = "\n\n".join(matches)
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "【通知】民生國小羽球場抽籤公告更新"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

# === 主程式 ===
if __name__ == "__main__":
    matches = check_announcements()
    if matches:
        send_email(matches)
        print("✅ 發現新公告，已寄出通知！")
    else:
        print("ℹ️ 沒有新公告")

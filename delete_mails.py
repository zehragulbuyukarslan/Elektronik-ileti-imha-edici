#delete_mails.py

import os
import imaplib
import email

# Ortam değişkenlerinden iCloud bilgilerini al
ICLOUD_EMAIL = os.getenv("ICLOUD_EMAIL")
ICLOUD_PASSWORD = os.getenv("ICLOUD_PASSWORD")
DELETE_FROM = os.getenv("DELETE_FROM", None)  # opsiyonel

DELETE_KEYWORDS = os.getenv("DELETE_KEYWORDS", "mülakat 101,seminer,makale,röportaj").split(",")

if not ICLOUD_EMAIL or not ICLOUD_PASSWORD:
    raise Exception("iCloud bilgileri bulunamadı. Lütfen Secrets'a ekle.")

print(f"📬 iCloud hesabına bağlanılıyor ({ICLOUD_EMAIL})...")

# iCloud IMAP sunucusuna bağlan
mail = imaplib.IMAP4_SSL("imap.mail.me.com")
mail.login(ICLOUD_EMAIL, ICLOUD_PASSWORD)
mail.select("INBOX")

total_deleted = 0

for keyword in DELETE_KEYWORDS:
    keyword = keyword.strip()
    print(f"🔍 Anahtar kelimeye göre aranıyor: {keyword}")
    # Eğer gönderen filtresi de varsa, birlikte kullan
    if DELETE_FROM:
        status, data = mail.search(None, f'(FROM "{DELETE_FROM}" TEXT "{keyword}")')
    else:
        status, data = mail.search(None, f'(TEXT "{keyword}")')

    if status != "OK":
        print(f"❌ Arama başarısız ({keyword}).")
        continue

    mail_ids = data[0].split()
    if not mail_ids:
        print(f"🔎 '{keyword}' içeren e-posta bulunamadı.")
        continue

    for mail_id in mail_ids:
        mail.store(mail_id, "+FLAGS", "\\Deleted")
    mail.expunge()
    print(f"✅ {len(mail_ids)} e-posta '{keyword}' kelimesine göre silindi.")
    total_deleted += len(mail_ids)

# Silinecek e-postaları ara
status, data = mail.search(None, f'(FROM "{DELETE_FROM}")')

if status != "OK":
    print("❌ Mail arama işlemi başarısız oldu.")
    exit()

mail_ids = data[0].split()
print(f"🔍 {len(mail_ids)} adet e-posta bulundu.")

if not mail_ids:
    print("Silinecek e-posta yok.")
else:
    for mail_id in mail_ids:
        mail.store(mail_id, "+FLAGS", "\\Deleted")
    mail.expunge()
    print(f"✅ {len(mail_ids)} e-posta başarıyla silindi.")


mail.logout()
print("📤 Oturum kapatıldı.")


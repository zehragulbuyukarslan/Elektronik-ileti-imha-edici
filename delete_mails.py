#delete_mails.py

import os
import imaplib
import sys

# Ortam değişkenlerinden iCloud bilgilerini al
ICLOUD_EMAIL = os.getenv("ICLOUD_EMAIL")
ICLOUD_PASSWORD = os.getenv("ICLOUD_PASSWORD")
DELETE_FROM = os.getenv("DELETE_FROM", None)  # opsiyonel

DELETE_KEYWORDS = os.getenv(
    "DELETE_KEYWORDS", "mulakat,seminer,online etkinlik,makale,roportaj,online yayın"
).split(",")

if not ICLOUD_EMAIL or not ICLOUD_PASSWORD:
    print("❌ iCloud bilgileri bulunamadı. Lütfen Secrets'a ekle.")
    sys.exit(1)

print(f"📬 iCloud hesabına bağlanılıyor ({ICLOUD_EMAIL})...")

# iCloud IMAP sunucusuna bağlan
try:
    mail = imaplib.IMAP4_SSL("imap.mail.me.com")
    mail.login(ICLOUD_EMAIL, ICLOUD_PASSWORD)
    mail.select("INBOX")
except Exception as e:
    print(f"❌ IMAP bağlantısı kurulamadı: {e}")
    sys.exit(1)

total_deleted = 0

for keyword in DELETE_KEYWORDS:
    keyword = keyword.strip()  # Boşlukları temizle
    print(f"🔍 Anahtar kelimeye göre aranıyor: {keyword}")
    
    try:
        if DELETE_FROM:
            search_query = f'(FROM "{DELETE_FROM}" TEXT "{keyword}")'
        else:
            search_query = f'(TEXT "{keyword}")'
            
        status, data = mail.search("UTF-8", search_query)
    except Exception as e:
        print(f"⚠️ Arama sırasında hata oluştu ({keyword}): {e}")
        continue

    # Arama başarısızsa veya data None ise
    if status != "OK" or not data or not data[0]:
        print(f"🔎 '{keyword}' içeren e-posta bulunamadı.")
        continue

    mail_ids = data[0].split()
    if not mail_ids:
        print(f"🔎 '{keyword}' içeren e-posta bulunamadı.")
        continue

    try:
        for mail_id in mail_ids:
            try:
                # Önce çöp kutusuna taşı
                result = mail.copy(mail_id, "Deleted Messages")

                if result[0] == "OK":
                    # Gelen kutusundaki kopyayı silinmiş olarak işaretle
                    mail.store(mail_id, "+FLAGS", "\\Deleted")
                else:
                    print(f"⚠️ Mail {mail_id} çöp kutusuna taşınamadı, direkt silinecek.")
                    mail.store(mail_id, "+FLAGS", "\\Deleted")

            except Exception as e:
                print(f"⚠️ Mail {mail_id} taşınırken hata: {e}")
                continue

        # Gelen kutusundaki silinmişleri temizle
        mail.expunge()

        deleted_count = len(mail_ids)
        total_deleted += deleted_count
        print(f"✅ {deleted_count} e-posta '{keyword}' kelimesine göre silindi.")


    except Exception as e:
        print(f"⚠️ Silme sırasında hata: {e}")

mail.logout()
print(f"📤 Oturum kapatıldı. Toplam silinen e-posta: {total_deleted}")

sys.exit(0)






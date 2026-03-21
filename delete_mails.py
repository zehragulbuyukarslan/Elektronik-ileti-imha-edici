import imaplib

def get_imap_server(email):
    """Email adresine göre IMAP sunucusunu belirle"""
    
    email_lower = email.lower()
    
    if 'gmail.com' in email_lower:
        return "imap.gmail.com"
    elif 'outlook.com' in email_lower or 'hotmail.com' in email_lower:
        return "imap-mail.outlook.com"
    elif 'yahoo.com' in email_lower:
        return "imap.mail.yahoo.com"
    elif 'icloud.com' in email_lower or 'me.com' in email_lower:
        return "imap.mail.me.com"
    else:
        # Diğer providers için varsayılan
        return "imap.gmail.com"

def delete_mails(email, password, keywords, delete_from=None, start_date=None, end_date=None):
    """
    Kullanıcının email bilgileri ile e-postalarını siler
    """
    
    print(f"📬 {email} hesabına bağlanılıyor...")
    
    # Email sağlayıcısına göre doğru IMAP sunucusunu seç
    imap_server = get_imap_server(email)
    print(f"📡 IMAP Sunucusu: {imap_server}")
    
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email, password)
        mail.select("INBOX")
        
    except Exception as e:
        print(f"❌ IMAP bağlantısı kurulamadı: {e}")
        raise Exception(f"Giriş başarısız. Email ve şifreni kontrol et: {e}")
    
    total_deleted = 0
    
    try:
        for keyword in keywords:
            keyword = keyword.strip()
            if not keyword:
                continue
                
            print(f"🔍 '{keyword}' aranıyor...")
            
            try:
                if delete_from:
                    search_query = f'(FROM "{delete_from}" TEXT "{keyword}")'
                else:
                    search_query = f'(TEXT "{keyword}")'
                    
                status, data = mail.search("UTF-8", search_query)
                
                if status != "OK" or not data or not data[0]:
                    print(f"🔎 '{keyword}' bulunamadı")
                    continue
                
                mail_ids = data[0].split()
                
                for mail_id in mail_ids:
                    try:
                        result = mail.copy(mail_id, "Deleted Messages")
                        
                        if result[0] == "OK":
                            mail.store(mail_id, "+FLAGS", "\\Deleted")
                        else:
                            mail.store(mail_id, "+FLAGS", "\\Deleted")
                    except Exception as e:
                        print(f"⚠️ Mail silinirken hata: {e}")
                        continue
                
                mail.expunge()
                deleted_count = len(mail_ids)
                total_deleted += deleted_count
                print(f"✅ {deleted_count} e-posta silindi")
                
            except Exception as e:
                print(f"⚠️ Hata ({keyword}): {e}")
                continue
    
    finally:
        mail.logout()
        print(f"📤 Oturum kapatıldı. Toplam: {total_deleted}")
    
    return total_deleted


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    email = os.getenv("EMAIL") or input("Email: ")
    password = os.getenv("PASSWORD") or input("Şifre: ")
    keywords_input = input("Anahtar kelimeler (enter ile ayırılmış): ")
    keywords = keywords_input.split('\n')
    
    delete_mails(email, password, keywords)
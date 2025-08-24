import requests
import random
import time
import sys
from urllib.parse import urlparse

# USER-AGENT veritabanı
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
]

# M3U URL ve çıktı ayarları
M3U_URL = "https://tinyurl.com/HepsiBirArada"
OUTPUT_FILENAME = "tv_listesi.m3u"  # Yeni dosya adı

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_referer_from_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/"

def fetch_m3u(url, max_retries=3, timeout=10):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': get_referer_from_url(url)
    }
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Deneme {attempt + 1}/{max_retries}: {url}")
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            if response.text.strip().startswith("#EXTM3U"):
                return response.text
            else:
                print("❌ Hata: Geçerli M3U formatı değil!")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Hata: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"⏳ {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
    
    return None

if __name__ == "__main__":
    print("=== M3U Listesi Güncelleme ===")
    m3u_content = fetch_m3u(M3U_URL)
    
    if m3u_content:
        with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"✅ '{OUTPUT_FILENAME}' başarıyla oluşturuldu!")
        sys.exit(0)
    else:
        print("❌ M3U alınamadı! Lütfen URL ve bağlantıyı kontrol edin.")
        sys.exit(1)

# streamed_selenium_m3u.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

TV_IDS = {
    "American Football": "NFL.Dummy.us",
    "Football": "Soccer.Dummy.us",
    "Basketball": "Basketball.Dummy.us",
    "Hockey": "NHL.Hockey.Dummy.us",
    "Tennis": "Tennis.Dummy.us",
    "Darts": "Darts.Dummy.us",
    "Motor Sports": "Racing.Dummy.us",
    "General": "General.Dummy.us"
}

# --- Embed sayfalarını buraya ekle ---
MATCH_PAGES = [
    {
        "page_url": "https://streamed.pk/embed/football/xyz123",
        "title": "Indianapolis Colts vs Pittsburgh Steelers",
        "category": "American Football",
        "logo": "https://streamed.pk/api/Logos/NFL.png"
    }
]

def get_m3u8_from_embed(url):
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5)  # Sayfanın JS ile M3U8 linki yüklenmesi için bekle
        page_source = driver.page_source
        # .m3u8 linkini bul
        import re
        match = re.search(r'https://[^\'" >]+\.m3u8', page_source)
        return match.group(0) if match else None
    finally:
        driver.quit()

def generate_m3u(matches):
    content = ["#EXTM3U"]
    for m in matches:
        m3u8 = get_m3u8_from_embed(m["page_url"])
        if m3u8:
            tv_id = TV_IDS.get(m["category"], "General.Dummy.us")
            content.append(f'#EXTINF:-1 tvg-id="{tv_id}" tvg-name="{m["title"]}" tvg-logo="{m["logo"]}" group-title="{m["category"]}",{m["title"]}')
            content.append(m3u8)
            print(f"✅ Bulundu: {m['title']}")
        else:
            print(f"⚠️ M3U8 bulunamadı: {m['title']}")
    return "\n".join(content)

if __name__ == "__main__":
    playlist = generate_m3u(MATCH_PAGES)
    with open("StreamedSU.m3u8", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("🎉 Playlist oluşturuldu: StreamedSU.m3u8")

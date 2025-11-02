# streamed_auto_m3u.py
# Python 3
import requests
import re

# --- Maç sayfalarını ve bilgilerini ekleyin ---
MATCH_PAGES = [
    {
        "page_url": "https://streamed.pk/embed/football/xyz123",
        "title": "Indianapolis Colts vs Pittsburgh Steelers",
        "category": "American Football",
        "logo": "https://streamed.pk/api/Logos/NFL.png"
    },
    {
        "page_url": "https://streamed.pk/embed/basketball/abc456",
        "title": "Los Angeles Lakers vs Miami Heat",
        "category": "Basketball",
        "logo": "https://streamed.pk/api/Logos/NBA.png"
    }
]

# --- TV ID mapping ---
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

# --- M3U8 linkini sayfa içeriğinden bul ---
def find_m3u8_in_content(content):
    pattern = r'(https?://[^\'" ]+\.m3u8[^\'" ]*)'
    match = re.search(pattern, content)
    return match.group(1) if match else None

# --- Embed sayfasından M3U8 çek ---
def fetch_m3u8_from_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://embedsports.top",
        "Origin": "https://embedsports.top"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return find_m3u8_in_content(r.text)
    except requests.RequestException as e:
        print(f"❌ Hata: {url} → {e}")
        return None

# --- M3U oluştur ---
def generate_m3u(matches):
    content = ["#EXTM3U"]
    for match in matches:
        page_url = match.get("page_url")
        title = match.get("title", "Untitled")
        category = match.get("category", "General")
        logo = match.get("logo", "")
        tv_id = TV_IDS.get(category, "General.Dummy.us")

        m3u8 = fetch_m3u8_from_page(page_url)
        if m3u8:
            content.append(f'#EXTINF:-1 tvg-id="{tv_id}" tvg-name="{title}" tvg-logo="{logo}" group-title="{category}",{title}')
            content.append(m3u8)
            print(f"✅ Bulundu: {title}")
        else:
            print(f"⚠️ M3U8 bulunamadı: {title}")
    return "\n".join(content)

# --- Ana program ---
if __name__ == "__main__":
    playlist = generate_m3u(MATCH_PAGES)
    with open("StreamedSU.m3u8", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("🎉 Playlist oluşturuldu: StreamedSU.m3u8")

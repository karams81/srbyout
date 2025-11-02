# auto_m3u_builder.py
# Python 3
import requests
import re

# Buraya maç sayfası URL'lerini ekle
MATCH_PAGES = [
    "https://streamed.pk/embed/football/xyz123",  # örnek sayfa
    "https://streamed.pk/embed/basketball/abc456"
]

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

def find_m3u8_in_content(content):
    pattern = r'(https?://[^\'" ]+\.m3u8[^\'" ]*)'
    match = re.search(pattern, content)
    return match.group(1) if match else None

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

def generate_m3u(urls):
    content = ["#EXTM3U"]
    for url in urls:
        m3u8 = fetch_m3u8_from_page(url.get("page_url"))
        if m3u8:
            title = url.get("title", "Untitled")
            category = url.get("category", "General")
            logo = url.get("logo", "")
            tv_id = TV_IDS.get(category, "General.Dummy.us")
            content.append(f'#EXTINF:-1 tvg-id="{tv_id}" tvg-name="{title}" tvg-logo="{logo}" group-title="{category}",{title}')
            content.append(m3u8)
            print(f"✅ Bulundu: {title}")
        else:
            print(f"⚠️ M3U8 bulunamadı: {url.get('title', 'Untitled')}")
    return "\n".join(content)

if __name__ == "__main__":
    playlist = generate_m3u(MATCH_PAGES)
    with open("StreamedSU.m3u8", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("🎉 Playlist oluşturuldu: StreamedSU.m3u8")

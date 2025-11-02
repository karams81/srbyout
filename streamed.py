import requests
import re
from pprint import pprint

CUSTOM_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Referer": "https://embedsports.top/",
    "Origin": "https://embedsports.top"
}

def get_matches(endpoint="live"):
    url = f"https://streamed.pk/api/matches/{endpoint}"
    print(f"📡 Fetching {endpoint} matches from API...")
    try:
        r = requests.get(url, headers=CUSTOM_HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        print(f"✅ {len(data)} matches found.")
        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def get_stream_embed_url(source):
    try:
        src_name = source.get('source')
        src_id = source.get('id')
        if not src_name or not src_id:
            return None
        api_url = f"https://streamed.pk/api/stream/{src_name}/{src_id}"
        r = requests.get(api_url, headers=CUSTOM_HEADERS, timeout=10)
        r.raise_for_status()
        js = r.json()
        if js and js[0].get('embedUrl'):
            return js[0]['embedUrl']
    except Exception as e:
        print(f"⚠️ get_stream_embed_url hata: {e}")
    return None

def find_m3u8_in_content(text):
    patterns = [
        r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)',
        r'source:\s*["\'](https?://[^\'"]+\.m3u8[^\'"]*)["\']',
        r'file:\s*["\'](https?://[^\'"]+\.m3u8[^\'"]*)["\']'
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)
    return None

def extract_m3u8_from_embed(embed_url):
    if not embed_url:
        return None
    try:
        print(f"  🌐 Embed: {embed_url}")
        r = requests.get(embed_url, headers=CUSTOM_HEADERS, timeout=15)
        r.raise_for_status()
        return find_m3u8_in_content(r.text)
    except Exception as e:
        print(f"⚠️ extract_m3u8 hata: {e}")
        return None

def main():
    matches = get_matches("live")
    if not matches:
        print("⚠️ No live matches found.")
        return

    lines = ["#EXTM3U"]
    found = 0

    for match in matches[:10]:  # ilk 10 maçı test edelim
        title = match.get("title", "Untitled")
        print(f"\n⚽ {title}")
        for src in match.get("sources", []):
            embed = get_stream_embed_url(src)
            if not embed:
                continue
            m3u8 = extract_m3u8_from_embed(embed)
            if m3u8:
                lines.append(f'#EXTINF:-1,{title}')
                lines.append(m3u8)
                print(f"  ✅ M3U8 bulundu: {m3u8}")
                found += 1
                break

    if found:
        with open("StreamedSU.m3u8", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\n💾 {found} adet yayın bulundu, StreamedSU.m3u8 oluşturuldu.")
    else:
        print("\n⚠️ Hiçbir .m3u8 bağlantısı bulunamadı.")

if __name__ == "__main__":
    main()

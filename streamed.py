import requests
import sys
import re
import concurrent.futures

# Fallback logolar
FALLBACK_LOGOS = {
    "american-football": "http://drewlive24.duckdns.org:9000/Logos/Am-Football2.png",
    "football":          "https://external-content.duckduckgo.com/iu/?u=https://i.imgur.com/RvN0XSF.png",
    "fight":             "http://drewlive24.duckdns.org:9000/Logos/Combat-Sports.png",
    "basketball":        "http://drewlive24.duckdns.org:9000/Logos/Basketball5.png",
    "motor sports":      "http://drewlive24.duckdns.org:9000/Logos/Motorsports3.png",
    "darts":             "http://drewlive24.duckdns.org:9000/Logos/Darts.png"
}

# API istekleri için header
CUSTOM_HEADERS = {
    "Origin": "https://embedsports.top",
    "Referer": "https://embedsports.top/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

# TV ID mapping
TV_IDS = {
    "Baseball": "MLB.Baseball.Dummy.us",
    "Fight": "PPV.EVENTS.Dummy.us",
    "American Football": "NFL.Dummy.us",
    "Afl": "AUS.Rules.Football.Dummy.us",
    "Football": "Soccer.Dummy.us",
    "Basketball": "Basketball.Dummy.us",
    "Hockey": "NHL.Hockey.Dummy.us",
    "Tennis": "Tennis.Dummy.us",
    "Darts": "Darts.Dummy.us",
    "Motor Sports": "Racing.Dummy.us"
}

# API’den maçları al
def get_matches(endpoint="all"):
    url = f"https://streamed.pk/api/matches/{endpoint}"
    try:
        print(f"📡 Fetching {endpoint} matches from the API...")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        print(f"✅ Successfully fetched {endpoint} matches.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {endpoint} matches: {e}", file=sys.stderr)
        return []

# Embed URL’den .m3u8 çıkar
def extract_m3u8_from_embed(embed_url):
    if not embed_url:
        return None
    try:
        # Eğer embed URL doğrudan .m3u8 ise
        if ".m3u8" in embed_url:
            return embed_url
        # Yoksa sayfayı çekip arama yap
        response = requests.get(embed_url, headers=CUSTOM_HEADERS, timeout=15)
        response.raise_for_status()
        patterns = [
            r'source:\s*["\'](https?://[^\'"]+\.m3u8?[^\'"]*)["\']',
            r'file:\s*["\'](https?://[^\'"]+\.m3u8?[^\'"]*)["\']',
            r'hlsSource\s*=\s*["\'](https?://[^\'"]+\.m3u8?[^\'"]*)["\']',
            r'src\s*:\s*["\'](https?://[^\'"]+\.m3u8?[^\'"]*)["\']',
            r'["\'](https?://[^\'"]+\.m3u8?[^\'"]*)["\']'
        ]
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)
    except requests.RequestException:
        pass
    return None

# Logo doğrulama
def validate_logo(url, category):
    cat = (category or "").lower().replace('-', ' ').strip()
    category_key = next((key for key in FALLBACK_LOGOS if key.lower() == cat), None)
    fallback = FALLBACK_LOGOS.get(category_key)

    if url:
        try:
            resp = requests.head(url, timeout=5, allow_redirects=True)
            if resp.status_code in (200, 302):
                return url
        except requests.RequestException:
            pass
    return fallback

# Maç için logo oluştur
def build_logo_url(match):
    api_category = (match.get('category') or '').strip()
    logo_url = None

    teams = match.get('teams') or {}
    for side in ['away', 'home']:
        team = teams.get(side, {})
        badge = team.get('badge') or team.get('id')
        if badge:
            logo_url = f"https://streamed.pk/api/images/badge/{badge}.webp"
            break

    if not logo_url and match.get('poster'):
        poster = match['poster']
        logo_url = f"https://streamed.pk/api/images/proxy/{poster}.webp"

    if logo_url:
        logo_url = re.sub(r'(https://streamed\.pk/api/images/proxy/)+', 'https://streamed.pk/api/images/proxy/', logo_url)
        logo_url = re.sub(r'\.webp\.webp$', '.webp', logo_url)

    logo_url = validate_logo(logo_url, api_category)
    return logo_url, api_category

# Maçı işle
def process_match(match):
    title = match.get('title', 'Untitled Match')
    sources = match.get('sources', [])
    for source in sources:
        embed_url = source.get('embedUrl') or source.get('url') or source.get('id')
        if embed_url:
            m3u8 = extract_m3u8_from_embed(embed_url)
            if m3u8:
                return match, m3u8
    return match, None

# M3U oluştur
def generate_m3u8():
    all_matches = get_matches("all")
    live_matches = get_matches("live")
    matches = all_matches + live_matches

    if not matches:
        return "#EXTM3U\n#EXTINF:-1,No Matches Found\n"

    content = ["#EXTM3U"]
    success = 0

    vlc_header_lines = [
        f'#EXTVLCOPT:http-origin={CUSTOM_HEADERS["Origin"]}',
        f'#EXTVLCOPT:http-referrer={CUSTOM_HEADERS["Referer"]}',
        f'#EXTVLCOPT:user-agent={CUSTOM_HEADERS["User-Agent"]}'
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_match, m): m for m in matches}
        for future in concurrent.futures.as_completed(futures):
            match, url = future.result()
            title = match.get('title', 'Untitled Match')
            if url:
                logo, cat = build_logo_url(match)
                display_cat = cat.replace('-', ' ').title() if cat else "General"
                tv_id = TV_IDS.get(display_cat, "General.Dummy.us")

                content.append(f'#EXTINF:-1 tvg-id="{tv_id}" tvg-name="{title}" tvg-logo="{logo}" group-title="StreamedSU - {display_cat}",{title}')
                content.extend(vlc_header_lines)
                content.append(url)
                success += 1
                print(f"  ✅ {title} ({logo}) TV-ID: {tv_id}")

    print(f"🎉 Found {success} working streams.")
    return "\n".join(content)

if __name__ == "__main__":
    playlist = generate_m3u8()
    try:
        with open("StreamedSU.m3u8", "w", encoding="utf-8") as f:
            f.write(playlist)
        print("💾 Playlist saved successfully.")
    except IOError as e:
        print(f"⚠️ Error saving file: {e}")
        print(playlist)

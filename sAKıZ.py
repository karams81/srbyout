import requests
import re
import sys
import yaml

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# YAML dosyasını oku
with open("sAKıZ.yml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

KANALLAR = data["kanallar"]

def siteyi_bul():
    print(f"\n{GREEN}[*] Site aranıyor...{RESET}")
    for i in range(1400, 1954):
        url = f"https://trgoals{i}.xyz/"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                if "channel.html?id=" in r.text:
                    print(f"{GREEN}[OK] Yayın bulundu: {url}{RESET}")
                    return url
                else:
                    print(f"{YELLOW}[-] {url} yayında ama yayın linki yok.{RESET}")
        except requests.RequestException:
            print(f"{RED}[-] {url} erişilemedi.{RESET}")
    return None

def find_baseurl(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return None
    match = re.search(r'baseurl\s*[:=]\s*["\']([^"\']+)["\']', r.text)
    if match:
        return match.group(1)
    return None

def generate_m3u(base_url, referer, user_agent):
    lines = ["#EXTM3U"]
    for idx, k in enumerate(KANALLAR, start=1):
        name = k["kanal_adi"]
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{name}",{name}')
        lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        lines.append(base_url + k["dosya"])
        print(f"  ✔ {idx:02d}. {name}")
    return "\n".join(lines)

if __name__ == "__main__":
    site = siteyi_bul()
    if not site:
        print(f"{RED}[HATA] Yayın yapan site bulunamadı.{RESET}")
        sys.exit(1)

    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    base_url = find_baseurl(channel_url)
    if not base_url:
        print(f"{RED}[HATA] Base URL bulunamadı.{RESET}")
        sys.exit(1)

    playlist = generate_m3u(base_url, site, "Mozilla/5.0")
    with open("sAKıZ.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"{GREEN}[OK] Playlist oluşturuldu: sAKıZ.m3u{RESET}")


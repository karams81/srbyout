import requests
import re

# M3U içeriği
m3u_content = "#EXTM3U\n"

# HTTP header'ları
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://google.com/"
}

# Domain arama
base = "https://trgoals"
domain = ""

print("Domain taranıyor...")

for i in range(1393, 2101):
    test_domain = f"{base}{i}.xyz"
    try:
        response = requests.get(test_domain, timeout=2, allow_redirects=True, headers=headers)
        if response.status_code in [200, 301, 302]:
            domain = test_domain
            print(f"Bulunan domain: {domain}")
            break
    except:
        pass

if not domain:
    print("Çalışır bir domain bulunamadı.")
    exit()

# VLC referer bu domain olsun (istersen sabit bırakabiliriz)
vlc_referer = domain + "/"

# Kanal ID’leri
channel_ids = {
    "yayinzirve":"beIN Sports 1 ☪️","yayininat":"beIN Sports 1 ⭐","yayin1":"beIN Sports 1 ♾️",
    "yayinb2":"beIN Sports 2","yayinb3":"beIN Sports 3","yayinb4":"beIN Sports 4",
    "yayinb5":"beIN Sports 5","yayinbm1":"beIN Sports 1 Max","yayinbm2":"beIN Sports 2 Max",
    "yayinss":"Saran Sports 1","yayinss2":"Saran Sports 2","yayint1":"Tivibu Sports 1",
    "yayint2":"Tivibu Sports 2","yayint3":"Tivibu Sports 3","yayint4":"Tivibu Sports 4",
    "yayinsmarts":"Smart Sports","yayinsms2":"Smart Sports 2","yayintrtspor":"TRT Spor",
    "yayintrtspor2":"TRT Spor 2","yayinas":"A Spor","yayinatv":"ATV","yayintv8":"TV8",
    "yayintv85":"TV8.5","yayinnbatv":"NBA TV","yayinex1":"Tâbii 1","yayinex2":"Tâbii 2",
    "yayinex3":"Tâbii 3","yayinex4":"Tâbii 4","yayinex5":"Tâbii 5","yayinex6":"Tâbii 6",
    "yayinex7":"Tâbii 7","yayinex8":"Tâbii 8"
}

print("Kanallar işleniyor...")

for channel_id, channel_name in channel_ids.items():
    try:
        # Kanal sayfasını çek
        channel_url = f"{domain}/channel.html?id={channel_id}"
        r = requests.get(channel_url, headers=headers, timeout=4)

        # baseurl bul
        match = re.search(r'const baseurl = "(.*?)"', r.text)
        if not match:
            print(f"⚠ Baseurl bulunamadı: {channel_id}")
            continue

        baseurl = match.group(1)
        full_url = f"{baseurl}{channel_id}.m3u8"

        # ✔ VLC için özel header satırları
        m3u_content += (
            f'#EXTINF:-1 tvg-logo="https://i.hizliresim.com/ska5t9e.jpg" '
            f'group-title="TURKIYE DEATHLESS", {channel_name}\n'
        )
        m3u_content += '#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)\n'
        m3u_content += f'#EXTVLCOPT:http-referer={vlc_referer}\n'
        m3u_content += f"{full_url}\n"

        print(f"✔ {channel_name} eklendi")
    
    except Exception as e:
        print(f"⚠ Hata: {channel_id} ({e})")

# Kaydet
with open("goals.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("\ngoals.m3u başarıyla oluşturuldu!")

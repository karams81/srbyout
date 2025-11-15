import requests
import time

API = "https://analyticsjs.sbs/load/yayinlink.php?id="
START = 1
END = 1000

def get_stream(id):
    try:
        r = requests.get(API + str(id), timeout=8)
        r.raise_for_status()
        data = r.json()

        if "deismackanal" in data:
            url = data["deismackanal"]
            if url and "m3u8" in url:
                return url
    except:
        return None
    return None


def main():
    print("🚀 Otomatik M3U Tarama Başladı")
    print(f"🔍 {START} → {END} arası ID taranacak...\n")

    playlist = []

    for i in range(START, END + 1):
        print(f"ID {i} taranıyor...", end="\r")

        url = get_stream(i)

        if url:
            print(f"\n✔ Yayın bulundu: ID {i} → {url}")
            playlist.append((i, url))

        time.sleep(0.3)  # sunucuyu yormamak için

    print("\n\n📁 M3U oluşturuluyor...")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for idnum, link in playlist:
            f.write(f"#EXTINF:-1,Kanal {idnum}\n")
            f.write(f"{link}\n\n")

    print(f"🎉 İşlem tamamlandı! {len(playlist)} adet yayın bulundu.")
    print("📄 Dosya: playlist.m3u")


if __name__ == "__main__":
    main()

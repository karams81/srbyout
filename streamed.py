# streamed_simple.py

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

# --- Buraya hazır M3U8 linklerini ekle ---
MATCHES = [
    {
        "title": "Indianapolis Colts vs Pittsburgh Steelers",
        "category": "American Football",
        "logo": "https://streamed.pk/api/Logos/NFL.png",
        "m3u8": "https://lb9.strmd.top/secure/dShpNuOYDhhOoPeJVUdynvzbYKGifRPr/charlie/stream/indianapolis-colts-vs-pittsburgh-steelers-1629468383/1/playlist.m3u8"
    },
    # İstersen buraya başka maçları da ekleyebilirsin
]

def generate_m3u(matches):
    content = ["#EXTM3U"]
    for m in matches:
        tv_id = TV_IDS.get(m["category"], "General.Dummy.us")
        content.append(
            f'#EXTINF:-1 tvg-id="{tv_id}" tvg-name="{m["title"]}" tvg-logo="{m["logo"]}" group-title="{m["category"]}",{m["title"]}'
        )
        content.append(m["m3u8"])
        print(f"✅ Eklendi: {m['title']}")
    return "\n".join(content)

if __name__ == "__main__":
    playlist = generate_m3u(MATCHES)
    with open("StreamedSU.m3u8", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("🎉 Playlist oluşturuldu: StreamedSU.m3u8")

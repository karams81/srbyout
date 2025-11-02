# m3u_builder.py
# Python 3

M3U_LINKS = [
    {
        "title": "Indianapolis Colts vs Pittsburgh Steelers",
        "category": "American Football",
        "logo": "https://streamed.pk/api/Logos/NFL.png",
        "url": "https://lb9.strmd.top/secure/dShpNuOYDhhOoPeJVUdynvzbYKGifRPr/charlie/stream/indianapolis-colts-vs-pittsburgh-steelers-1629468383/1/playlist.m3u8"
    },
    # Buraya diğer maç linklerini ekleyebilirsin
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

def generate_m3u(links):
    content = ["#EXTM3U"]
    for item in links:
        title = item.get("title", "Untitled Match")
        url = item.get("url")
        logo = item.get("logo", "")
        category = item.get("category", "General")
        tv_id = TV_IDS.get(category, "General.Dummy.us")

        content.append(f'#EXTINF:-1 tvg-id="{tv_id}" tvg-name="{title}" tvg-logo="{logo}" group-title="{category}",{title}')
        content.append(url)

    return "\n".join(content)

if __name__ == "__main__":
    playlist = generate_m3u(M3U_LINKS)
    with open("StreamedSU.m3u8", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("✅ Playlist oluşturuldu: StreamedSU.m3u8")

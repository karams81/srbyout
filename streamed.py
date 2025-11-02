import requests
from pprint import pprint

def test_streamed_api():
    url = "https://streamed.pk/api/matches/live"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
        "Referer": "https://embedsports.top/",
        "Origin": "https://embedsports.top"
    }

    try:
        print(f"📡 {url} adresinden veriler çekiliyor...")
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
        print(f"✅ {len(data)} canlı maç bulundu.\n")

        if not data:
            print("⚠️ Hiç canlı maç bulunamadı.")
            return

        # İlk 3 maçı gösterelim
        for m in data[:3]:
            pprint({
                "title": m.get("title"),
                "category": m.get("category"),
                "sources": m.get("sources")
            })
            print("-" * 60)

    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

if __name__ == "__main__":
    test_streamed_api()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import argparse
import logging

# ----------------------------
# Ayarlar
# ----------------------------
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# ----------------------------
# Fonksiyonlar
# ----------------------------
def aktif_domain_bul():
    """dizi20.life ve dizi21.life arasından aktif olanı döndürür"""
    for domain in ["https://dizi20.life", "https://dizi21.life"]:
        try:
            r = requests.get(domain, timeout=5)
            if r.status_code == 200:
                logging.info(f"🌐 Aktif domain bulundu: {domain}")
                return domain
        except requests.RequestException:
            continue
    logging.error("Hiçbir aktif domain bulunamadı.")
    return None

def kategori_tara(base_url, kategori):
    """Belirtilen kategori sayfasındaki içerikleri döndürür"""
    url = f"{base_url}/{kategori}"
    try:
        r = requests.get(url)
        if r.status_code != 200:
            logging.warning(f"{url} sayfasına erişilemedi.")
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        # Örnek: içerikler 'a' tagleri ile listeleniyor
        links = [a['href'] for a in soup.find_all('a', href=True)]
        logging.info(f"{url} içinde {len(links)} içerik bulundu.")
        return links
    except Exception as e:
        logging.error(f"Hata: {e}")
        return []

def playlist_olustur(dizinler, output_file):
    """M3U playlist oluşturur"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for link in dizinler:
            f.write(f"{link}\n")
    logging.info(f"✅ Playlist oluşturuldu: {output_file}")

# ----------------------------
# Ana Fonksiyon
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Dizi/Film playlist oluşturucu")
    parser.add_argument("--output", default="playlist.m3u", help="Çıktı dosyası")
    parser.add_argument("--verbose", action="store_true", help="Detaylı log")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    base_url = aktif_domain_bul()
    if not base_url:
        return

    toplam_icerik = []
    for kategori in ["diziler", "filmler"]:
        icerikler = kategori_tara(base_url, kategori)
        toplam_icerik.extend(icerikler)

    playlist_olustur(toplam_icerik, args.output)

if __name__ == "__main__":
    main()

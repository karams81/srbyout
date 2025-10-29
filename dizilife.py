#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging
import sys
import argparse
import time
from urllib.parse import urlparse

# --- Renkli log formatı ---
class RenkliFormatter(logging.Formatter):
    renkler = {
        logging.DEBUG: "\033[90m",   # Gri
        logging.INFO: "\033[92m",    # Yeşil
        logging.WARNING: "\033[93m", # Sarı
        logging.ERROR: "\033[91m",   # Kırmızı
        logging.CRITICAL: "\033[95m" # Mor
    }
    son = "\033[0m"

    def format(self, record):
        renk = self.renkler.get(record.levelno, self.son)
        tarih = f"[{self.formatTime(record, '%H:%M:%S')}]"
        return f"{renk}{tarih} {record.levelname:<8} {record.getMessage()}{self.son}"

# --- Argümanlar ---
parser = argparse.ArgumentParser(description="DiziLife scraper - M3U playlist oluşturucu")
parser.add_argument("--verbose", action="store_true", help="Detaylı log çıktısı")
parser.add_argument("--output", default="playlist.m3u", help="Çıktı dosyası adı")
args = parser.parse_args()

# --- Logging ayarı ---
log_seviyesi = logging.DEBUG if args.verbose else logging.INFO
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(RenkliFormatter())
logging.basicConfig(level=log_seviyesi, handlers=[handler])
log = logging.getLogger(__name__)

# --- Otomatik aktif domain tespiti ---
def aktif_domain_bul():
    """dizi20.life, dizi21.life, dizi22.life gibi domainleri test ederek çalışanı bulur"""
    for i in range(20, 30):
        domain = f"https://dizi{i}.life"
        try:
            r = requests.get(domain, timeout=5, allow_redirects=True)
            if r.status_code == 200:
                aktif = urlparse(r.url).scheme + "://" + urlparse(r.url).netloc
                log.info(f"🌐 Aktif domain bulundu: {aktif}")
                return aktif
        except requests.RequestException:
            log.debug(f"{domain} aktif değil.")
    log.error("Hiçbir aktif domain bulunamadı!")
    sys.exit(1)

BASE_URL = aktif_domain_bul()
session = requests.Session()

# --- Yardımcı fonksiyonlar ---
def get_page(url):
    """Sayfayı indirir ve yönlendirmeleri takip eder."""
    try:
        log.debug(f"GET {url}")
        response = session.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()
        if response.url != url:
            log.debug(f"Yönlendirildi: {response.url}")
        return response.text
    except requests.RequestException as e:
        log.error(f"Bağlantı hatası: {url} ({e})")
        return None

def parse_links(html):
    """Sayfadaki dizi bağlantılarını çeker."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/dizi/" in href or "/film/" in href:
            links.append(href)
    return sorted(set(links))

# --- Ana işlem ---
def main():
    log.info("Manuel URL sağlanmadı, kategoriler otomatik taranıyor...")

    kategori_url = [f"{BASE_URL}/diziler", f"{BASE_URL}/filmler"]
    tum_linkler = []

    for kategori in kategori_url:
        log.debug(f"Kategori taranıyor: {kategori}")
        html = get_page(kategori)
        if html:
            links = parse_links(html)
            log.info(f"{kategori} içinde {len(links)} içerik bulundu.")
            tum_linkler.extend(links)

    tum_linkler = sorted(set(tum_linkler))
    log.info(f"Toplam {len(tum_linkler)} içerik sayfası bulundu.")

    # Playlist dosyasını oluştur
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for link in tum_linkler:
            f.write(f"#EXTINF:-1,{link.split('/')[-1]}\n")
            full_url = link if link.startswith("http") else f"{BASE_URL}{link}"
            f.write(f"{full_url}\n")
            time.sleep(0.05)

    log.info(f"✅ Playlist oluşturuldu: {args.output}")

# --- Giriş noktası ---
if __name__ == "__main__":
    main()

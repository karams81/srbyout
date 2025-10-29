
---

# `dizilife.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dizilife.py
Basit, güvenli bir scraper örneği:
- Otomatik domain tespiti (dizi20..dizi40)
- --local ile yerel HTML dosyasından çalışma
- Esnek link parse etme
- .m3u playlist oluşturma
"""

import argparse
import logging
import sys
import time
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from typing import List, Optional

# ---------------------
# Logging (renkli)
# ---------------------
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
        mesaj = super().format(record)
        # only include the message part to keep format predictable
        return f"{renk}{tarih} {record.levelname:<8} {record.getMessage()}{self.son}"

# ---------------------
# Argparse
# ---------------------
parser = argparse.ArgumentParser(description="DiziLife scraper - M3U playlist oluşturucu (yerel test destekli)")
parser.add_argument("--verbose", action="store_true", help="Detaylı log çıktısı")
parser.add_argument("--output", default="playlist.m3u", help="Çıktı dosyası adı")
parser.add_argument("--local", help="Yerel HTML dosyası (tarayıcıda kaydedilmiş) ile çalış")
parser.add_argument("--domain-start", type=int, default=20, help="Domain test aralığı başlangıcı (vars:20)")
parser.add_argument("--domain-end", type=int, default=40, help="Domain test aralığı bitişi (vars:40)")
args = parser.parse_args()

log_level = logging.DEBUG if args.verbose else logging.INFO
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(RenkliFormatter())
logging.basicConfig(level=log_level, handlers=[handler])
log = logging.getLogger(__name__)

# ---------------------
# Session & headers
# ---------------------
session = requests.Session()
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
}

# ---------------------
# Domain tespiti
# ---------------------
def aktif_domain_bul(start: int = 20, end: int = 40, timeout: int = 5) -> Optional[str]:
    """
    dizi{start}.life ... dizi{end}.life aralığını test eder.
    İlk 200 OK dönen domain'in scheme+netloc kısmını döner.
    """
    log.debug(f"Domain aralığı aranıyor: dizi{start}.life .. dizi{end - 1}.life")
    for i in range(start, end):
        domain = f"https://dizi{i}.life"
        try:
            r = session.get(domain, timeout=timeout, allow_redirects=True, headers=DEFAULT_HEADERS)
            log.debug(f"GET {domain} -> {r.status_code} ({r.url})")
            if r.status_code == 200:
                parsed = urlparse(r.url)
                aktif = f"{parsed.scheme}://{parsed.netloc}"
                return aktif
        except requests.RequestException as e:
            log.debug(f"{domain} erişilemedi: {e}")
    return None

# ---------------------
# HTML alma (web veya local)
# ---------------------
def get_page(url: str) -> Optional[str]:
    try:
        log.debug(f"GET {url}")
        r = session.get(url, timeout=10, allow_redirects=True, headers=DEFAULT_HEADERS)
        r.raise_for_status()
        if r.url != url:
            log.debug(f"Yönlendirildi: {r.url}")
        return r.text
    except requests.RequestException as e:
        log.error(f"Bağlantı hatası: {url} ({e})")
        return None

def get_local_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        log.error(f"Yerel dosya okunamadı: {path} ({e})")
        return None

# ---------------------
# Link parse etme
# ---------------------
def parse_links(html: str, base_url: str) -> List[str]:
    """
    HTML içinden dizi/film bağlantılarını esnekçe yakalar.
    base_url ile tam URL'ler oluşturulur.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = []
    keywords = ["dizi", "film", "series", "konusanlar", "episode", "bolum"]
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        # Basit filtre: anahtar kelimelerden herhangi biri geçiyorsa değerlendir
        if any(k in href.lower() for k in keywords):
            # Normalize et
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = base_url.rstrip("/") + href
            elif not href.startswith("http"):
                href = base_url.rstrip("/") + "/" + href.lstrip("/")
            links.append(href)
    # unique ve sıralı
    return sorted(set(links))

# ---------------------
# Main
# ---------------------
def main():
    # Eğer local modu verilmişse onu tercih et
    if args.local:
        log.info("🔎 Yerel HTML modu etkin: %s", args.local)
        html = get_local_file(args.local)
        if not html:
            log.error("Yerel dosya açılamadı, çıkılıyor.")
            sys.exit(2)
        # base_url'i local dosyaya göre varsayılan kullan
        # (kullanıcı manuel olarak base_url veremez bu sürümde)
        base_url = "https://dizi21.life"
    else:
        log.info("Manuel URL sağlanmadı, kategoriler otomatik taranıyor...")
        aktif = aktif_domain_bul(start=args.domain_start, end=args.domain_end)
        if not aktif:
            log.error("Hiçbir aktif domain bulunamadı! (aralık: %d..%d)", args.domain_start, args.domain_end)
            sys.exit(3)
        base_url = aktif
        # Kategori sayfasını indir
        html = None

    tum_linkler = []

    if args.local and html:
        # local üzerinden parse et
        tum_linkler = parse_links(html, base_url)
        log.info("Yerel dosyadan %d içerik bulundu.", len(tum_linkler))
    else:
        # web mod: kategorileri indir
        kategori_url = [f"{base_url}/diziler", f"{base_url}/filmler"]
        for kategori in kategori_url:
            log.debug(f"Kategori taranıyor: {kategori}")
            html_k = get_page(kategori)
            if not html_k:
                log.warning("Kategori sayfası alınamadı: %s", kategori)
                continue
            # debug için istersen local debug dosyası yazabilirsiniz (opsiyonel)
            # with open("debug.html", "w", encoding="utf-8") as f: f.write(html_k)
            links = parse_links(html_k, base_url)
            log.info("%s içinde %d içerik bulundu.", kategori, len(links))
            tum_linkler.extend(links)

    tum_linkler = sorted(set(tum_linkler))
    log.info("Toplam %d içerik sayfası bulundu.", len(tum_linkler))

    # Playlist oluştur
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for link in tum_linkler:
                title = link.rstrip("/").split("/")[-1] or link
                f.write(f"#EXTINF:-1,{title}\n")
                f.write(f"{link}\n")
                # küçük gecikme, aşırı istekten kaçınmak için
                time.sleep(0.02)
        log.info("✅ Playlist oluşturuldu: %s", args.output)
    except Exception as e:
        log.error("Çıkış dosyası yazılamadı: %s (%s)", args.output, e)
        sys.exit(4)

if __name__ == "__main__":
    main()

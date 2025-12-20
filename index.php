<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

/* =====================
   AYARLAR
===================== */
$headers = [
    'Accept: */*',
    'Accept-Encoding: gzip',
    'Accept-Language: tr-TR,tr;q=0.9',
    'Connection: keep-alive',
    'User-Agent: okhttp/4.12.0'
];

$channels = [
    [ "Name" => "TEST KANAL", "Logo" => "https://example.com/logo.png", "ChannelID" => "test.m3u8" ]
];

/* =====================
   CURL FONKSİYONU
===================== */
function getData($url, $headers, $referer = null) {
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => '',
        CURLOPT_SSL_VERIFYHOST => false,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_HTTPHEADER => array_merge(
            $headers,
            $referer ? ['Referer: ' . $referer] : []
        ),
        CURLOPT_TIMEOUT => 20
    ]);
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}

/* =====================
   DEBUG BAŞLANGIÇ
===================== */
file_put_contents("debug.txt", "Script başladı\n");

/* =====================
   1. ADIM – ANA SAYFA
===================== */
$site = getData("https://netspor.co/", $headers);
file_put_contents("debug.txt", "Ana sayfa length: ".strlen($site)."\n", FILE_APPEND);

if (!$site) {
    file_put_contents("debug.txt", "Ana sayfa boş\n", FILE_APPEND);
    exit;
}

/* =====================
   2. ADIM – JS DOSYASI
===================== */
preg_match('#script src="(.*?)"#', $site, $m);
if (!isset($m[1])) {
    file_put_contents("debug.txt", "script src bulunamadı\n", FILE_APPEND);
    exit;
}

$js = "https://netspor.co/" . ltrim($m[1], '/');
file_put_contents("debug.txt", "JS: $js\n", FILE_APPEND);

/* =====================
   3. ADIM – URL AL
===================== */
$site1 = getData($js, $headers);
preg_match('#"url":\s*"(.*?)"#', $site1, $m);
if (!isset($m[1])) {
    file_put_contents("debug.txt", "url bulunamadı\n", FILE_APPEND);
    exit;
}

$url = "https://netspor.co/" . ltrim($m[1], '/');
file_put_contents("debug.txt", "URL: $url\n", FILE_APPEND);

/* =====================
   4. ADIM – BASEURL
===================== */
$site2 = getData($url, $headers);
preg_match('#baseurls\s*=\s*\[\s*["\']([^"\']+)#', $site2, $m);
if (!isset($m[1])) {
    file_put_contents("debug.txt", "baseurls bulunamadı\n", FILE_APPEND);
    exit;
}

$link = trim($m[1]);
file_put_contents("debug.txt", "BASE LINK: $link\n", FILE_APPEND);

/* =====================
   M3U OLUŞTUR
===================== */
$m3u  = "#EXTM3U\n";

foreach ($channels as $c) {
    $m3u .= "#EXTINF:-1 tvg-name=\"{$c['Name']}\" tvg-logo=\"{$c['Logo']}\",{$c['Name']}\n";
    $m3u .= "#EXTVLCOPT:http-referrer=https://netspor.co/\n";
    $m3u .= "#EXTVLCOPT:http-user-agent=okhttp/4.12.0\n";
    $m3u .= $link . $c['ChannelID'] . "\n\n";
}

file_put_contents("NETSpor.m3u", $m3u);
file_put_contents("debug.txt", "M3U oluşturuldu\n", FILE_APPEND);

echo "OK\n";

<?php
header("Content-Type: application/vnd.apple.mpegurl");
header("Content-Disposition: attachment; filename=NETSpor.m3u");
$Live = $_GET['ID'];
$channels = [
    [ "Number" => "1", "Name" => "beIN SPORTS HD1", "Logo" => "https://digiturkairtv.com/images/channels/beINSPORTSHD1.png", "ChannelID" => "androstreamlivebs1.m3u8" ],
    [ "Number" => "2", "Name" => "beIN SPORTS HD2", "Logo" => "https://digiturkairtv.com/images/channels/beINSPORTSHD2.png", "ChannelID" => "androstreamlivebs2.m3u8" ],
    [ "Number" => "3", "Name" => "beIN SPORTS HD3", "Logo" => "https://digiturkairtv.com/images/channels/beinsports3.png", "ChannelID" => "androstreamlivebs3.m3u8" ],
    [ "Number" => "4", "Name" => "beIN SPORTS HD4", "Logo" => "https://digiturkairtv.com/images/channels/beinsports4.png", "ChannelID" => "androstreamlivebs4.m3u8" ],
    [ "Number" => "5", "Name" => "beIN SPORTS HD5", "Logo" => "https://digiturkairtv.com/images/channels/beinsports5.png", "ChannelID" => "androstreamlivebs5.m3u8" ],
    [ "Number" => "6", "Name" => "beIN SPORTS HD1 MAX", "Logo" => "https://digiturkairtv.com/images/channels/beINSPORTSMAX1.png", "ChannelID" => "androstreamlivebsm1.m3u8" ],
    [ "Number" => "7", "Name" => "beIN SPORTS HD2 MAX", "Logo" => "https://digiturkairtv.com/images/channels/beINSPORTSMAX2.png", "ChannelID" => "androstreamlivebsm2.m3u8" ],
    [ "Number" => "8", "Name" => "S SPORT", "Logo" => "https://yt3.ggpht.com/gvJvmHjz_AD2oWOrKpMHrc6PkrPaf9ZJn714gU1hOYxOh7XWqLbSjwniRy9wXxs0R6vyIFsCivA", "ChannelID" => "androstreamlivess1.m3u8" ],
    [ "Number" => "9", "Name" => "S SPORT 2", "Logo" => "https://yt3.ggpht.com/gvJvmHjz_AD2oWOrKpMHrc6PkrPaf9ZJn714gU1hOYxOh7XWqLbSjwniRy9wXxs0R6vyIFsCivA", "ChannelID" => "androstreamlivess2.m3u8" ],
    [ "Number" => "10", "Name" => "TivibuSPOR", "Logo" => "https://yt3.ggpht.com/VfKm_ajwsvkrsG4O6-5m1-LBAo8mgiAz4htzprv1zcF5liZ1Zgz5ANNbU_PYI8CE173sFIOqtQ", "ChannelID" => "androstreamlivets.m3u8" ],
    [ "Number" => "11", "Name" => "TivibuSPOR 1", "Logo" => "https://yt3.ggpht.com/VfKm_ajwsvkrsG4O6-5m1-LBAo8mgiAz4htzprv1zcF5liZ1Zgz5ANNbU_PYI8CE173sFIOqtQ", "ChannelID" => "androstreamlivets1.m3u8" ],
    [ "Number" => "12", "Name" => "TivibuSPOR 2", "Logo" => "https://yt3.ggpht.com/VfKm_ajwsvkrsG4O6-5m1-LBAo8mgiAz4htzprv1zcF5liZ1Zgz5ANNbU_PYI8CE173sFIOqtQ", "ChannelID" => "androstreamlivets2.m3u8" ],
    [ "Number" => "13", "Name" => "TivibuSPOR 3", "Logo" => "https://yt3.ggpht.com/VfKm_ajwsvkrsG4O6-5m1-LBAo8mgiAz4htzprv1zcF5liZ1Zgz5ANNbU_PYI8CE173sFIOqtQ", "ChannelID" => "androstreamlivets3.m3u8" ],
    [ "Number" => "14", "Name" => "TivibuSPOR 4", "Logo" => "https://yt3.ggpht.com/VfKm_ajwsvkrsG4O6-5m1-LBAo8mgiAz4htzprv1zcF5liZ1Zgz5ANNbU_PYI8CE173sFIOqtQ", "ChannelID" => "androstreamlivets4.m3u8" ],
    [ "Number" => "15", "Name" => "spor SMART", "Logo" => "https://www.dsmart.com.tr/api/v1/public/images/kanallar/SPORSMART.png", "ChannelID" => "androstreamlivesm1.m3u8" ],
    [ "Number" => "16", "Name" => "spor SMART 2", "Logo" => "https://www.dsmart.com.tr/api/v1/public/images/kanallar/SPORSMART2.png", "ChannelID" => "androstreamlivesm2.m3u8" ],
    [ "Number" => "17", "Name" => "IDMAN TV", "Logo" => "https://yt3.ggpht.com/T10TP4qbY584Rx30XlDn_7EPIvo4OsI6wtdlh2UCtQWithOqWNqxiSnhPY3EwX1oM4kevKcTEbI", "ChannelID" => "androstreamliveidm.m3u8" ],
    [ "Number" => "18", "Name" => "CBC SPORT", "Logo" => "https://yt3.googleusercontent.com/OqnOCP8kHegiwb2gHNGsX6okeuYOujMQRoYxIEeWEwni66oDG67FJ6rgboEtmF9f79iQvihG", "ChannelID" => "androstreamlivecbcs.m3u8" ],
    [ "Number" => "19", "Name" => "FBTV", "Logo" => "https://yt3.googleusercontent.com/ytc/AIdro_kG04jzq7wxoRvUmeqFO1zzt6CDop8OltgqJ9E9PXj1PuU", "ChannelID" => "androstreamlivefb.m3u8" ],
    [ "Number" => "20", "Name" => "GS TV", "Logo" => "https://yt3.googleusercontent.com/ytc/AIdro_lBR3MUCWVEF0aBWLfpvDvCnPHSWqTBCyZNEtiXyLSZ2jA", "ChannelID" => "androstreamlivegs.m3u8" ],
    [ "Number" => "21", "Name" => "sportstv", "Logo" => "https://yt3.googleusercontent.com/ytc/AIdro_lKnrGQgvaKuU6UINXvHHq5Fy-Qo8SvCbzXpN6h3rkXug", "ChannelID" => "androstreamlivesptstv.m3u8" ],
    [ "Number" => "22", "Name" => "TRT Spor", "Logo" => "https://yt3.googleusercontent.com/FCzDc31AsTFzobw8Z4QBCc8AGtKgFP4mq28RgbcLJGdVNlE0RoremvEr1XntYHFc6G0dAwU-", "ChannelID" => "androstreamlivetrts.m3u8" ],
    [ "Number" => "23", "Name" => "TRT SPOR Yıldız", "Logo" => "https://yt3.googleusercontent.com/-8Ri3w9lxEPds96rwxSbKvO6hLWNI1_dqIO0T75xAQ9KomwH68sIXycW5hYUEljYbenIhnW1SA", "ChannelID" => "androstreamlivetrtsy.m3u8" ],
    [ "Number" => "24", "Name" => "TRT 1", "Logo" => "https://yt3.ggpht.com/Ar9s9sZNclvmZN1l7GfIdnAQjh_ZkVhGMx6Dy5PHbq2keR9ijkPMFkk9VxZnIEnTf0MrXfSU4g", "ChannelID" => "androstreamlivetrt1.m3u8" ],
    [ "Number" => "25", "Name" => "aSPOR", "Logo" => "https://yt3.ggpht.com/43xh3uEvLl7kAKca-zFauATzT3spixqjb9v-cYBVxBLzbcbVj42iV3Msbpd5zXwN_w7jXdnzFq8", "ChannelID" => "androstreamliveas.m3u8" ],
    [ "Number" => "26", "Name" => "a2", "Logo" => "https://yt3.googleusercontent.com/RZG-XV8AGd-_HWnGIVJtSNurIjUJxtZrb06jwRrrWt1BTTRChGOdz75ATZqaPlS0zQitJdI8Rg", "ChannelID" => "androstreamlivea2.m3u8" ],
    [ "Number" => "27", "Name" => "TJK TV", "Logo" => "https://yt3.googleusercontent.com/ytc/AIdro_nHSKFStnIjdMil38RGvlbpMPATSHd7TjRgKRH88iEV5Y8", "ChannelID" => "androstreamlivetjk.m3u8" ],
    [ "Number" => "28", "Name" => "HT SPOR", "Logo" => "https://yt3.googleusercontent.com/B3IWp1Ke7InBdWs0z8dkXpRlg4J6lQ0ETi8hbMQ64w3uh9RfHTOtU6K7_uLYRbIoA6NteY9a", "ChannelID" => "androstreamliveht.m3u8" ],
    [ "Number" => "29", "Name" => "ATV", "Logo" => "https://yt3.ggpht.com/rGaatci_rjFWnwKiycOnIolZYkXz8SeTNVMz4G_45i_flLh_toDIBKT6ctxlDH8b7vqW4Cc_-XY", "ChannelID" => "androstreamliveatv.m3u8" ],
    [ "Number" => "30", "Name" => "Tv8", "Logo" => "https://yt3.googleusercontent.com/ytc/AIdro_mnwqLdHqFXbkm6QwloGNJ1EX5N3Z8klIpdSF59MRbbLxU", "ChannelID" => "androstreamlivetv8.m3u8" ],
    [ "Number" => "31", "Name" => "Tv8.5", "Logo" => "https://yt3.ggpht.com/mkjHjP6e2h9JykcMntzaTsCXCdNthlLu_EiDKE5_AifSpyLD1qkhCaJaY8g-eYbd_pwApWNfOQ", "ChannelID" => "androstreamlivetv85.m3u8" ],
    [ "Number" => "32", "Name" => "NBA", "Logo" => "https://yt3.ggpht.com/qtn_u6ISz-HvZphchyOE6qFFfA_iu9-8dC8yABZ2E4uAbYbtZci0rki5tQNLdCrfijZkOClRRw", "ChannelID" => "yayinnbatv.m3u8" ],
    [ "Number" => "33", "Name" => "EUROSPORT 1", "Logo" => "https://yt3.ggpht.com/CTYNXpw6_5CzpZbDDVMUIUsn3KwlbPGBW2w2x0Glgftvwj2YpHnCN5Wt2aDbv76eBjn-NqIKqg", "ChannelID" => "androstreamlivees1.m3u8" ],
    [ "Number" => "34", "Name" => "EUROSPORT 2", "Logo" => "https://yt3.ggpht.com/CTYNXpw6_5CzpZbDDVMUIUsn3KwlbPGBW2w2x0Glgftvwj2YpHnCN5Wt2aDbv76eBjn-NqIKqg", "ChannelID" => "androstreamlivees2.m3u8" ],
    [ "Number" => "35", "Name" => "tabii SPOR 1", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb1.m3u8" ],
    [ "Number" => "36", "Name" => "tabii SPOR 2", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb2.m3u8" ],
    [ "Number" => "37", "Name" => "tabii SPOR 3", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb3.m3u8" ],
    [ "Number" => "38", "Name" => "tabii SPOR 4", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb4.m3u8" ],
    [ "Number" => "39", "Name" => "tabii SPOR 5", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb5.m3u8" ],
    [ "Number" => "40", "Name" => "tabii SPOR 6", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb6.m3u8" ],
    [ "Number" => "41", "Name" => "tabii SPOR 7", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb7.m3u8" ],
    [ "Number" => "42", "Name" => "tabii SPOR 8", "Logo" => "https://yt3.ggpht.com/fnTAQELerKbTGtUKO0Iu0irkcVP1z0z-kKG-BdZetLZPK_G9yf8z8PPhIPDBfhmWUQe5Q59BqA", "ChannelID" => "androstreamlivetb8.m3u8" ],
    [ "Number" => "43", "Name" => "EXXEN SPOR 1", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn1.m3u8" ],
    [ "Number" => "44", "Name" => "EXXEN SPOR 2", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn2.m3u8" ],
    [ "Number" => "45", "Name" => "EXXEN SPOR 3", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn3.m3u8" ],
    [ "Number" => "46", "Name" => "EXXEN SPOR 4", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn4.m3u8" ],
    [ "Number" => "47", "Name" => "EXXEN SPOR 5", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn5.m3u8" ],
    [ "Number" => "48", "Name" => "EXXEN SPOR 6", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn6.m3u8" ],
    [ "Number" => "49", "Name" => "EXXEN SPOR 7", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn7.m3u8" ],
    [ "Number" => "50", "Name" => "EXXEN SPOR 8", "Logo" => "https://yt3.googleusercontent.com/UJrEza5owqpIQSdFredj9UqwNvPTEs1rLhfaf8lOxrojMcmM0QVrGm1dAl6bLv1We-3uC7Nq_g", "ChannelID" => "androstreamliveexn8.m3u8" ]
];
$headers = [
    'Accept: */*',
    'Accept-Encoding: gzip',
    'Accept-Language: tr-TR,tr;q=0.9',
    'Connection: keep-alive',
    'User-Agent: okhttp/4.12.0'
];

function getData($url, $headers, $referer = null) {
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_SSL_VERIFYHOST => false,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => '',
        CURLOPT_HTTPHEADER => array_merge(
            $headers,
            $referer ? ['Referer: ' . $referer] : []
        )
    ]);
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}
$site = getData('https://netspor.co/', $headers);
preg_match('#script src="(.*?)"#', $site, $icerik);
$Data = $icerik[1];
$site1 = getData("https://netspor.co/$Data", $headers);
preg_match('#"url": "(.*?)"#', $site1, $icerik);
$Url = $icerik[1];
$site2 = getData("https://netspor.co/$Url", $headers);
preg_match('#var\s+baseurls\s*=\s*\[\s*["\']([^"\']+)["\']\s*,?#s', $site2, $icerik);
$Link = trim($icerik[1]);
echo "#EXTM3U\n";
foreach ($channels as $channel) {
    echo "#EXTINF:-1 tvg-name=\"{$channel['Name']}\" tvg-logo=\"{$channel['Logo']}\",{$channel['Name']}\n";
    echo "#EXTVLCOPT:http-referrer=https://netspor.co/\n";
    echo "#EXTVLCOPT:http-user-agent=okhttp/4.12.0\n";
    echo $Link . $channel['ChannelID'] . "\n\n";
}
?>
# Doğrulama kaydı

## 31 Ekim 2026: tasarım, hareketli görüntü ve rehber görselleri

| Kontrol | Durum | Kanıt ve sınır |
|---|---|---|
| İçerik yapısı | PASS | 15 test. 20 bölüm, 129 madde. Rehber 16 bölüm, 24 şekil, 23 terminal paneli. Eksik şekil dosyası ve etiketsiz panel derlemeyi durduruyor |
| Terminal panelleri | PASS | 14 panel bu makinede çalıştırılan komutların gerçek çıktısı, 9 panel şematik ya da kurgu olarak etiketli. Kişisel veri çıkarıldı |
| Sayfa işlevleri | PASS | 78 tarayıcı kontrolü yerelde (Node sunucusu) ve herkese açık adreste |
| Görsel inceleme | PASS | Her bölümün şekilleri 1280 ve 390 px, açık ve koyu temada ajanlarca, bölüm 5 ayrıca elle incelendi. Animasyonların hareketli hali izlenmedi |
| GitHub CI | PASS | [İçerik kontrolü](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/41186345388), commit `dd7210a` |
| Canlı yayın | PASS | [Pages](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/41186344494). 25 dosya anonim HTTP 200 ve yerel dosyalarla SHA-256 düzeyinde aynı: [kanıt](dogrulama/canli-yayin.json) |
| PDF | PASS | 123 A4 sayfa |

## 30 Ekim 2026: Opus 5.5 ve Projects eklemeleri

| Kontrol | Durum | Kanıt ve sınır |
|---|---|---|
| İçerik yapısı | PASS | 14 test. 20 bölüm, 125 madde, 25 temel, 100 ileri. Rehber 14 bölüm |
| Sayfa işlevleri | PASS | 74 tarayıcı kontrolü yerelde ve herkese açık adreste |
| Ürün iddiaları | PASS | Projects maddeleri claude-projects ve cloud-environments belgeleriyle, 5.7 model-config ve settings-reference ile karşılaştırıldı. Opus 5.5 kaynaklı 3.8, 12.8, 13.7, 16.5 iş akışı önerisidir |
| Canlı özellik denemesi | NOT_RUN | Projects ve model geçişi canlı denenmedi |
| GitHub CI | PASS | [İçerik kontrolü](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/40958918442), commit `b9a2622` |
| Dizin ağaçları (sonraki yayın) | PASS | Commit `0c70cf9`: [CI](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/41034279070), [Pages](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/41034277809). 23 canlı dosya yerelle aynı, 74 tarayıcı kontrolü canlı adreste geçti. PDF 100 sayfa |
| Canlı yayın | PASS | [Pages dağıtımı](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/40958915697). 23 dosya anonim HTTP 200 ve yerel dosyalarla SHA-256 düzeyinde aynı: [kanıt](dogrulama/canli-yayin.json) |
| PDF | PASS | 99 A4 sayfa |

## 29 Ekim 2026 rehber

| Kontrol | Durum | Kanıt ve sınır |
|---|---|---|
| İçerik yapısı | PASS | 14 test. Rehber sayfaları güncel, madde, ek ve bölüm bağlantıları çözülüyor, geçersiz bağlantı reddediliyor |
| Sayfa işlevleri | PASS | 72 tarayıcı kontrolü. 13 bölüm ve içindekiler 1440 ve 320 px'te taşmıyor |
| Ürün iddiaları | PASS | Her bölümün iddiaları yazımda resmî belgeyle karşılaştırıldı, sonra 13 bölüm bir tutarlılık okumasından geçti |
| Alıştırmalar | NOT_RUN | Bölüm 8'deki hook betiği dışında alıştırmalar canlı koşulmadı |
| PDF | PASS | 92 A4 sayfa |
| GitHub CI | PASS | [İçerik kontrolü](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/40909268315), commit `250e3e0` |
| Canlı yayın | PASS | [Pages dağıtımı](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/40909266132). 22 dosya (ana sayfa, PDF, 6 ek, 14 rehber sayfası) anonim HTTP 200 ve yerel dosyalarla SHA-256 düzeyinde aynı: [kanıt](dogrulama/canli-yayin.json) |
| Canlı sayfa işlevleri | PASS | Aynı 72 tarayıcı kontrolü herkese açık adreste de geçti |

## 29 Ekim 2026 güncellemesi

| Kontrol | Durum | Kanıt ve sınır |
|---|---|---|
| İçerik yapısı ve üretilen dosya eşitliği | PASS | 11 test. 113 madde, 25 temel, 88 ileri. Eski kimlikler korunuyor, ek dosyaları güncel |
| Hata yakalayan test | PASS | Geçersiz `[[3.99]]` ek bağlantısı reddediliyor. Test geçerli numarayla bozulunca düştü |
| Sayfa işlevleri | PASS | 44 tarayıcı kontrolü: eski 30'a ek olarak altı ek sayfası, ekten maddeye bağlantı, 1440 ve 320 px taşma. Taşma kontrolü dosya konumları ekinde 320 px'te uzun yolu yakaladı, düzeltildi |
| Görsel inceleme | PASS | Komutlar eki masaüstü, dört ek 320 px, Ekler bölümü, madde 2.7 ve PDF ek sayfaları açılıp bakıldı |
| PDF | PASS | 50 A4 sayfa. Altı ek başlığı metinde var |
| Ürün iddiaları | PASS | Yeni maddeler ve ekler resmî belgeyle karşılaştırıldı. Belgede bulunmayan iddialar yazılmadı |
| Claude özelliklerinin canlı koşumu | NOT_RUN | Yeni maddelerdeki komutlar ve bayraklar bu görevde çalıştırılmadı |
| GitHub CI | PASS | [İçerik kontrolü](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/40902023457), commit `0dc3fe5` |
| Canlı yayın | PASS | [Pages dağıtımı](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/40902021597). Anonim HTTP 200, HTML, PDF ve altı ek yerel dosyalarla SHA-256 düzeyinde aynı: [kanıt](dogrulama/canli-yayin.json) |
| Canlı sayfa işlevleri | PASS | Aynı 44 tarayıcı kontrolü herkese açık adreste de geçti: [sonuçlar](dogrulama/browser-live.json) |

## 21 Ekim 2026

Tarih: 21 Ekim 2026. Hedef: mevcut GitHub deposu ve GitHub Pages sayfası.

| Kontrol | Durum | Kanıt ve sınır |
|---|---|---|
| İçerik yapısı ve üretilen dosya eşitliği | PASS | 8 test; 107 madde, 25 temel, 82 ileri; eski 97 kimlik korunuyor |
| Hata yakalayan testler | PASS | Eksik doğrulama alanı, yinelenen bölüm ve bilinmeyen kaynak reddediliyor |
| Sayfa işlevleri | PASS | Chrome 155 ile 30 kontrol: filtre, arama, kalıcılık, sıfırlama, JSON aktarımı, hata durumları, tema, kopyalama ve klavye |
| Öğretici hook betiği | PASS | 3 sahte girdi: izinli, engelli, bozuk JSON; canlı Claude entegrasyonu değildir |
| Önceki temizleme hatası | FAIL → PASS | Eski sayfada ilk tık görünür madde sayısını 97’den 0’a düşürdü; yeni testte 107 kalıyor |
| Görsel inceleme | PASS | 1440 px açık/koyu masaüstü, 390/320 px mobil, kaynak ve örnek alanı |
| Resmî kaynak erişimi | PASS | 26 kaynak; kaynak bilgisi ve hash kayıtlı |
| PDF | PASS | 28 A4 sayfa; bütün madde başlıkları metinde mevcut, sayfa görselleri incelendi |
| Yerel Claude CLI | PASS | `claude --version`: 2.1.284; `--help` incelendi |
| Claude özelliklerinin canlı koşumu | NOT_RUN | Hook entegrasyonu, model/ajan çağrıları, sandbox, MCP, bulut/Desktop zamanlama ve mobil araç davranışları bu görevde çalıştırılmadı |
| Diğer tarayıcılar / ekran okuyucu | NOT_RUN | Safari, Firefox ve VoiceOver çalıştırılmadı |
| Canlı yayın | PASS | Pages yayını başarılı; anonim HTTP 200 ile HTML ve PDF yerel dosyalarla SHA-256 düzeyinde eşleşti |
| Canlı sayfa işlevleri | PASS | Aynı 30 tarayıcı kontrolü herkese açık adreste de geçti |
| GitHub CI | PASS | İçerik kontrolü GitHub Actions üzerinde de başarılı |

Tarayıcı testinde ilk arama fixture’ı “bellek” sözcüğünün “belleği” biçimiyle eşleşmesini varsaydığı için başarısız oldu. Fixture, amaçlanan Türkçe büyük/küçük harf davranışını sınayacak “OTOMATIK” sorgusuyla düzeltildi; başarısız ilk koşum yerel kanıtta korundu. Bu bir kök-bulma arama motoru değildir.

## Tekrar çalıştırma

```sh
python3 kaynak/yap.py
python3 -m unittest discover -s kaynak -p 'test_*.py' -v
python3 -m http.server 8770 --bind 127.0.0.1
# Ayrı terminal: mevcut Playwright kurulumu ve Chrome/Chromium gerekir.
CHROME_PATH="/uygun/yol/chrome" node kaynak/test_browser.cjs
```

Playwright modülü normal Node çözümlemesiyle veya mevcut kurulumun `NODE_PATH` değişkeniyle bulunmalıdır. Tarayıcı testi kendi geçici profilini kullanır; yerel testte PDF’yi de yeniler. Canlı siteyi sınamak için `TEST_URL` ver; bu mod PDF üretmez. PDF üretiminden sonra görsel denetimi yinele.

[Tarayıcı sonuçları](dogrulama/browser-local.json) · [Kaynak kontrolü](dogrulama/kaynaklar.json)

## Yayın kanıtı

İçerik commit’i: `d6873cd404cc2edc273e400aca4ba84c1198bf66`.

[Anonim HTML/PDF karşılaştırması](dogrulama/canli-yayin.json) · [Canlı tarayıcı sonuçları](dogrulama/browser-live.json) · [İçerik CI](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/39671417993) · [Pages dağıtımı](https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/actions/runs/39671414428).

Sonraki kanıt commit’i yalnız rapor ve sonuç kayıtlarını ekler; HTML/PDF içeriği değişmez.

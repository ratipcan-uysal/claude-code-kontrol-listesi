# Doğrulama kaydı

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

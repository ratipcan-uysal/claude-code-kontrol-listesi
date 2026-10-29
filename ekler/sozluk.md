# Terimler sözlüğü

_Belge kontrolü: 29 Ekim 2026_

Terimler ilk geçtiği maddede kısaca tanımlanır. Bu sayfa hepsini bir arada verir. Her satır terimin bu listede ne anlama geldiğini söyler. Ürün davranışının tamamı için ilgili resmî belgeye bak.

## Oturum ve bağlam

| Terim | Bu listede ne demek |
|---|---|
| Oturum | Claude ile tek bir konuşma ve onun araç geçmişi. Kapatıp açınca konuşma bağlamı sıfırlanır, dosyalar kalır. |
| Bağlam (context) | Modelin o anda görebildiği her şey: mesajlar, okunan dosyalar, araç çıktıları, yüklenen talimatlar. Sınırlıdır ve dolar. |
| Token | Modelin metni işlediği parça. Bağlam ve kullanım token'la ölçülür. Kelimeyle birebir eşleşmez. |
| Sıkıştırma (`/compact`) | Uzayan konuşmanın özetle değiştirilmesi. Yer açar, ayrıntı kaybettirebilir. |
| Checkpoint | Claude'un dosya düzenlemelerinden önce aldığı yerel geri dönüş noktası. Git'in yerini tutmaz. |
| Devir dosyası | Oturum kapanmadan önce durumun yazıldığı dosya. Yeni oturum oradan devam eder. |
| Otomatik bellek | Claude'un oturumlar arasında kendi tuttuğu notlar. Talimat dosyasından ayrıdır, eskiyebilir. |

## Talimat ve ayar

| Terim | Bu listede ne demek |
|---|---|
| CLAUDE.md | Her oturumun başında yüklenen talimat dosyası. Üç düzeyi var: kullanıcı, proje ve alt dizin. |
| `CLAUDE.local.md` | Yalnız bu makinede geçerli proje notu. Git'e girmez. |
| Kural dosyası (`.claude/rules/`) | Yalnız eşleşen dosyalara dokunulunca yüklenen talimat. |
| `settings.json` | İzin, hook, model ve ortam ayarlarının dosyası. Kullanıcı, proje, yerel ve yönetilen katmanları vardır. |
| Yönetilen politika | Kurumun yönettiği ve kullanıcının ezemediği ayar katmanı. |
| Prompt | Claude'a verilen istek metni. |
| Output style | Claude'un cevap üslubunu değiştiren hazır ya da özel ayar. |

## İzin ve güvenlik

| Terim | Bu listede ne demek |
|---|---|
| İzin modu | Claude'un araç kullanmadan önce ne zaman onay soracağını belirleyen mod. Plan modu bunlardan biridir. |
| Allow / ask / deny | İzin kuralının üç sonucu: sormadan izin ver, sor, reddet. |
| Plan modu | Claude'un yalnız okuyup plan yazdığı, dosya değiştirmediği mod. |
| Sandbox | Komutların dosya sistemi ve ağ erişimini işletim sistemi düzeyinde sınırlayan yalıtım. |
| Prompt injection | Okunan sayfa, belge ya da e-postadaki metnin kullanıcı talimatı gibi davranmaya çalışması. |

## Genişletme

| Terim | Bu listede ne demek |
|---|---|
| Hook | Belirli bir olayda (araç öncesi, araç sonrası, oturum başı gibi) otomatik çalışan betik. Modelin kararına bağlı değildir. |
| Skill | Gerektiğinde yüklenen talimat ve dosya paketi. Açıklaması her zaman bağlamdadır, gövdesi yalnız kullanılınca yüklenir. |
| Slash komutu | `/` ile başlayan komut. Bir kısmı yerleşik, bir kısmını skill ve plugin'ler ekler. |
| Alt ajan (subagent) | Kendi bağlamında çalışan ve sonucu ana oturuma özet olarak dönen yardımcı Claude. |
| MCP | Claude'u dış sistemlere (veritabanı, iş takibi, tarayıcı gibi) araç olarak bağlayan açık protokol. |
| Plugin | Skill, ajan, hook ve MCP ayarlarını tek pakette dağıtma biçimi. |
| Statusline | Terminal altında sürekli görünen, kendi betiğinle üretilen durum satırı. |

## Çalışma biçimi

| Terim | Bu listede ne demek |
|---|---|
| Headless (`claude -p`) | Etkileşimsiz koşum. İstek verilir, sonuç metin ya da JSON olarak döner, oturum biter. |
| Effort | Modelin düşünmeye ayıracağı çaba düzeyi. |
| Worktree | Aynı Git deposunun ayrı bir klasördeki ikinci çalışma kopyası. Paralel yazarları ayırır. |
| Rutin | Zamanlanmış ya da tetiklenmiş, gözetimsiz koşan Claude görevi. Bulutta ya da masaüstünde çalışır. |
| Gözetimsiz koşum | Kullanıcı başında yokken ilerleyen iş. Soru soramaz, izin bekleyemez. |
| Advisor | Zor kararda ikinci, daha güçlü bir modelin görüşünü alma özelliği. |
| Harness | Modelin çevresindeki çalışma düzeni: araçlar, izinler, bağlam yönetimi. Claude Code bir harness'tır. |

---

[Kontrol listesi](../README.md) · [Rehber](../rehber/README.md) · [Komutlar ve kısayollar](komutlar.md) · [Sorun giderme](sorun-giderme.md) · [Dosya konumları](dosyalar.md) · [İpuçları ve püf noktaları](ipuclari.md) · [Gerçek deneyimlerden on ders](deneyimler.md)

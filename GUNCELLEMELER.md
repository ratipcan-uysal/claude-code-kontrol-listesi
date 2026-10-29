# 30 Ekim 2026: Projects

Dayanak resmî belge: [Projects](https://code.claude.com/docs/en/claude-projects) ve [bulut ortamları](https://code.claude.com/docs/en/cloud-environments). Konu seçimi bir topluluk yazısından geldi, iddialar belgeyle karşılaştırıldı. Yazıdaki günlük thread sınırı (200) belgeyle çelişiyordu, belgede 500. Belgede olmayan sayılar eklenmedi.

- Kontrol listesine 20. bölüm, yedi madde: proje talimatı, repo ayarlarının thread'e gelmemesi, ağ erişimi, ağ sırrı, kurulum betiği, model ve effort ile Usage, Waiting on you.
- Rehbere 14. bölüm: Projects, koordinatör ve thread'ler.
- Sorun gidermeye üç satır: GitHub App, thread onayı, proje konuşmasında connector olmaması.

# 30 Ekim 2026: Opus 5.5 rehberinden eklemeler

Kaynak: Anthropic'in "Getting the most out of Opus 5.5" yazısı (22 Eylül 2026). Ürün davranışı resmî belgeyle karşılaştırıldı.

- Beş yeni madde, 113'ten 118'e: 3.8 ne zaman devam edip ne zaman durup soracağını yazmak, 5.7 model değişimini fark edip geri dönmek, 12.8 rapor biçimini sabitlemek, 13.7 uzun işin görev listesini dosyada tutmak, 16.5 tasarımda istenmeyen kalıpları adıyla yazmak.
- Rehber: bölüm 3'e çalışan işe mesaj eklemek, bölüm 12'ye Opus 5.5 ile "think carefully" satırlarını budama örneği.
- İpuçları: cevapta iç akıl yürütmeyi istememek, görseli yeniden yazmamak, uzun belgeyi tutarsızlık için taratmak.
- Rehberde "bölüm {{bolum:n}}" kalıbı çift "Bölüm" üretiyordu. Dört yer düzeltildi, derleyici artık bu kalıbı reddediyor.

# 29 Ekim 2026: Claude Code rehberi

Kontrol listesine üç seviyeli, alıştırmalı bir rehber eklendi: 13 bölüm, yaklaşık 15 bin kelime.

- Temel: zihinsel model, iş vermek, oturumu yönetmek, kanıtla teslim. Orta: talimat mimarisi, izin ve güvenlik, skill/alt ajan/MCP, hook. Uzman: paralel işler, gözetimsiz iş, ekip ölçeği, sistemi iyileştirmek, bitirme projesi.
- Her bölüm: zihinsel model, karar kuralları, gerçek vaka ve etiketli kurgu senaryo, alıştırma ve "bitti" kanıtı, madde ve ek bağlantıları.
- Ürün iddiaları resmî belgeyle karşılaştırıldı. Belgede olmayan yöntemler iş akışı önerisi diye işaretlendi.
- Rehber web, Markdown ve PDF olarak üretiliyor. PDF 92 sayfa.
- README'de kod içindeki `<ad>` gibi ifadelerin silinmesi düzeltildi.

# 29 Ekim 2026: altı madde ve altı başvuru eki

19 bölüm korundu, 107 madde 113'e çıktı. Mevcut kimlikler ve `cc-kontrol-v2` kaydı değişmedi, yeni maddeler bölüm sonlarına eklendi.

- 1.8 ayarın hangi katmandan geldiği, 2.7 devam, dallandırma ve temiz başlangıç, 5.6 modeli aynı görevle karşılaştırma, 8.6 engelleyen hook'u async yapmama, 8.7 hook sırası varsaymama, 14.7 makineye aktarılacak sonucu şemayla tanımlama.
- Altı ek: komutlar ve kısayollar, sorun giderme, dosya konumları, ipuçları ve püf noktaları, gerçek deneyimlerden on ders, terimler sözlüğü. Her ek ilgili maddelere bağlanıyor. Ekler web sayfası, Markdown ve PDF olarak üretiliyor.
- İpuçları eki 48 maddeye çıktı: ayarlar, talimatlar, oturum, bağlam ve çıktı, hata ayıklama, genişletme, ekip ve güvenlik.
- Dar ekranda ek tabloları kart olarak diziliyor.
- Yapısal testler 11'e, tarayıcı kontrolleri 44'e çıktı.

# 21 Ekim 2026 kalite güncellemesi

19 bölüm korundu. 97 madde 107’ye çıktı; mevcut 51 maddenin anlatımı veya örneği düzeltildi, 10 yeni kontrol eklendi. Eski bölüm/madde kimlikleri ve `cc-kontrol-v2` yerel kayıt anahtarı korunur.

- Talimatlar, otomatik bellek ve AGENTS.md yükleme koşulları ayrıldı; 100 satır şartı kaldırıldı.
- Alt ajan model seçimi ve önceliği, sağlayıcı farkı, abonelik/API maliyeti ve effort kapsamı netleştirildi. `ultrathink` açıklaması resmî belgede doğrulandığı için korundu.
- Read deny ve sandbox sınırları, hook hata politikası, Bash erişiminin salt okunur olmaması ve yeni repo güveni düzeltildi.
- Test logunun gerçek çıkış kodunu koruyan örnek eklendi. Git index’inin iki komutla atomik olmadığı açıklandı.
- Gözetimsiz görev yetkisi, bulut/Desktop/oturum içi zamanlama, tur sınırı ve headless hata durumları ayrıldı.
- Türkçe giriş testinden kaçınma önerisi kaldırıldı. Simülatör ve derleme temizliği kesin sahiplik ve kanıt korumaya bağlandı.
- Doğrulanamayan kişisel istatistikler ve ölçülmüş getiri izlenimi kaldırıldı. Her teknik maddeye kaynak; genel önerilere açık editoryal etiket eklendi.
- İşaret temizleme düğmesinin bütün maddeleri gizlemesi düzeltildi. Arama, JSON yedekleme/geri yükleme, tema seçimi, gizli hedefe bağlantı ve mobil metin yerleşimi eklendi veya düzeltildi.
- HTML, README ve PDF aynı içerik kaynağından yeniden üretildi.

## Yeni maddeler

- 1.7
- 6.7
- 7.7
- 9.7
- 9.8
- 12.7
- 13.6
- 14.5
- 14.6
- 19.6

## Düzenlenen mevcut maddeler

1.1, 1.2, 1.5, 1.6, 2.1, 2.5, 3.1, 3.3, 3.7, 4.3, 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.3, 7.4, 7.5, 7.6, 8.2, 8.3, 8.4, 8.5, 9.1, 9.2, 9.4, 10.1, 11.2, 11.4, 12.2, 12.6, 13.1, 13.2, 14.1, 14.2, 14.4, 15.1, 15.2, 15.3, 17.1, 17.3, 17.5, 18.4, 19.2, 19.3

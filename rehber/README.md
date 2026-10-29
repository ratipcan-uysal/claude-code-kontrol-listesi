# Claude Code rehberi

_Belge kontrolü: 29 Ekim 2026_

Kontrol listesi neyin yapılacağını söyler. Ekler komutları, dosya yollarını ve ayarları sıralar. Bu rehber ise ikisinin arasındaki boşluğu doldurur: Claude Code'un neden öyle davrandığını, hangi durumda hangi aracın seçileceğini ve bunun nasıl öğrenileceğini anlatır.

Uzmanı acemiden ayıran şey daha çok komut bilmesi değildir. Uzman, bir sonucu gördüğünde onun hangi katmandan geldiğini bilir: modelin kararından mı, bir talimattan mı, bir izin kuralından mı, bir hook'tan mı. Bu yüzden her bölüm bir zihinsel modelle başlar ve bir alıştırmayla biter.

## Nasıl çalışılır

Rehber üç seviyeden oluşur. **Temel** seviye tek bir oturumu iyi yönetmeyi öğretir. **Orta** seviye talimatları, izinleri ve yeniden kullanılabilir parçaları kurmayı öğretir. **Uzman** seviye paralel, gözetimsiz ve ekip ölçeğinde çalışmayı öğretir. Sırayla okumak en iyisi, çünkü her seviye bir öncekinin kavramlarını kullanır.

Her bölüm aynı yapıdadır:

- **Zihinsel model:** Bölümün konusunu açıklayan tek fikir.
- **Karar kuralları:** Hangi durumda ne yapılacağı.
- **Hata biçimleri:** Bu konuda işler en sık nasıl ters gider. Gerçek vakalar tarihli bir ölçüm defterinden alındı ve öyle işaretlendi. Kurgu senaryolar da açıkça "kurgu" diye yazıldı.
- **Alıştırma:** Kendi elinle yapacağın iş ve bittiğini gösteren kanıt.
- **Bağlantılar:** İlgili kontrol listesi maddeleri ve ekler.

Alıştırmalar herhangi bir git deposunda yapılabilir. Silme, yeniden yazma ya da yayın içeren alıştırmaları gerçek iş deposunda değil, bu iş için açtığın bir deneme deposunda yap.

Ürün davranışı resmî belgeyle karşılaştırıldı. Belgede olmayan bir yöntem önerildiğinde bu açıkça yazıldı. Komut ve ayar ayrıntısı hızla değiştiği için rehberde değil eklerde tutuluyor. Yerel CLI 2.1.284 ile karşılaştırıldı, sen kendi sürümünü `claude --version` ile gör.

## Temel

- [1. Zihinsel model: döngü, bağlam ve harness](01-zihinsel-model.md): Claude Code'la yaşanan her sürprizin açıklaması üç parçadan birindedir: model, araç ya da harness. Bağlam penceresi modelin gördüğü tek şeydir.

## Orta

- [5. Talimat mimarisi: rica ile garanti](05-talimat-mimarisi.md): Bir kural ya Claude'a söylenir ya da Claude Code'a uygulatılır. Hangisinin nereye gideceğini bilmek, kuralın tutup tutmayacağını belirler.

---

[Kontrol listesi](../README.md)

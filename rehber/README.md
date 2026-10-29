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
- [2. İş vermek: bitiş çizgisini çizmek](02-is-vermek.md): İyi bir istek hedefin yanında bitiş ölçütünü, kısıtı, örneği ve okuru da söyler. Ölçütü Claude'un kendi koşturabileceği bir kanıta çevirirsen tek doğrulayıcı sen kalmazsın.
- [3. Oturum: masayı doğru yönetmek](03-oturumu-yonetmek.md): Her oturum komutu bağlam penceresinin içeriğini değiştirir. Konu başına oturum, devir dosyası, sıkıştırma, dallandırma ve geri sarma arasında hangisinin ne zaman kullanılacağı ve sınırları.
- [4. Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md): "Geçti" bir iddiadır. Sayı, kasten kırılan kontrol, önce ve sonra görüntü ve diff ile eşleşen rapor ise kanıttır. Teslim yerel, push ve yayın olarak üç ayrı aşamadır.

## Orta

- [5. Talimat mimarisi: rica ile garanti](05-talimat-mimarisi.md): Bir kural ya Claude'a söylenir ya da Claude Code'a uygulatılır. Hangisinin nereye gideceğini bilmek, kuralın tutup tutmayacağını belirler.
- [6. İzin ve güvenlik: mod, kural, sandbox](06-izin-ve-guvenlik.md): İzin modu, izin kuralı ve sandbox üç ayrı soruya cevap verir. Hangisinin neyi koruduğu, kuralın dar ve eşleşebilir yazılması ve gözetimsiz koşumda etkin modun doğrulanması.
- [7. Yeniden kullanım: skill, alt ajan, MCP, plugin](07-skill-ajan-mcp.md): Skill, alt ajan, MCP ve plugin'in her biri farklı bir sorunu çözer. Hangisinin ne zaman seçileceği, skill açıklamasının neden tetik olduğu ve MCP'nin gerçek bir okumayla sınanması.
- [8. Hook ile garanti: olay, çıkış kodu, sınama](08-hook-ile-garanti.md): Hook, modelin kararına girmeden olay gelince çalışan koddur. Çıkış koduna göre neyi engelleyip neyi engellemediği, hook tiplerinin farkı ve hook'u bozarak sınamak.

## Uzman

- [9. Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md): Paralel çalışma yalnız sonuçları ve kaynakları gerçekten bağımsız işlerde kazandırır. Worktree dosya ve index çakışmasını çözer, port, tarayıcı, pano, simülatör ve makine yükü ortak kalır.
- [10. Gözetimsiz iş: sen yokken çalışan sistem](10-gozetimsiz-is.md): Gözetimsiz iş, hangi kararın verilebileceğini, neyin işi durduracağını ve bittiğin kanıtını önceden yazmaktır. En pahalı hata işin yapılmaması değil, yapılmadığının fark edilmemesidir.
- [11. Ekip ölçeği: ortak ayar, dağıtım ve güven](11-ekip-olcegi.md): Ekip dosyası bir öneri, yönetilen ayar bir kuraldır. Ayarı, skill'i ve plugin'i kimin yazdığını, kimin incelediğini ve kimin çalıştırdığını bilmek ekip ölçeğinin temel sorusudur.
- [12. Sistemi iyileştirmek: hatayı katmana yazmak](12-sistemi-iyilestirmek.md): Her başarısızlığın adresi bağlam, model kararı ya da harness'tir ve ders doğru katmana yazılır. Üçüncü tekrar kural olur, bakım ritmi ve önce ve sonra karşılaştırması sistemi sağlıklı tutar.
- [13. Bitirme projesi: her adımda kanıt](13-bitirme-projesi.md): Kendi seçtiğin küçük ve gerçek bir işi plan, uygulama, doğrulama ve teslim aşamalarından geçirirsin. Her aşamada önceki bölümlerin becerisini kullanır ve bir kanıt dosyası bırakırsın.
- [14. Projects: koordinatör ve thread'ler](14-projects.md): Proje, işi thread'lere bölen tek bir konuşmadır. Her thread repoyu temiz klonlayan bir bulut oturumudur ve makinendeki hook, izin ve skill'leri değil, proje talimatını, belleğini, connector'larını ve ortamını alır.

---

[Kontrol listesi](../README.md)

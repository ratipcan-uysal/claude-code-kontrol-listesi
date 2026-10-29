# Rehberin dizini. Bölüm metni kaynak/bolumler/<ad>.md içinde, Markdown alt kümesiyle (yap.py EKLER bölümü).
# [[3.1]] maddeye, {{ek:komutlar}} eke, {{bolum:5}} başka bölüme bağlanır. "ad" dosya adıdır, değiştirme.
REHBER_TARIH = "29 Ekim 2026"

SEVIYELER = {"temel": "Temel", "orta": "Orta", "uzman": "Uzman"}

REHBER_GIRIS = r"""
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
"""

import os
_DIZIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bolumler")

REHBER = [
 dict(no=1, ad="01-zihinsel-model", seviye="temel", baslik="Zihinsel model: döngü, bağlam ve harness",
      ozet="Claude Code'la yaşanan her sürprizin açıklaması üç parçadan birindedir: model, araç ya da harness. Bağlam penceresi modelin gördüğü tek şeydir."),
 dict(no=5, ad="05-talimat-mimarisi", seviye="orta", baslik="Talimat mimarisi: rica ile garanti",
      ozet="Bir kural ya Claude'a söylenir ya da Claude Code'a uygulatılır. Hangisinin nereye gideceğini bilmek, kuralın tutup tutmayacağını belirler."),
 dict(no=6, ad="06-izin-ve-guvenlik", seviye="orta", baslik="İzin ve güvenlik: mod, kural, sandbox",
      ozet="İzin modu, izin kuralı ve sandbox üç ayrı soruya cevap verir. Hangisinin neyi koruduğu, kuralın dar ve eşleşebilir yazılması ve gözetimsiz koşumda etkin modun doğrulanması."),
 dict(no=7, ad="07-skill-ajan-mcp", seviye="orta", baslik="Yeniden kullanım: skill, alt ajan, MCP, plugin",
      ozet="Skill, alt ajan, MCP ve plugin'in her biri farklı bir sorunu çözer. Hangisinin ne zaman seçileceği, skill açıklamasının neden tetik olduğu ve MCP'nin gerçek bir okumayla sınanması."),
 dict(no=8, ad="08-hook-ile-garanti", seviye="orta", baslik="Hook ile garanti: olay, çıkış kodu, sınama",
      ozet="Hook, modelin kararına girmeden olay gelince çalışan koddur. Çıkış koduna göre neyi engelleyip neyi engellemediği, hook tiplerinin farkı ve hook'u bozarak sınamak."),
 dict(no=9, ad="09-paralel-isler", seviye="uzman", baslik="Paralel işler: bağımsızlığı ölçmek",
      ozet="Paralel çalışma yalnız sonuçları ve kaynakları gerçekten bağımsız işlerde kazandırır. Worktree dosya ve index çakışmasını çözer, port, tarayıcı, pano, simülatör ve makine yükü ortak kalır."),
 dict(no=10, ad="10-gozetimsiz-is", seviye="uzman", baslik="Gözetimsiz iş: sen yokken çalışan sistem",
      ozet="Gözetimsiz iş, hangi kararın verilebileceğini, neyin işi durduracağını ve bittiğin kanıtını önceden yazmaktır. En pahalı hata işin yapılmaması değil, yapılmadığının fark edilmemesidir."),
 dict(no=2, ad="02-is-vermek", seviye="temel", baslik="İş vermek: bitiş çizgisini çizmek",
      ozet="İyi bir istek hedefin yanında bitiş ölçütünü, kısıtı, örneği ve okuru da söyler. Ölçütü Claude'un kendi koşturabileceği bir kanıta çevirirsen tek doğrulayıcı sen kalmazsın."),
 dict(no=3, ad="03-oturumu-yonetmek", seviye="temel", baslik="Oturum: masayı doğru yönetmek",
      ozet="Her oturum komutu bağlam penceresinin içeriğini değiştirir. Konu başına oturum, devir dosyası, sıkıştırma, dallandırma ve geri sarma arasında hangisinin ne zaman kullanılacağı ve sınırları."),
 dict(no=4, ad="04-kanitla-teslim", seviye="temel", baslik="Kanıtla teslim: iddiayı sayıya çevir",
      ozet="\"Geçti\" bir iddiadır. Sayı, kasten kırılan kontrol, önce ve sonra görüntü ve diff ile eşleşen rapor ise kanıttır. Teslim yerel, push ve yayın olarak üç ayrı aşamadır."),
 dict(no=11, ad="11-ekip-olcegi", seviye="uzman", baslik="Ekip ölçeği: ortak ayar, dağıtım ve güven",
      ozet="Ekip dosyası bir öneri, yönetilen ayar bir kuraldır. Ayarı, skill'i ve plugin'i kimin yazdığını, kimin incelediğini ve kimin çalıştırdığını bilmek ekip ölçeğinin temel sorusudur."),
 dict(no=12, ad="12-sistemi-iyilestirmek", seviye="uzman", baslik="Sistemi iyileştirmek: hatayı katmana yazmak",
      ozet="Her başarısızlığın adresi bağlam, model kararı ya da harness'tir ve ders doğru katmana yazılır. Üçüncü tekrar kural olur, bakım ritmi ve önce ve sonra karşılaştırması sistemi sağlıklı tutar."),
 dict(no=13, ad="13-bitirme-projesi", seviye="uzman", baslik="Bitirme projesi: her adımda kanıt",
      ozet="Kendi seçtiğin küçük ve gerçek bir işi plan, uygulama, doğrulama ve teslim aşamalarından geçirirsin. Her aşamada önceki bölümlerin becerisini kullanır ve bir kanıt dosyası bırakırsın."),
 dict(no=14, ad="14-projects", seviye="uzman", baslik="Projects: koordinatör ve thread'ler",
      ozet="Proje, işi thread'lere bölen tek bir konuşmadır. Her thread repoyu temiz klonlayan bir bulut oturumudur ve makinendeki hook, izin ve skill'leri değil, proje talimatını, belleğini, connector'larını ve ortamını alır."),
]
REHBER.sort(key=lambda b: b["no"])

for _b in REHBER:
    _b["md"] = open(os.path.join(_DIZIN, _b["ad"] + ".md"), encoding="utf-8").read()

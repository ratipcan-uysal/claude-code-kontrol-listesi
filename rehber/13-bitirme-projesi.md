# 13. Bitirme projesi: her adımda kanıt

_Uzman · Belge kontrolü: 29 Ekim 2026_

Kendi seçtiğin küçük ve gerçek bir işi plan, uygulama, doğrulama ve teslim aşamalarından geçirirsin. Her aşamada önceki bölümlerin becerisini kullanır ve bir kanıt dosyası bırakırsın.

## Zihinsel model: uzmanlık, her adımda kanıt bırakmaktır

Önceki on iki bölümde ayrı ayrı beceriler öğrendin: bağlamı yönetmek, işi bitiş çizgisiyle vermek, kuralı doğru katmana koymak, paralel ve gözetimsiz çalışmak, sistemi iyileştirmek. Bu bölümde hepsini tek bir işte birleştireceksin. Ölçüt öncekilerden farklı: yeni bir şey öğrenmeyeceksin, öğrendiğini **her adımda kanıtla** göstereceksin.

Bu ölçüt rastgele seçilmedi. [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md) bölümünün ana fikri şuydu: "tamamlandı" bir iddiadır, kanıt değil. Uzmanla acemi arasındaki fark, uzmanın bir sonucu gördüğünde hangi katmandan geldiğini bilmesi ve bir şeyin bittiğini sayıyla, çıktıyla ya da dosyayla göstermesidir. Bitirme projesinde bunu zorunlu kılıyoruz: her aşamanın sonunda masaya konabilecek bir kanıt olacak. Kanıtı olmayan aşama bitmiş sayılmaz.

Bu bölümün yapısı diğerlerinden farklı. Alıştırma yerine bir proje, hata biçimleri yerine bir değerlendirme listesi var. Çünkü burada hata yapmak, öğrenmenin parçası: takıldığın yer, hangi bölümü yeniden okuman gerektiğini gösterir.

## Proje

Kendi seçtiğin küçük ama gerçek bir iş yap. "Gerçek" demek, sonucu bir gün gerçekten kullanacağın demek. Oyuncak örnek değil. Birkaç fikir:

- Bir klasördeki dosyaları kurala göre ayıran ve ne yaptığını raporlayan bir betik.
- Bir CSV ya da log dosyasından haftalık özet üreten bir rapor üretici.
- Tek sayfalık, birkaç bölümden oluşan küçük bir web sayfası.

Üç sınırı baştan koy:

1. **Herhangi bir git deposunda yapılabilsin.** Yeni, boş bir depo da olur. Gerçek bir iş deposuna dokunma, bu iş için açtığın bir depoda çalış.
2. **Bir iş günü sürmesin.** Büyük işi küçültüp bitmiş bir şey çıkarmak, büyük işi yarım bırakmaktan değerlidir. Sığmayan kısmı "sonra" listesine yaz.
3. **Dışarıdan veri ve hesap gerektirmesin.** Ücretli servis, gerçek müşteri verisi ya da kurum hesabı olmasın. Gerekirse sahte veri üret.

Seçimini tek cümleyle yaz: "Şunu yapacağım, şu girdiyi alıp şu çıktıyı verecek, şu komutla çalıştırılacak."

## Aşamalar

Dört aşama var. Her birinde hangi bölümün becerisini kullandığın yazılı. Aşamayı bitirmeden sonrakine geçme.

### 1. Plan

Claude'a kod yazdırmadan önce işi tanımla. Girdi, çıktı, "bitti" ölçütü ve dokunulmayacak yerler yazılı olsun. İş küçükse plan modunda bir plan iste ve oku. Beğenmediğin yeri değiştirmeden uygulamaya geçme. Becerin burada [Bölüm 2: İş vermek: bitiş çizgisini çizmek](02-is-vermek.md) (bitiş çizgisini çizmek) ve [Bölüm 1: Zihinsel model: döngü, bağlam ve harness](01-zihinsel-model.md) (hangi parçanın neyi yapacağı). Projeye bir `CLAUDE.md` aç ve yalnız bu iş için gerçekten gerekli üç dört satır yaz: nasıl çalıştırılır, nasıl test edilir, neye dokunulmaz. Hangi satırın kural, hangisinin tercih olduğunu [Bölüm 5: Talimat mimarisi: rica ile garanti](05-talimat-mimarisi.md) içindeki ölçütle ayır. İstisnası olmayan bir şey varsa (örneğin "örnek veri dosyasını silme") bunu CLAUDE.md'de değil izin kuralında tut, [Bölüm 6: İzin ve güvenlik: mod, kural, sandbox](06-izin-ve-guvenlik.md) bu konuda yardım eder.

### 2. Uygulama

İşi küçük adımlarla ilerlet ve her adımdan sonra çalıştır. Oturum uzarsa bağlamı yönet: yeni bir iş için temiz oturum aç, gerekirse özet bırakarak devam et. Bu [Bölüm 3: Oturum: masayı doğru yönetmek](03-oturumu-yonetmek.md) bölümünün becerisidir. Tekrar eden bir adımı fark edersen (aynı komutu üçüncü kez yazıyorsan) onu bir skill ya da betiğe çevir, hook gerektiren bir şey varsa [Bölüm 8: Hook ile garanti: olay, çıkış kodu, sınama](08-hook-ile-garanti.md) bölümüne dön. Projede birbirinden bağımsız iki parça varsa (örneğin betiğin kendisi ve belgesi) bunları ayrı worktree'lerde paralel yaptırabilirsin. Ama önce bağımsız olduklarını kanıtla, [Bölüm 9: Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md) bölümündeki uyarıyı hatırla: paralel olmak bağımsız olmak demek değildir.

### 3. Doğrulama

Burada kendi yazdığın kontrolü sına. Claude "çalışıyor" derse sen çalıştır ve çıktıyı gör. En az iki sınama yap:

- **Beklenen yolda:** gerçek bir girdiyle çalıştır, çıktıyı beklenenle karşılaştır.
- **Bozulan yolda:** bir hatayı kasıtlı olarak geri koy (yanlış bir kural, bozuk bir girdi satırı) ve kontrolün bunu yakaladığını gör. Hatayı geri koyduğunda kontrol düşmüyorsa o kontrol hiçbir şeye bakmıyordur. [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md) bunun vakalarını anlatıyor.

Test varsa koşulan test sayısını oku: sıfır test koşmak geçmek değildir. Test yoksa yazdır, sonra yine hatayı geri koyarak sına. Doğrulamayı yapan oturum, kodu yazan oturum olmasın. Yeni bir oturumda "bu çıktıyı kırmaya çalış" diye iste.

### 4. Teslim

Teslim, işi bırakmaktır ama bırakırken bir sonraki kişiye (ya da bir ay sonraki kendine) ne olduğunu anlatman gerekir. Üç şey bırak:

- Çalıştırma komutu ve örnek çıktı.
- Neyin yapılmadığı ve neden. Yarım bıraktığın her madde proje kökündeki bir bekleyenler dosyasına girsin.
- Sürüm ve ortam notu: `claude --version`, işletim sistemi, kullandığın model.

İşi commit'le. Her commit'in mesajı o değişikliğin neden yapıldığını söylesin. Push yapma, deneme deposunda gerek yok. Eğer işi gözetimsiz bir koşuma da bağlamak istersen [Bölüm 10: Gözetimsiz iş: sen yokken çalışan sistem](10-gozetimsiz-is.md) bölümündeki kuralları uygula: ara çıktı diske yazılsın, uzun iş arka plana atılıp tur kapatılmasın. Ekibinle paylaşacaksan [Bölüm 11: Ekip ölçeği: ortak ayar, dağıtım ve güven](11-ekip-olcegi.md) bölümündeki ayrımı kullan: ortak olan commit'lenir, kişisel olan yerelde kalır. Son olarak [Bölüm 12: Sistemi iyileştirmek: hatayı katmana yazmak](12-sistemi-iyilestirmek.md) bölümündeki soruyu sor: bu projede öğrendiğim ders hangi katmana yazılmalı? Dersi yaz ve nereye yazdığını söyle.

## Kanıt listesi

Aşağıdaki tabloyu projenin köküne `KANIT.md` olarak kaydet ve doldur. Her satır için somut bir dosya, çıktı ya da komut göster. "Yaptım" yazmak kanıt sayılmaz.

| Aşama | Beklenen kanıt |
|---|---|
| Plan | Tek cümlelik proje tanımı, yazılı "bitti" ölçütü, dokunulmayacaklar listesi |
| Plan | Dört satırı geçmeyen `CLAUDE.md` ve her satırın neden kural ya da tercih olduğu |
| Uygulama | Küçük adımlara bölünmüş commit geçmişi (`git log --oneline`) |
| Uygulama | Bağlamın dolduğu ya da yeni oturuma geçtiğin bir noktada bıraktığın özet |
| Doğrulama | Beklenen yolda gerçek girdi ve çıktı |
| Doğrulama | Kasıtlı geri konan hata ve kontrolün onu yakaladığını gösteren çıktı |
| Doğrulama | Koşulan test sayısı (sıfırdan büyük) ya da testin yokluğunu açıklayan not |
| Teslim | Çalıştırma komutu, örnek çıktı, sürüm ve ortam notu |
| Teslim | Bekleyenler dosyası: yapılmayanlar ve nedenleri |
| Teslim | Öğrendiğin dersin yazıldığı dosya ve katmanın gerekçesi |

## Değerlendirme

Sayısal puan yok. Projeyi bitirdikten sonra aşağıdaki soruları kendine, dürüstçe sor. "Hayır" ya da "emin değilim" cevabı, geri dönüp yeniden okuman gereken bölümü gösterir.

- Projeyi başlamadan önce tek cümleyle ve ölçülebilir bir "bitti" ölçütüyle tanımladın mı? ([Bölüm 2: İş vermek: bitiş çizgisini çizmek](02-is-vermek.md))
- Bir sonuç beklenmedik çıktığında önce hangi katmandan geldiğini (model, araç, harness) sordun mu? ([Bölüm 1: Zihinsel model: döngü, bağlam ve harness](01-zihinsel-model.md))
- Oturum şiştiğinde yeni oturuma geçtin mi, ve geçerken neyi taşıdığını biliyor musun? ([Bölüm 3: Oturum: masayı doğru yönetmek](03-oturumu-yonetmek.md))
- Her "tamamlandı" cümlesinin arkasında senin gördüğün bir çıktı var mı? ([Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md))
- Kuralların hangileri Claude'un kararında, hangileri Claude Code'un uyguladığı katmanda? Bunu açıklayabilir misin? ([Bölüm 5: Talimat mimarisi: rica ile garanti](05-talimat-mimarisi.md))
- Kontrolünü hatayı geri koyup düşürerek sınadın mı, yoksa yalnız geçtiğini mi gördün? ([Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md))
- Yarım bıraktığın bir şey bir dosyada yazılı mı, yoksa yalnız aklında mı? ([Bölüm 12: Sistemi iyileştirmek: hatayı katmana yazmak](12-sistemi-iyilestirmek.md))
- Paylaşılan bir kaynağı (dal, index, port, dosya) iki yerden kullandıysan çakışmayı nasıl önledin? ([Bölüm 9: Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md))
- Öğrendiğin dersi doğru katmana yazdın mı ve neden orası? ([Bölüm 12: Sistemi iyileştirmek: hatayı katmana yazmak](12-sistemi-iyilestirmek.md))
- Bu projeyi bir ekip arkadaşına devretsen, `KANIT.md` ve depo yeterli olur muydu? ([Bölüm 3: Oturum: masayı doğru yönetmek](03-oturumu-yonetmek.md))
- Bir şey sana en pahalıya geldiyse, o hata bir şeyin kırılmasından mı, yoksa hiçbir şeye bakmadan başarılı görünmesinden mi çıktı? ([Gerçek deneyimlerden on ders](../ekler/deneyimler.md) sayfasındaki vakalar bu soruya dönüyor.)

Kendini dürüstçe sorguladığında üç şeyi de yaz: neyi kaçırmış olabilirsin, hangi iddian en zayıf, hangi kararının gerekçesi yok. Rehberi bitirmiş olmanın işareti, bu üç cümleyi rahatça yazabilmek.

## Bağlantılar

Önceki bölümler: [Bölüm 1: Zihinsel model: döngü, bağlam ve harness](01-zihinsel-model.md) [Bölüm 2: İş vermek: bitiş çizgisini çizmek](02-is-vermek.md) [Bölüm 3: Oturum: masayı doğru yönetmek](03-oturumu-yonetmek.md) [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md) [Bölüm 5: Talimat mimarisi: rica ile garanti](05-talimat-mimarisi.md) [Bölüm 6: İzin ve güvenlik: mod, kural, sandbox](06-izin-ve-guvenlik.md) [Bölüm 7: Yeniden kullanım: skill, alt ajan, MCP, plugin](07-skill-ajan-mcp.md) [Bölüm 8: Hook ile garanti: olay, çıkış kodu, sınama](08-hook-ile-garanti.md) [Bölüm 9: Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md) [Bölüm 10: Gözetimsiz iş: sen yokken çalışan sistem](10-gozetimsiz-is.md) [Bölüm 11: Ekip ölçeği: ortak ayar, dağıtım ve güven](11-ekip-olcegi.md) [Bölüm 12: Sistemi iyileştirmek: hatayı katmana yazmak](12-sistemi-iyilestirmek.md). Kontrol listesi: [12.1](../README.md#12-dogrulama) [12.2](../README.md#12-dogrulama) [18.1](../README.md#18-bilgi) [18.2](../README.md#18-bilgi) [19.6](../README.md#19-bakim). Ekler: [Gerçek deneyimlerden on ders](../ekler/deneyimler.md), [Sorun giderme](../ekler/sorun-giderme.md), [Terimler sözlüğü](../ekler/sozluk.md).

---

[← Bölüm 12](12-sistemi-iyilestirmek.md) · [İçindekiler](README.md) · [Bölüm 14 →](14-projects.md)

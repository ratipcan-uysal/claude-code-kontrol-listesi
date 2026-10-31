## Zihinsel model: uzmanlık, her adımda kanıt bırakmaktır

Önceki on iki bölümde ayrı ayrı beceriler öğrendin: bağlamı yönetmek, işi bitiş çizgisiyle vermek, kuralı doğru katmana koymak, paralel ve gözetimsiz çalışmak, sistemi iyileştirmek. Bu bölümde hepsini tek bir işte birleştireceksin. Ölçüt öncekilerden farklı: yeni bir şey öğrenmeyeceksin, öğrendiğini **her adımda kanıtla** göstereceksin.

Bu ölçüt rastgele seçilmedi. {{bolum:4}} bölümünün ana fikri şuydu: "tamamlandı" bir iddiadır, kanıt değil. Uzmanla acemi arasındaki fark, uzmanın bir sonucu gördüğünde hangi katmandan geldiğini bilmesi ve bir şeyin bittiğini sayıyla, çıktıyla ya da dosyayla göstermesidir. Bitirme projesinde bunu zorunlu kılıyoruz: her aşamanın sonunda masaya konabilecek bir kanıt olacak. Kanıtı olmayan aşama bitmiş sayılmaz.

{{sekil:b13-bitirme-asamalari|Dört aşama sırayla ilerler ve her biri KANIT.md dosyasına bir iz bırakır. Aşamanın kanıtı yoksa bir sonrakine geçilmez.}}

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

Claude'a kod yazdırmadan önce işi tanımla. Girdi, çıktı, "bitti" ölçütü ve dokunulmayacak yerler yazılı olsun. İş küçükse plan modunda bir plan iste ve oku. Beğenmediğin yeri değiştirmeden uygulamaya geçme. Becerin burada {{bolum:2}} (bitiş çizgisini çizmek) ve {{bolum:1}} (hangi parçanın neyi yapacağı). Projeye bir `CLAUDE.md` aç ve yalnız bu iş için gerçekten gerekli üç dört satır yaz: nasıl çalıştırılır, nasıl test edilir, neye dokunulmaz. Hangi satırın kural, hangisinin tercih olduğunu {{bolum:5}} içindeki ölçütle ayır. İstisnası olmayan bir şey varsa (örneğin "örnek veri dosyasını silme") bunu CLAUDE.md'de değil izin kuralında tut, {{bolum:6}} bu konuda yardım eder.

### 2. Uygulama

İşi küçük adımlarla ilerlet ve her adımdan sonra çalıştır. Oturum uzarsa bağlamı yönet: yeni bir iş için temiz oturum aç, gerekirse özet bırakarak devam et. Bu {{bolum:3}} bölümünün becerisidir. Tekrar eden bir adımı fark edersen (aynı komutu üçüncü kez yazıyorsan) onu bir skill ya da betiğe çevir, hook gerektiren bir şey varsa {{bolum:8}} bölümüne dön. Projede birbirinden bağımsız iki parça varsa (örneğin betiğin kendisi ve belgesi) bunları ayrı worktree'lerde paralel yaptırabilirsin. Ama önce bağımsız olduklarını kanıtla, {{bolum:9}} bölümündeki uyarıyı hatırla: paralel olmak bağımsız olmak demek değildir.

### 3. Doğrulama

Burada kendi yazdığın kontrolü sına. Claude "çalışıyor" derse sen çalıştır ve çıktıyı gör. En az iki sınama yap:

- **Beklenen yolda:** gerçek bir girdiyle çalıştır, çıktıyı beklenenle karşılaştır.
- **Bozulan yolda:** bir hatayı kasıtlı olarak geri koy (yanlış bir kural, bozuk bir girdi satırı) ve kontrolün bunu yakaladığını gör. Hatayı geri koyduğunda kontrol düşmüyorsa o kontrol hiçbir şeye bakmıyordur. {{bolum:4}} bunun vakalarını anlatıyor.

Test varsa koşulan test sayısını oku: sıfır test koşmak geçmek değildir. Test yoksa yazdır, sonra yine hatayı geri koyarak sına. Doğrulamayı yapan oturum, kodu yazan oturum olmasın. Yeni bir oturumda "bu çıktıyı kırmaya çalış" diye iste.

### 4. Teslim

Teslim, işi bırakmaktır ama bırakırken bir sonraki kişiye (ya da bir ay sonraki kendine) ne olduğunu anlatman gerekir. Üç şey bırak:

- Çalıştırma komutu ve örnek çıktı.
- Neyin yapılmadığı ve neden. Yarım bıraktığın her madde proje kökündeki bir bekleyenler dosyasına girsin.
- Sürüm ve ortam notu: `claude --version`, işletim sistemi, kullandığın model.

İşi commit'le. Her commit'in mesajı o değişikliğin neden yapıldığını söylesin. Push yapma, deneme deposunda gerek yok. Eğer işi gözetimsiz bir koşuma da bağlamak istersen {{bolum:10}} bölümündeki kuralları uygula: ara çıktı diske yazılsın, uzun iş arka plana atılıp tur kapatılmasın. Ekibinle paylaşacaksan {{bolum:11}} bölümündeki ayrımı kullan: ortak olan commit'lenir, kişisel olan yerelde kalır. Son olarak {{bolum:12}} bölümündeki soruyu sor: bu projede öğrendiğim ders hangi katmana yazılmalı? Dersi yaz ve nereye yazdığını söyle.

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

Doldurulmuş bir `KANIT.md` şöyle görünür. Proje ve sayılar uydurma, yalnız biçimi gösteriyor.

```terminal Şematik örnek
# KANIT.md   proje: csv-haftalik-ozet

## Plan
tanım:   haftalik.csv'yi okur, ozet.md yazar, `python ozet.py haftalik.csv`
bitti:   ozet.md'de 7 gün ve toplam satırı var
dokunma: ornek/ klasörü

## Doğrulama
beklenen: ozet.md 7 gün + toplam, 8 satır
bozulan:  bir tarihi bozdum, kontrol KALDI (çıkış kodu 1)
test:     5 test koştu, 5 geçti

## Teslim
sürüm:    claude 2.1.284, macOS, Opus
ders:     "CSV'de tarih biçimi sabit" -> proje CLAUDE.md (bu koda ait)
```

- `## Plan`: üç satırın üçü de sınanabilir. "Bitti" satırı bir dosyaya bakarak doğrulanabiliyor.
- `bozulan:` satırı bu bölümün asıl şartı. Kontrolün düştüğünü görmeden o satır yazılamaz.
- `test:` satırında sayı sıfırdan büyük. "Test geçti" demek yetmez, kaç test koştuğu yazılı olmalı.
- `ders:` satırı katmanı da söylüyor. Aynı cümle kullanıcı dosyasına yazılsaydı başka projelere gürültü olurdu.

## Değerlendirme

Sayısal puan yok. Projeyi bitirdikten sonra aşağıdaki soruları kendine, dürüstçe sor. "Hayır" ya da "emin değilim" cevabı, geri dönüp yeniden okuman gereken bölümü gösterir.

- Projeyi başlamadan önce tek cümleyle ve ölçülebilir bir "bitti" ölçütüyle tanımladın mı? ({{bolum:2}})
- Bir sonuç beklenmedik çıktığında önce hangi katmandan geldiğini (model, araç, harness) sordun mu? ({{bolum:1}})
- Oturum şiştiğinde yeni oturuma geçtin mi, ve geçerken neyi taşıdığını biliyor musun? ({{bolum:3}})
- Her "tamamlandı" cümlesinin arkasında senin gördüğün bir çıktı var mı? ({{bolum:4}})
- Kuralların hangileri Claude'un kararında, hangileri Claude Code'un uyguladığı katmanda? Bunu açıklayabilir misin? ({{bolum:5}})
- Kontrolünü hatayı geri koyup düşürerek sınadın mı, yoksa yalnız geçtiğini mi gördün? ({{bolum:4}})
- Yarım bıraktığın bir şey bir dosyada yazılı mı, yoksa yalnız aklında mı? ({{bolum:12}})
- Paylaşılan bir kaynağı (dal, index, port, dosya) iki yerden kullandıysan çakışmayı nasıl önledin? ({{bolum:9}})
- Öğrendiğin dersi doğru katmana yazdın mı ve neden orası? ({{bolum:12}})
- Bu projeyi bir ekip arkadaşına devretsen, `KANIT.md` ve depo yeterli olur muydu? ({{bolum:3}})
- Bir şey sana en pahalıya geldiyse, o hata bir şeyin kırılmasından mı, yoksa hiçbir şeye bakmadan başarılı görünmesinden mi çıktı? ({{ek:deneyimler}} sayfasındaki vakalar bu soruya dönüyor.)

Kendini dürüstçe sorguladığında üç şeyi de yaz: neyi kaçırmış olabilirsin, hangi iddian en zayıf, hangi kararının gerekçesi yok. Rehberi bitirmiş olmanın işareti, bu üç cümleyi rahatça yazabilmek.

## Bağlantılar

Önceki bölümler: {{bolum:1}} {{bolum:2}} {{bolum:3}} {{bolum:4}} {{bolum:5}} {{bolum:6}} {{bolum:7}} {{bolum:8}} {{bolum:9}} {{bolum:10}} {{bolum:11}} {{bolum:12}}. Kontrol listesi: [[12.1]] [[12.2]] [[18.1]] [[18.2]] [[19.6]]. Ekler: {{ek:deneyimler}}, {{ek:sorun-giderme}}, {{ek:sozluk}}.

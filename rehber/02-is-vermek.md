# 2. İş vermek: bitiş çizgisini çizmek

_Temel · Belge kontrolü: 29 Ekim 2026_

İyi bir istek hedefin yanında bitiş ölçütünü, kısıtı, örneği ve okuru da söyler. Ölçütü Claude'un kendi koşturabileceği bir kanıta çevirirsen tek doğrulayıcı sen kalmazsın.

## Zihinsel model: iş vermek, bitiş çizgisini çizmektir

Claude Code'a verdiğin istek bir talimat olduğu kadar bir sözleşmedir. İsteğin "ne yapılacak" kısmı genellikle belli olur. Eksik kalan kısım "ne zaman bitti sayılacak" ve "neye dokunulmayacak" sorularıdır. Bu iki boşluğu sen doldurmazsan Claude kendi tahminiyle doldurur ve tahmin çoğu zaman makul görünür ama senin aklındakiyle aynı çıkmaz.

Belgenin en çok vurguladığı alışkanlık da budur: Claude'a işin sonucunu kendi kendine kontrol edebileceği bir yol ver. Testler, beklenen çıktı, ekran görüntüsü ya da bir komutun çıkış kodu bu yolu sağlar. Böyle bir ölçüt yoksa tek doğrulayıcı sen kalırsın ve her parçada Claude seni bekler. Ölçüt varsa Claude denemeyi, ölçmeyi ve düzeltmeyi kendi döngüsünde yapar.

İyi bir iş isteği beş parçadan oluşur:

| Parça | Cevapladığı soru | Eksikse ne olur |
|---|---|---|
| Hedef | Ne değişecek? | Claude başka bir şeyi çözer |
| Bitiş ölçütü | Hangi kanıtla biter? | İş hep "bitti gibi" görünür |
| Kısıt | Neye dokunma? | Çalışan kısmı bozarsın |
| Örnek | Çıktı nasıl görünür? | Biçim tutmaz |
| Okur ve yer | Kim, nerede kullanacak? | Ton ve ayrıntı seviyesi şaşar |

## Bitiş ölçütü ve doğrulanabilir kabul ölçütü

"Giriş formundaki hatayı düzelt" bir hedeftir, bitiş ölçütü değildir. "Boş e-postayla gönderince form kırmızı uyarı göstersin, `npm test` içinde bu durumu sınayan yeni bir test olsun ve tüm testler geçsin" ise bitiş ölçütüdür. İkinci cümlede Claude'un kendi başına koşturabileceği iki şey var: bir test ve bir komut. [3.1](../README.md#3-gorev)

Kabul ölçütünün sınaması basit: bir yabancı sadece bu cümleye bakıp "oldu" ya da "olmadı" diyebilir mi? "Hızlı açılsın" diyemez. "Ana sayfa soğuk açılışta iki saniyenin altında yüklensin, ölçümü şu komut versin" diyebilir. Ölçülemeyen bir ölçüt yazamıyorsan işi ikiye böl: önce ölçmeyi kuran bir iş, sonra ölçüte göre çalışan bir iş. [3.2](../README.md#3-gorev)

## Kısıt ve korunacak davranış

Claude bir hatayı düzeltirken yakındaki "çirkin" kodu da toparlayabilir. Niyeti iyidir ama diff'in okunmasını zorlaştırır ve çalışan bir davranışı bozabilir. Bunu kısıtla önlersin: hangi dosyaya dokunulacağını, hangi davranışın aynı kalacağını ve neyin yapılmayacağını söyle.

Güçlü kısıt cümlesi üç şey içerir: korunacak davranış, sınır ve kanıt. Örnek: "Ödeme akışı aynı çalışsın, yalnız `fiyat.py` içindeki yuvarlamayı değiştir, mevcut ödeme testleri değişmeden geçsin." Yasak listesi uzun olmak zorunda değil. Sadece Claude'un makul bulup yapacağı ama senin istemediğin şeyleri yaz. [3.4](../README.md#3-gorev)

## Örnek ve karşı örnek

Çıktının biçimini anlatmaktansa göstermek daha kısadır ve yanlış anlaşılmaz. Bir örnek "buna benzesin" der. Karşı örnek "buna benzemesin" der ve çoğu zaman daha çok bilgi taşır, çünkü Claude'un kolay yolunu keser.

Kurgu senaryo: Sibel haftalık durum özeti istiyor. Bir önceki haftanın özetini örnek olarak yapıştırıyor ve altına bir karşı örnek ekliyor: "Şu özet fazla uzundu, her satırın başında 'bu hafta' yazıyordu, bunu tekrarlama." İlk denemede format tutuyor. Karşı örnek olmasaydı Claude örneğin uzunluğunu ve sözcüklerini kopyalayacaktı. [3.5](../README.md#3-gorev)

## Plan modu ne zaman

Plan modu Claude'a dosyaları okutur ama düzenletmez. Sen planı onaylayınca uygulama başlar. Belgeye göre `Shift+Tab` ile durum çubuğunda `plan mode on` yazana kadar geçilir ya da `claude --permission-mode plan` ile başlanır. Bu iş akışı önerisi değil, belgelenmiş bir mod. Ne zaman kullanacağın ise senin kararın:

- Hedef belirsizse, birden çok dosyaya dokunuyorsa ya da yaklaşımı sen de bilmiyorsan önce plan iste.
- Değişiklik bir cümleyle diff olarak anlatılabiliyorsa, ör. bir yazım hatası ya da tek satırlık düzeltme, plan modu zaman kaybıdır.
- Gereksinimleri kendin de net bilmiyorsan belgenin önerisi: Claude'dan seni röportaj yapıp bir `SPEC.md` yazmasını iste, sonra temiz bir oturumda o dosyadan inşa et. [3.3](../README.md#3-gorev)

## "İyi"yi ölçüte çevirmek

"En iyi", "kaliteli", "profesyonel" gibi sözcükler Claude'a yön vermez, çünkü iyinin ne olduğunu senin kafanda kalan kıstaslar belirler. Sözcüğü bir ölçüte çevir. "Kaliteli bir README" yerine "kurulum üç komutta bitsin, ilk örnek çalışsın, bir ekran görüntüsü olsun" yaz. "İyi performans" yerine bir süre, bir bellek sınırı ya da bir kıyas komutu yaz. [4.1](../README.md#4-prompt)

## Okur ve kullanım yeri

Aynı bilgi bir mühendise yazılan commit mesajında, bir yöneticiye giden özette ve bir müşteri e-postasında farklı görünür. Claude okuru bilmezse ortalama bir ton seçer. "Bu metni bütçeyi onaylayacak yönetici okuyacak, teknik terim kullanma, tek ekranı geçmesin" demek sonucu belirgin biçimde değiştirir. Kullanım yeri de aynı işi görür: bir e-posta, bir slayt, bir kod yorumu, bir issue. [4.2](../README.md#4-prompt)

## Karar kuralları

- **İsteği göndermeden önce şunu sor:** Claude bitirdiğinde "oldu" demek için hangi kanıta bakacağım? Cevap yoksa ölçütü ekle.
- **Ölçütü Claude'un koşturabileceği biçimde yaz.** Bir test, bir komut, bir dosyada beklenen satır. Senin gözüne kalan kontrol seni darboğaz yapar.
- **Kısıtı dört parça yap:** neye dokunabilir, neye dokunamaz, hangi davranış aynı kalır, neyin kanıtı var.
- **Biçim önemliyse bir örnek yapıştır.** Çoğu zaman bir de karşı örnek ekle.
- **Küçük ve net işi doğrudan yaptır.** Büyük ve belirsiz işte önce plan iste.
- **Sıfatları ölçüte çevir.** Okuru ve yeri her yazı işinde söyle.

## Hata biçimleri

**Gerçek vaka: ölçüt yoktu, yeşil yanıltıcıydı.** Bir test komutuna süitin okunur adı filtre olarak verildi. Eşleşen test çıkmadı, sıfır test koştu ve çıktı "başarılı" dedi. İstekte yalnız "testler geçsin" yazıyorsa bu yeşil kabul edilir. "En az şu kadar test koşsun ve geçsin" yazıyorsa sıfır hemen göze çarpar. Ayrıntısı [Gerçek deneyimlerden on ders](../ekler/deneyimler.md) sayfasında D02. [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md) bölümü bu vakayı kanıt açısından işler.

**Gerçek vaka: olgu, eski rapordan geldi.** On gün önceki bir denetim notu "uygulama yalnız bir ülkede satışta" diyordu. Not oturuma girdi ve öneri ona dayandı. Yönetim panelinde uygulama 175 ülkedeydi. İsteğin içine yapıştırdığın her olgu, ölçütün bir parçası olur. Yanlış olgu yanlış ölçüt doğurur. Ayrıntısı D10.

**Kurgu senaryo: kısıtsız düzeltme.** Kaan bir sipariş toplamı hatasını düzelttirir. Claude hatayı düzeltir, ayrıca yakındaki üç fonksiyonun adını "daha okunur" olacak şekilde değiştirir. Diff 40 satıra çıkar, Kaan dört fonksiyonun hangisinin gerçekten gerektiğini ayıklayamaz ve hepsini geri alır. "Yalnız `toplam.py`, başka dosya ve ad değişikliği yok" kısıtı bunu önlerdi.

## Alıştırma: aynı iş, iki istek

Herhangi bir git deposunda yap. Küçük bir iş seç, ör. bir fonksiyona giriş doğrulaması eklemek ya da bir betiğe `--yardim` seçeneği koymak.

1. İlk isteği zayıf yaz, tek cümle: "X'e doğrulama ekle". İş bitince çıktıyı ve `git diff --stat` satırını kaydet. Sonra `git restore .` ile değişikliği geri al.
2. Aynı işi bu sefer güçlü isteyle ver. İsteğe şunlar girsin: bitiş ölçütü (hangi komut, hangi çıktı), iki kabul ölçütü, bir kısıt (dokunulacak dosya, korunacak davranış), biçim için bir örnek ve bir karşı örnek.
3. İkisini karşılaştır: diff kaç dosyaya ve kaç satıra değdi? Claude kaç kez durup sana soru sordu? Test ya da komut kanıtı sundu mu?
4. Büyük bir iş seçtiysen ikinci denemeyi plan modunda başlat ve planı onaylamadan önce kısıtlarına uyup uymadığına bak.

**Bitti sayılması için:** iki satırlık bir karşılaştırma tablosu (dosya sayısı, satır sayısı, soru sayısı, kanıt var mı) ve bir cümle: hangi ölçüt farkı yarattı.

## Bağlantılar

Kontrol listesi: [3.1](../README.md#3-gorev) [3.2](../README.md#3-gorev) [3.3](../README.md#3-gorev) [3.4](../README.md#3-gorev) [3.5](../README.md#3-gorev) [4.1](../README.md#4-prompt) [4.2](../README.md#4-prompt). Önceki bölüm: [Bölüm 1: Zihinsel model: döngü, bağlam ve harness](01-zihinsel-model.md). Sonraki: [Bölüm 3: Oturum: masayı doğru yönetmek](03-oturumu-yonetmek.md), [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md). Ekler: [Komutlar ve kısayollar](../ekler/komutlar.md), [İpuçları ve püf noktaları](../ekler/ipuclari.md).

---

[← Bölüm 1](01-zihinsel-model.md) · [İçindekiler](README.md) · [Bölüm 3 →](03-oturumu-yonetmek.md)

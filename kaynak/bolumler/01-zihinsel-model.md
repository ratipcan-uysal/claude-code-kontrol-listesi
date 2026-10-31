## Zihinsel model: bir döngü, üç parça

Claude Code'a bir iş verdiğinde arka planda bir döngü döner. Belge bu döngüyü üç evreyle anlatır: bağlam toplamak, harekete geçmek ve sonucu doğrulamak. Evreler iç içe geçer. Claude bir dosyayı okur, bir şey dener, sonucu görür, yeniden okur. Sen de döngünün herhangi bir anında araya girebilirsin.

{{sekil:b01-dongu|Döngünün üç evresi sırayla yanar. Sen her an araya girebilirsin. Hareket kapalıysa üçü de yanık durur.}}

Döngüyü üç parça yürütür:

- **Model** karar verir: hangi dosyayı okuyacağına, hangi komutu deneyeceğine, ne zaman duracağına.
- **Araçlar** iş yapar: dosya okur ve düzenler, arama yapar, kabuk komutu çalıştırır, web'e çıkar, alt ajan başlatır.
- **Harness** modeli saran düzendir. Hangi aracın izinli olduğunu, bağlama neyin gireceğini, hangi hook'un çalışacağını o belirler. Claude Code'un kendisi bir harness'tır.

{{sekil:b01-uc-parca|Harness modeli ve araçları sarar. Model istek gönderir, araçlar sonuç döndürür.}}

Rehberde sık geçen üç terim: **hook**, bir olay olunca kendiliğinden çalışan küçük bir betiktir. **Skill**, Claude'a bir işin nasıl yapılacağını anlatan, yeniden kullanılabilir bir tarif dosyasıdır. **MCP**, Claude'u dış bir sisteme araç olarak bağlayan sunucudur.

Bu ayrım ilk bakışta akademik görünür. Ama Claude Code'la yaşadığın hemen her sürprizin açıklaması bu üç parçadan birindedir. "Claude kuralımı unuttu" bir bağlam sorunudur. "Claude bu komutu çalıştırmadı" bir izin sorunudur. "Claude yanlış dosyayı düzenledi" bir model kararıdır. Uzman, sonucu gördüğünde önce hangi parçadan geldiğini sorar.

## Bağlam penceresi: modelin gördüğü tek şey

Model yalnız bağlam penceresinde olanı görür. Diskteki dosyaları, dünkü konuşmayı, senin aklındaki niyeti görmez. Pencerede konuşma geçmişi, okunan dosyaların içeriği, komut çıktıları, CLAUDE.md, otomatik bellek, yüklenmiş skill'ler ve sistem talimatları durur.

Bir kısmı oturum başında yüklenir, bir kısmı gerektiğinde:

| Ne zaman | Ne yüklenir |
|---|---|
| Oturum başında | CLAUDE.md dosyaları, otomatik belleğin dizin dosyası, skill açıklamaları, MCP araçlarının adları |
| Gerektiğinde | Okunan dosyalar, araç çıktıları, çağrılan skill'in gövdesi, eşleşen dosyaya dokununca yol kuralları, alt dizin CLAUDE.md'leri |

{{sekil:b01-baglam-penceresi|Aynı tablo pencerenin içinden: sol tarafı oturum açılırken dolar, sağ tarafı iş ilerledikçe.}}

Her yeni oturum boş bir pencereyle başlar. Oturumdan oturuma taşınan yalnız diskte duran şeylerdir: CLAUDE.md her seferinde yeniden okunur, otomatik bellek yeniden yüklenir, dosyalar yerinde durur. Konuşmanın kendisi taşınmaz. Aynı konuşmaya dönmenin tek yolu `--continue` ya da `--resume` ile o oturumu açmaktır.

Pencere dolunca Claude Code konuşmayı özetler. Pencerenin boyutu modele ve plana göre değişir. Sıkıştırma, yerel 1 milyon token'lık pencereli modellerde varsayılan olarak 967 bin civarında tetiklenir, 200 bin token'lık pencerede sınıra gelince. Belge sıkıştırmanın bedelini açıkça yazar: konuşmanın başındaki ayrıntılı talimatlar kaybolabilir. Proje kökündeki CLAUDE.md ve otomatik bellek sıkıştırmadan sonra diskten yeniden eklenir. Sohbette verdiğin bir talimat ise özetin insafına kalır.

Pencerenin içini kendin görebilirsin. Aşağıdaki çıktı, boş bir klasörde `claude -p "/context"` komutuyla alındı:

```terminal Gerçek çıktı, kısaltılmış
$ claude -p "/context"
## Context Usage

**Model:** claude-opus-5-5
**Tokens:** 37.4k / 1m (4%)

### Estimated usage by category

| Category | Tokens | Percentage |
|----------|--------|------------|
| System prompt | 2.2k | 0.2% |
| System tools | 23.5k | 2.4% |
| System tools (deferred) | 29.8k | 3.0% |
| Custom agents | 714 | 0.1% |
| Memory files | 4.5k | 0.5% |
| Skills | 6.5k | 0.6% |
| Free space | 929.6k | 93.0% |
| Autocompact buffer | 33k | 3.3% |

[ajan, bellek dosyası ve skill ayrıntı tabloları çıkarıldı]
```

- **Tokens satırı:** Pencere 1 milyon token. Boş bir klasörde yeni oturum açılır açılmaz 37,4 bin token, yani yüzde 4 dolu. "Boş pencere" bile tamamen boş değil.
- **System prompt ve System tools satırları:** Harness'in kendi koyduğu talimat ve araç tanımları. Senin yazdığın şey değil. "Deferred" olanların yalnız adı yüklüdür, ayrıntısı gerektiğinde gelir.
- **Memory files satırı:** CLAUDE.md dosyalarının payı. Bu makinede yalnız kullanıcı düzeyindeki CLAUDE.md var, 4,5 bin token. Projeye bir CLAUDE.md eklenirse bu satır büyür.
- **Skills satırı:** Yalnız skill açıklamaları. Gövde, skill çağrılınca girer.
- **Free space ve Autocompact buffer:** Boş alan ve sıkıştırma payı. 1 milyondan 33 bin çıkınca 967 bin kalır, yukarıda geçen sıkıştırma eşiğiyle aynı sayı.

## Neyi kim yapar

| Soru | Cevabı veren | Nereden görürsün |
|---|---|---|
| Claude bunu biliyor mu? | Bağlam penceresi | `/context`, `/memory` |
| Bunu yapmaya karar verecek mi? | Model | Konuşmanın kendisi, `Ctrl+O` transkript |
| Yapmasına izin var mı? | Harness: izin kuralları, mod, hook | `/permissions`, `/hooks`, `/status` |
| Yaptığı şey doğru mu? | Kimse kendiliğinden söylemez | Test, ekran, diff: senin kanıtın |

Son satır bilerek boş bırakıldı. Döngünün "doğrula" evresi modelin kendi kontrolüdür. Senin kontrolünün yerini tutmaz. Bunu {{bolum:4}} ve kontrol listesinin doğrulama bölümü ayrıntılandırıyor.

## Alt ajan: ayrı bir pencere

{{sekil:b01-alt-ajan|Alt ajan ana oturumdan yalnız devir mesajını alır. Geriye yalnız özet döner.}}

Alt ajan kendi bağlam penceresinde çalışır ve ana oturuma yalnız bir özet döndürür. Konuşma geçmişini, okunmuş dosyaları ve çağrılmış skill'leri görmez. Ana oturum ona görevi anlatan bir devir mesajı yazar, alt ajan oradan başlar. Bu iki sonuç doğurur. Geniş bir aramayı alt ajana vermek ana pencereyi temiz tutar. Ama alt ajan, senin oturumda söylediğin bir şeyi ancak devir mesajına girdiyse bilir. Bir istisna var: fork, ana konuşmanın kopyasıyla başlar.

## Karar kuralları

- **Claude bir şeyi "bilmiyorsa" önce bağlama bak.** Bilgi pencerede yoksa model için yoktur. `/context` neyin yüklendiğini, `/memory` hangi talimat dosyalarının okunduğunu gösterir. [[2.2]]
- **Oturum boyunca geçerli olması gereken talimatı sohbete değil dosyaya yaz.** Sıkıştırmadan sonra dosya geri gelir, sohbet gelmez. [[2.6]]
- **Konu değişince yeni oturum aç.** Eski işin dosyaları ve kararları penceredeyse yeni işi de etkiler. [[2.3]]
- **Çok dosya okuyacak bir araştırmayı alt ajana ver.** Ana pencereye yalnız sonuç girer. [[2.4]]
- **Büyük çıktıyı pencereye değil dosyaya aldır.** Uzun bir log'un yüzde birlik kısmı gerekiyorsa geri kalanı yer kaplamasın. [[2.5]]
- **Bir sürprizi açıklarken üç soruyu sırayla sor:** Bağlamda var mıydı? Model ne karar verdi? Harness izin verdi mi?

## Hata biçimleri

**Gerçek vaka: kural vardı, model görmedi.** Ortak kurallar bir dosyaya taşınıp dört projenin CLAUDE.md'sine import edildi. `claude -p` ile koşan, ekransız ve soru sormayan headless oturumda model yalnız import satırını gördü, dosyanın içeriğini görmedi, çünkü proje dışı import onayı o koşumda hiç sorulmamıştı. Model kuralı "çiğnemedi", kural hiç bağlama girmedi. Ayrıntısı {{ek:deneyimler}} sayfasında D07.

**Gerçek vaka: bağlamdaki eski bilgi, model için gerçektir.** On gün önceki bir rapor "uygulama yalnız bir ülkede satışta" diyordu ve bu cümle oturuma yapıştırıldı. Model buna dayanarak öneri yaptı. Gerçekte uygulama 175 ülkede satıştaydı. Pencereye giren her cümle, kaynağına bakılmadıkça doğru kabul edilir. Ayrıntısı D10.

**Kurgu senaryo: "Dün söylediğimi unuttu."** Elif bir gün boyunca Claude'la bir rapor betiği üzerinde çalışır ve tarih biçiminin gün/ay/yıl olacağını sohbette söyler. Ertesi gün yeni bir oturum açar, betik ay/gün/yıl üretir. Model unutmadı, o bilgi yeni pencerede hiç yoktu. Kural CLAUDE.md'ye yazılınca sorun bir daha çıkmaz.

```terminal Kurgu, şematik
# 1. gün, oturum A
> tarih biçimi gün/ay/yıl olsun
(yalnız sohbette, dosyaya yazılmadı)
```

```terminal Kurgu, şematik
# 2. gün, yeni oturum B
> /context
konuşma geçmişi: boş pencere
çıktı: ay/gün/yıl
```

Birinci panelde söz yalnız sohbette kaldı, hiçbir dosyaya girmedi. İkinci panelde pencere yeni ve konuşma geçmişi boş. Bilgi diskte olmadığı için model varsayılan biçime düştü.

## Alıştırma: bağlamı ölç

Herhangi bir git deposunda yap.

1. Yeni bir oturum aç. Hiçbir şey sormadan `/context` yaz, çıktıyı bir dosyaya kaydet.
2. Depodaki en büyük kaynak dosyalardan birini Claude'a okut ve ne yaptığını özetlemesini iste. `/context` çıktısını yeniden kaydet.
3. `/memory` ile hangi talimat dosyalarının yüklendiğine bak. Listede beklemediğin ya da eksik bulduğun bir dosya var mı?
4. CLAUDE.md'ye geçici bir satır ekle, ör. "Bu projede tarih biçimi gün/ay/yıl." Yeni bir oturum aç ve Claude'a dosya okutmadan tarih biçimini sor. Sonra satırı sil.

**Bitti sayılması için:** iki `/context` çıktısı ve üç cümle. Hangi kategori ne kadar büyüdü, neden büyüdü, 4. adımda Claude bilgiyi nereden aldı.

## Bağlantılar

Kontrol listesi: [[2.1]] [[2.2]] [[2.3]] [[2.4]] [[2.5]] [[2.6]] [[1.5]] [[1.7]]. Ekler: {{ek:komutlar}}, {{ek:dosyalar}}.

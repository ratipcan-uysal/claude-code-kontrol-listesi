## Zihinsel model: bir döngü, üç parça

Claude Code'a bir iş verdiğinde arka planda bir döngü döner. Belge bu döngüyü üç evreyle anlatır: bağlam toplamak, harekete geçmek ve sonucu doğrulamak. Evreler iç içe geçer. Claude bir dosyayı okur, bir şey dener, sonucu görür, yeniden okur. Sen de döngünün herhangi bir anında araya girebilirsin.

Döngüyü üç parça yürütür:

- **Model** karar verir: hangi dosyayı okuyacağına, hangi komutu deneyeceğine, ne zaman duracağına.
- **Araçlar** iş yapar: dosya okur ve düzenler, arama yapar, kabuk komutu çalıştırır, web'e çıkar, alt ajan başlatır.
- **Harness** modeli saran düzendir. Hangi aracın izinli olduğunu, bağlama neyin gireceğini, hangi hook'un çalışacağını o belirler. Claude Code'un kendisi bir harness'tır.

Bu ayrım ilk bakışta akademik görünür. Ama Claude Code'la yaşadığın hemen her sürprizin açıklaması bu üç parçadan birindedir. "Claude kuralımı unuttu" bir bağlam sorunudur. "Claude bu komutu çalıştırmadı" bir izin sorunudur. "Claude yanlış dosyayı düzenledi" bir model kararıdır. Uzman, sonucu gördüğünde önce hangi parçadan geldiğini sorar.

## Bağlam penceresi: modelin gördüğü tek şey

Model yalnız bağlam penceresinde olanı görür. Diskteki dosyaları, dünkü konuşmayı, senin aklındaki niyeti görmez. Pencerede konuşma geçmişi, okunan dosyaların içeriği, komut çıktıları, CLAUDE.md, otomatik bellek, yüklenmiş skill'ler ve sistem talimatları durur.

Bir kısmı oturum başında yüklenir, bir kısmı gerektiğinde:

| Ne zaman | Ne yüklenir |
|---|---|
| Oturum başında | CLAUDE.md dosyaları, otomatik belleğin dizin dosyası, skill açıklamaları, MCP araçlarının adları |
| Gerektiğinde | Okunan dosyalar, araç çıktıları, çağrılan skill'in gövdesi, eşleşen dosyaya dokununca yol kuralları, alt dizin CLAUDE.md'leri |

Her yeni oturum boş bir pencereyle başlar. Oturumdan oturuma taşınan yalnız diskte duran şeylerdir: CLAUDE.md her seferinde yeniden okunur, otomatik bellek yeniden yüklenir, dosyalar yerinde durur. Konuşmanın kendisi taşınmaz. Aynı konuşmaya dönmenin tek yolu `--continue` ya da `--resume` ile o oturumu açmaktır.

Pencere dolunca Claude Code konuşmayı özetler. Pencerenin boyutu modele ve plana göre değişir. 1 milyon token'lık pencerede sıkıştırma varsayılan olarak 967 bin civarında tetiklenir, 200 bin token'lık pencerede sınıra gelince. Belge sıkıştırmanın bedelini açıkça yazar: konuşmanın başındaki ayrıntılı talimatlar kaybolabilir. Proje kökündeki CLAUDE.md ve otomatik bellek sıkıştırmadan sonra diskten yeniden eklenir. Sohbette verdiğin bir talimat ise özetin insafına kalır.

## Neyi kim yapar

| Soru | Cevabı veren | Nereden görürsün |
|---|---|---|
| Claude bunu biliyor mu? | Bağlam penceresi | `/context`, `/memory` |
| Bunu yapmaya karar verecek mi? | Model | Konuşmanın kendisi, `Ctrl+O` transkript |
| Yapmasına izin var mı? | Harness: izin kuralları, mod, hook | `/permissions`, `/hooks`, `/status` |
| Yaptığı şey doğru mu? | Kimse kendiliğinden söylemez | Test, ekran, diff: senin kanıtın |

Son satır bilerek boş bırakıldı. Döngünün "doğrula" evresi modelin kendi kontrolüdür. Senin kontrolünün yerini tutmaz. Bunu {{bolum:5}} ve kontrol listesinin doğrulama bölümü ayrıntılandırıyor.

## Alt ajan: ayrı bir pencere

Alt ajan kendi bağlam penceresinde çalışır ve ana oturuma yalnız bir özet döndürür. Konuşma geçmişini, okunmuş dosyaları ve çağrılmış skill'leri görmez. Ana oturum ona görevi anlatan bir devir mesajı yazar, alt ajan oradan başlar. Bu iki sonuç doğurur. Geniş bir aramayı alt ajana vermek ana pencereyi temiz tutar. Ama alt ajan, senin oturumda söylediğin bir şeyi ancak devir mesajına girdiyse bilir. Bir istisna var: fork, ana konuşmanın kopyasıyla başlar.

## Karar kuralları

- **Claude bir şeyi "bilmiyorsa" önce bağlama bak.** Bilgi pencerede yoksa model için yoktur. `/context` neyin yüklendiğini, `/memory` hangi talimat dosyalarının okunduğunu gösterir. [[2.2]]
- **Oturum boyunca geçerli olması gereken talimatı sohbete değil dosyaya yaz.** Sıkıştırmadan sonra dosya geri gelir, sohbet gelmez. [[2.6]]
- **Konu değişince yeni oturum aç.** Eski işin dosyaları ve kararları penceredeyse yeni işi de etkiler. [[2.3]]
- **Çok dosya okuyacak bir araştırmayı alt ajana ver.** Ana pencereye yalnız sonuç girer. [[2.4]]
- **Büyük çıktıyı pencereye değil dosyaya aldır.** Uzun bir log'un yüzde birlik kısmı gerekiyorsa geri kalanı yer kaplamasın. [[2.5]]
- **Bir sürprizi açıklarken üç soruyu sırayla sor:** Bağlamda var mıydı? Model ne karar verdi? Harness izin verdi mi?

## Hata biçimleri

**Gerçek vaka: kural vardı, model görmedi.** Ortak kurallar bir dosyaya taşınıp dört projenin CLAUDE.md'sine import edildi. Etkileşimli oturumda her şey yolundaydı. Headless koşumda model yalnız import satırını gördü, dosyanın içeriğini görmedi, çünkü proje dışı import onayı o koşumda hiç sorulmamıştı. Model kuralı "çiğnemedi", kural hiç bağlama girmedi. Ayrıntısı {{ek:deneyimler}} sayfasında D07.

**Gerçek vaka: bağlamdaki eski bilgi, model için gerçektir.** On gün önceki bir rapor "uygulama yalnız bir ülkede satışta" diyordu ve bu cümle oturuma yapıştırıldı. Model buna dayanarak öneri yaptı. Gerçekte uygulama 175 ülkede satıştaydı. Pencereye giren her cümle, kaynağına bakılmadıkça doğru kabul edilir. Ayrıntısı D10.

**Kurgu senaryo: "Dün söylediğimi unuttu."** Elif bir gün boyunca Claude'la bir rapor betiği üzerinde çalışır ve tarih biçiminin gün/ay/yıl olacağını sohbette söyler. Ertesi gün yeni bir oturum açar, betik ay/gün/yıl üretir. Model unutmadı, o bilgi yeni pencerede hiç yoktu. Kural CLAUDE.md'ye yazılınca sorun bir daha çıkmaz.

## Alıştırma: bağlamı ölç

Herhangi bir git deposunda yap.

1. Yeni bir oturum aç. Hiçbir şey sormadan `/context` yaz, çıktıyı bir dosyaya kaydet.
2. Depodaki en büyük kaynak dosyalardan birini Claude'a okut ve ne yaptığını özetlemesini iste. `/context` çıktısını yeniden kaydet.
3. `/memory` ile hangi talimat dosyalarının yüklendiğine bak. Listede beklemediğin ya da eksik bulduğun bir dosya var mı?
4. CLAUDE.md'ye geçici bir satır ekle, ör. "Bu projede tarih biçimi gün/ay/yıl." Yeni bir oturum aç ve Claude'a dosya okutmadan tarih biçimini sor. Sonra satırı sil.

**Bitti sayılması için:** iki `/context` çıktısı ve üç cümle. Hangi kategori ne kadar büyüdü, neden büyüdü, 4. adımda Claude bilgiyi nereden aldı.

## Bağlantılar

Kontrol listesi: [[2.1]] [[2.2]] [[2.3]] [[2.4]] [[2.5]] [[2.6]] [[1.5]] [[1.7]]. Ekler: {{ek:komutlar}}, {{ek:dosyalar}}.

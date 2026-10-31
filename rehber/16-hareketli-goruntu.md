# 16. Hareketli görüntü: ajan videoyu izleyemez

_Uzman · Belge kontrolü: 29 Ekim 2026_

Ajan videoyu izleyemez ama kareye bakabilir ve sayıyı ölçebilir. Zaman planı metinden hesaplanır, kontroller render'dan önce koşar, kare tablosu ve olaya bağlı ses aynı plandan beslenir.

## Zihinsel model: videoyu izleyemez, kareye bakar, sayıyı ölçer

Claude Code bir videoyu baştan sona izleyemez. Ama tek bir kareye bakabilir, bir dosyadan sayı okuyabilir ve bir betik yazıp onu çalıştırabilir. Hareketli görüntü işinin bütün yöntemi bu üç yeteneğin üstüne kurulur: videoyu izlemek yerine onu karelere ve sayılara çevir, ajan o karelere baksın ve o sayıları okusun.

Bu bölümün örneği yazarın kendi motion kiti. Instagram için kinetik tipografi ve anlatı videosu üreten, Node, ffmpeg ve Chrome dışında bağımlılığı olmayan küçük bir araç seti. Bölümdeki fikirler başka bir araçla da kurulur.

Kitin döngüsü yedi adımdır:

1. Metinden zaman planını hesapla.
2. Sahneyi bu plana bağlı yaz.
3. Ölç. Kontroller geçmeden ilerleme.
4. Kare tablosuna bak. Sayının göremediği şeyi göz yakalar.
5. Sesi aynı plandan üret.
6. Render al.
7. Çıkan dosyada son kontrolü yap.

Render en pahalı adımdır, hata ne kadar geç yakalanırsa o kadar iş çöpe gider. [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md) bölümündeki kanıt fikri burada hareketli görüntüye uyarlanıyor.

## Zamanı elle yazma: tek plan, adlı olaylar

Videoda en çok bozulan şey zamanlamadır. Bir cümle uzar, ses yanlış yerde kalır. Çözüm zamanı hiçbir yere elle yazmamaktır. Kitte planlayıcı her sahnenin kelime sayısına bakıp giriş, vurgu, oturma ve çıkış anlarını hesaplar ve tek bir dosyaya yazar. Okuma süresi de bu hesabın içindedir: metin yerine oturduktan sonra en az bir saniye, üç kelimeden sonraki her kelime için çeyrek saniye, finalde en az iki buçuk saniye ekranda kalır.

Sahnedeki özel hareketler bu anlara adla bağlanır. Olayı "vurgu anından 0,1 saniye sonra" ya da "giriş anından 0,62 saniye sonra" diye tanımlarsın, saniye değeri olarak değil. Ses de aynı olayları okur. Bir çarpma sesi "çöküş olayına" konur, "14,2. saniyeye" konmaz. Metni değiştirdiğinde plan yeniden hesaplanır, görüntü, ses ve kontroller birlikte kayar. Hiçbiri senin elle düzeltmeni beklemez.

Bunu Claude'a kural olarak ver: sahne kodunda saniye değeri yazmak yasak. Kitin talimat dosyasında da bu satır var.

_Şekil: Plan olayları adlandırır. Sahne, ses ve kontrol aynı adlı olaylardan okur. Oynatma çizgisi soldan sağa ilerler. ([web sürümünde](16-hareketli-goruntu.html#sekil-b16-tek-zaman-cizelgesi))_

## Render'dan önce ölçüm

Kit videoyu kodlamadan, sahneyi kare kare çizerek ölçer. Anlatıdaki kontroller:

| Kontrol | Neye bakar |
|---|---|
| ilk kare | 0. karede okunur metin var mı, küçük resim boş kalmasın |
| okuma süresi | Her metin, kelime sayısına göre yeterince ekranda kalıyor mu |
| metin sabit | Oturduktan sonra çıkışa kadar metin katmanı kıpırdıyor mu |
| güvenli alan | Metin ve çizimler arayüzün örttüğü üst, alt ve sağ bölgelere giriyor mu |
| hareket | Arka planda yarım saniyeden uzun donma var mı |
| senkron | Kelime zamanları gerçekten konuşmaya oturuyor mu (anlatı videosunda) |

Render'dan sonra kit MP4'te ses seviyesini de ölçer. Hedef -14 LUFS civarı, tepe -1 dBTP altı. Tek komut hepsini sırayla koşar ve ölçüm kalırsa render yapmaz.

Alıştırmanın 3. adımında göreceğin çıktı aşağıdaki gibi olur. Gerçek bir koşum değil, biçimi gösterir.

**Şematik örnek**

```text
$ node olc.js plan.json
okuma süresi   sahne 2: 7 kelime, 1,2 sn (en az 2,0 sn)   KALDI
ilk kare       geçti
metin sabit    geçti
sonuç: KALDI   çıkış kodu 1, render yapılmadı
$ node olc.js plan.json    # süre düzeltildikten sonra
okuma süresi   sahne 2: 7 kelime, 2,4 sn (en az 2,0 sn)   GEÇTİ
sonuç: GEÇTİ   çıkış kodu 0
```

- 1. satır: ölçüm neye baktığını, ölçtüğü değeri ve eşiği birlikte yazar. Yalnız "kaldı" yazan bir kontrol neyi düzelteceğini söylemez.
- 4. satır: çıkış kodu sıfırdan farklı olduğu için sonraki adım (render) başlamaz.
- Son iki satır: aynı ölçümün önce düşmesi ve sonra geçmesi bölümün aradığı kanıttır. Yalnız geçen bir ölçüm hiçbir şeye bakmıyor olabilir.

Güvenli alan kontrolünün inceliği şurada: sahne, çizdiği her şeyin sınırını bildirir ve kontrol bunları kamera yakınlaşması ve sarsıntı dahil, gerçekte ekrana düştükleri yerde tartar.

## Kare tablosu: ajanın gözü

Ölçüm sayıyı verir, ama "bu kare çirkin mi, iki öğe üst üste mi bindi" sorusunu sayı cevaplamaz. Bunun için kit her sahne ve her adlı olay için tek bir kare üretir ve hepsini altı sütunlu tek bir PNG'ye dizer. Her karenin altında zaman etiketi vardır, üstüne güvenli alanlar yarı saydam kırmızıyla bindirilir. Ajan bu tek görüntüyü açar ve her karede şuna bakar: tek odak noktası var mı, giren ve çıkan öğe çakışıyor mu, metin telefon genişliğinde okunur mu, kaynak yazısı arayüz bölgesinin dışında mı.

_Şekil: Kare tablosunun şeması. Gerçek bir tablo değil, yalnız düzeni gösteriyor. ([web sürümünde](16-hareketli-goruntu.html#sekil-b16-kare-tablosu-sema))_

Aynı fikir açık kaynak claude-motion projesinde de var. README'sine göre orada da ajanlar videoyu izleyemez ama kareye bakar, her vuruş için zaman damgalı bir kare tablosu çıkar, tek bir zaman çizelgesi sahneyi, sesi ve incelemeyi besler ve hareket kuralları sayılarla yazılır. Proje MIT lisanslı. Bunları yalnız o README'ye dayanarak aktarıyorum, projeyi çalıştırmadım.

## Ses: vuruş olaya bağlı, kayıt önce kontrolden geçer

Sesi de koddan üret ve olaya bağla. Kitte sesler sentezlenir, örnek dosya ya da lisanslı müzik yoktur. Betik her sesi bir olayın adıyla yerleştirir ve bir dalga görüntüsü çıkarır, üstünde olay çizgileri vardır. Ajan dalgaya bakıp her vuruşun bir çizginin üstüne oturup oturmadığını görür. Seviye için ayrıca sayı var: mastering -14 LUFS'a ve bir true peak tavanına kendisi oturtur.

Seslendirmeli videoda önce kayıt gelir. Kitin `master` aşaması ham kaydı işlemeden önce bakar. Yaygın kırpılma, yüksek gürültü tabanı ya da ağır yankı varsa durur ve neyin değişip yeniden kaydedileceğini söyler: "giriş kazancını düşürüp yeniden kaydet", "halı ya da perde olan bir odada kaydet". Sonra paragraf seviyeleri, duraklamalar ve tepe eşiklere göre ayarlanır, rapor yazılır.

Bir sınır var ve kit onu açıkça yazar: kulak kullanıcıda. Ajan sesi dinleyemez. Kullanıcı "30. saniyede kesik" der, ajan ara aşamaları karşılaştırıp sorunun kayıttan mı işlemeden mi geldiğini bulur ve her düzeltmeden sonra önce ve sonra parçası verir. Ölçüm ön elemedir, onay kulakla verilir.

## Hareket kuralları

Kit hareketi zevke bırakmaz, kural yazar:

- Her hareketin bir amacı olur. Anlatıda bu, söylenen kelimeye bağlı olmaktır. Bağlanamayan hareket eklenmez.
- Çıkış girişten sadedir. Giden metin kısa kayar ve hafif bulanır, dikkat sıradaki cümlededir.
- Abartıyı nadir anlara ayır. Üstünden geçip oturan eğriyi ve sarsıntıyı yalnız ana anlarda kullanırsın, sarsıntıyı videoda en çok iki üç kez.
- Aynı efekt her yerde tekrar ederse vurgu olmaktan çıkar. Bir paragrafta en çok bir ana an olur, art arda iki sayfada aynı çizim tipi kullanılmaz.
- Konuşmanın üstüne efekt sesi binmez. Efekt, ilk heceyi örtmeyecek kadar önce biter ve konuşmanın çok altında kalır.

Ajan bu kuralların ihlalini kare tablosunda arar.

## Karar kuralları

- **Zamanı plandan al.** Elle yazılmış her saniye değeri, bir sonraki metin değişikliğinde bozulacak bir borçtur.
- **Her kontrolü bozarak sına.** Yeni bir ölçüm yazdıysan onu bilerek bozuk bir projede çalıştır ve düştüğünü gör. [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md) bölümündeki ilke burada da geçerli.
- **Renderdan önce ölç, renderdan sonra sesi ve süreyi yeniden ölç.** Ara dosyada geçen kontrol son dosyada geçmeyebilir.
- **Görseli sayıyla değil kareyle onayla.** Sayı çakışmayı, kare hiyerarşiyi gösterir.
- **Ses sorununu önce kaynağında ara.** Kayıttan mı, işlemeden mi geldiğini ayır, sonra düzelt.
- **"Çok statik" şikâyetini ölçüye çevir.** Kitte kural: arka planda en uzun donma yarım saniyeyi geçmez.

## Hata biçimleri

**Gerçek vaka (kit, 29 Ekim 2026): ilk sürüm reddedildi.** Anlatı videosunun ilk biçimi bir kupür görseli ve altına yazılan altyazıydı. Kullanıcı bunu statik buldu ve reddetti. Çıkan ders sayfa sayfa bir defter dili oldu: her cümleye, kelime söylendiği an çizilmeye başlayan bir çizim bağlandı. Hareket kuralının "söylenen kelimeye bağlı" maddesi bu reddin ürünü. "Çok statik" itirazını sayıya çeviren hareket kontrolü de bu yüzden var.

**Gerçek vaka (kit, 29 Ekim 2026): kontrol çizimi görmedi.** Güvenli alan kontrolü yalnız metin kutularını tartıyordu. Sahneye çizimler girince bir figür arayüzün örttüğü bölgeye inebiliyordu ve kontrol yine geçiyordu. Çözüm, sahnenin çizim sınırlarını bildirmesi ve kontrolün onları da tartmasıydı. Test, çizimi kasten alt bölgeye indirip kontrolün düştüğünü doğruluyor.

**Gerçek vaka (kit, 30 Ekim 2026): efekt ilk heceyi yedi.** Her paragrafın başındaki sayfa çevirme sesi, kullanıcıya göre konuşmanın ilk hecesini örtüyordu ("sayfanın başı yenmiş"). Ölçüm bunu yakalamadı, kullanıcının kulağı yakaladı. Kural şu oldu: efekt ilk heceden en az 0,1 saniye önce biter ve konuşmadan en az 10 dB aşağıda kalır, çizim başına kalem sesi tamamen kalktı.

**Gerçek vaka (ölçüm defteri, 30 Ekim 2026): olmayan kırpılma.** Aynı çalışmada miksin tepesini ölçerken yazar stereo dosyayı ffmpeg'in `-ac 1` bayrağıyla tek kanala indirdi. Tepe -0,8 dBFS çıktı ve "miks kırpılıyor" diye yanlış teşhis kondu. Dosyanın gerçek true peak değeri -3,1 dBTP'ydi. ffmpeg iki kanalı yaklaşık 0,707 katsayıyla toplar, iki kanalda aynı sinyal varsa sonuç +3 dB olur. Ölçümü kanalları ayrı okuyarak ya da `pan=mono|c0=0.5*c0+0.5*c1` ile yap.

**Kurgu senaryo: kendi kuralıyla ölçen kontrol.** Tuna, bir tanıtım videosu için okuma süresi kontrolü yazdırır. Claude kontrolü proje dosyasındaki bekleme değeriyle ölçer. Tuna videoyu sıkıştırmak için o değeri düşürür ve kontrol yine geçer, çünkü ölçülen şey ölçütü de gevşetmiştir. Kitin kodunda bu tuzak not edilmiş: okuma kontrolü projenin kuralıyla değil kitin sabit kuralıyla ölçer.

## Alıştırma: on beş saniyelik videoyu planla ölç

Herhangi bir araçla yap: Remotion, Canvas ya da bir HTML sayfası. Önemli olan yöntem.

1. Üç cümlelik bir metinle kısa bir video başlat. Zamanlamayı tek bir dosyada tut, ör. her sahne için giriş ve oturma anı, her olay için ad. Sahne kodunda hiçbir yere saniye yazma.
2. Render'dan önce çalışan bir ölçüm yaz. En kolayı okuma süresi: her cümle ekranda kelime başına en az çeyrek saniye kalsın. Ölçüm hata verirse çıkış kodu sıfırdan farklı olsun.
3. Ölçümü bozup düştüğünü gör. Plan dosyasında bir cümlenin süresini yarıya indir ve ölçümün KALDI dediğini kaydet. Sonra düzelt ve GEÇTİ dediğini kaydet.
4. Her sahne ve olay için bir kare üret ve hepsini tek bir PNG'ye diz. Her karenin altına zaman etiketi, üstüne güvenli alanları koy.
5. Kare tablosuna bak ve bir sorun bul. Bulamazsan neye baktığını yaz: odak, çakışma, okunurluk.
6. Videoyu al, son dosyada süreyi ve varsa ses seviyesini ölç.

**Bitti sayılması için:** plan dosyası, düşen ve geçen ölçüm çıktısı (aynı ölçümün ikisi birden), tek PNG kare tablosu ve son video. Plan dosyasında hiçbir sahne kodunda saniye değeri geçmediğini bir `grep` çıktısıyla göster.

## Bağlantılar

Kontrol listesi: [12.1](../README.md#12-dogrulama) [12.2](../README.md#12-dogrulama) [12.5](../README.md#12-dogrulama) [16.1](../README.md#16-tasarim) [16.2](../README.md#16-tasarim) [16.3](../README.md#16-tasarim) [16.4](../README.md#16-tasarim) [16.5](../README.md#16-tasarim). Önceki bölümler: [Bölüm 4: Kanıtla teslim: iddiayı sayıya çevir](04-kanitla-teslim.md), [Bölüm 15: Arayüz tasarımı: Claude Design ve tahtalar](15-claude-design.md). Ekler: [İpuçları ve püf noktaları](../ekler/ipuclari.md), [Gerçek deneyimlerden on ders](../ekler/deneyimler.md).

Kontrol listesindeki karşılıkları: [16.7](../README.md#16-tasarim) [16.8](../README.md#16-tasarim) [16.9](../README.md#16-tasarim).

---

[← Bölüm 15](15-claude-design.md) · [İçindekiler](README.md)

## Zihinsel model: kanıt, iddianın yerini tutmaz

Claude Code bir işi bitirdiğinde "tamamlandı, testler geçiyor" diyebilir. Bu cümle bir kanıt değil, bir iddiadır. {{bolum:1}} bölümündeki döngünün son evresi doğrulamadır ve belge açık söyler: yazdığı kodun çalıştığını gösterebilecek bir kanıt vermezsen tek doğrulayıcı sen kalırsın. Gözetmediğin bir oturumda ise elindeki tek kanıt budur.

Bu bölümün tek ilkesi şu: teslim almadan önce "geçti" sözcüğünü bir sayıya, bir çıktıya ya da bir görüntüye çevir. Çevirebildiğin şey kanıttır. Çeviremediğin şey Claude'un anlatısıdır ve anlatı çoğu zaman doğrudur ama doğru olmadığı gün pahalıdır.

## "Geçti" yerine sayı

Test aracı "başarılı" der. Bu tek sözcük iki çok farklı durumu örter: 200 test koştu ve geçti, ya da sıfır test koştu ve hiçbir şey bulmadığı için geçti. İkincisi yeşildir ama hiçbir şey ölçmemiştir. Bu yüzden her sonuçta durum satırının yanındaki sayıyı oku: kaç test koştu, kaç dosya tarandı, kaç satır değişti. Beklediğin sayıyla eşleşmiyorsa yeşil bir şey söylemiyor. [[12.1]]

## Sıfır test koşan filtre

Test araçları tek bir testi çalıştırmak için bir filtre kabul eder. Filtre hiçbir testle eşleşmezse bazı araçlar hata vermez ve boş koşuyu başarılı sayar. Süitin okunur adını verirsen eşleşme olmayabilir. Tip ya da fonksiyon adıyla filtrelersen eşleşir ve çıktıda sayı sıfırın üstüne çıkar. Sözdizimi araca göre değişir, ilke değişmez: filtreli koşunun sonunda test sayısı sıfırdan büyük olmalı.

**Gerçek vaka D02.** Test komutuna süitin okunur adı filtre olarak verildi, eşleşen test olmadı ve çıktı "başarılı" dedi. Rapora "test geçiyor" diye girmek üzereydi. Aynı gün iki benzer yeşil daha çıktı: hiçbir dosya bulamadığı için geçen bir lint ve penceresi dar olduğu için körleşen bir lint (lint, kod stilini ve basit hataları denetleyen araçtır). Üçünün ortak yanı, durum satırının doğru, kapsamın boş olmasıdır. Ayrıntısı {{ek:deneyimler}} sayfasında D02. [[12.1]]

Aynı durum küçük bir deneme klasöründe, filtre hiçbir testle eşleşmeyecek şekilde verilerek denendi:

```terminal Gerçek çıktı, kısaltılmış
$ python3 -m unittest -k yok_boyle_test -v test_toplam
----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN
$ echo $?
5
```

- **`Ran 0 tests` satırı:** Asıl bilgi bu sayı. Kapsam boş.
- **`NO TESTS RAN` ve çıkış kodu 5:** Python'un `unittest` aracı boş koşuyu açıkça işaretliyor ve sıfırdan farklı kodla çıkıyor. Her araç bu kadar açık davranmaz, bu yüzden sayıyı kendin okumak zorundasın.

## Yeni kontrolü hatayı geri koyarak sınamak

Claude yeni bir test, lint kuralı ya da doğrulama betiği yazdıysa onun çalıştığını göstermek için bir tek yol var: kontrolün yakalaması gereken hatayı kasten geri koy ve kontrolün düştüğünü gör. Düşmüyorsa kontrol hiçbir şeye bakmıyor demektir. Sonra hatayı çıkar ve kontrolün yeşile döndüğünü gör. Bu üç adımlık döngü (yeşil, kasten kır, kırmızı, düzelt, yeşil) bir kontrolün gerçekten çalıştığının tek kanıtıdır. [[12.2]]

{{sekil:b04-kasten-kir|Kontrolü sınama döngüsü. Üçüncü adımda kırmızı görmezsen kontrol hiçbir şeye bakmıyor demektir.}}

Aynı döngü, bir `+` işaretinin `-` yapıldığı küçük bir fonksiyonla:

```terminal Gerçek çıktı, kısaltılmış
$ python3 -m unittest -v test_toplam
test_iki_sayi (test_toplam.ToplamTesti.test_iki_sayi) ... ok
Ran 1 test in 0.000s
OK

$ sed -i '' 's/a + b/a - b/' toplam.py
$ python3 -m unittest test_toplam
FAIL: test_iki_sayi (test_toplam.ToplamTesti.test_iki_sayi)
AssertionError: -1 != 5
Ran 1 test in 0.001s
FAILED (failures=1)

$ sed -i '' 's/a - b/a + b/' toplam.py
$ python3 -m unittest -v test_toplam
test_iki_sayi (test_toplam.ToplamTesti.test_iki_sayi) ... ok
Ran 1 test in 0.000s
OK
```

- **İlk `OK` ve `Ran 1 test`:** Kontrol yeşil ve sayı 1. Başlangıç noktası bu.
- **`sed` satırı ve `FAILED (failures=1)`:** Hata kasten konuldu ve test düştü. `AssertionError: -1 != 5` satırı testin tam olarak neye baktığını da söylüyor: iki sayının toplamına.
- **Son `OK`:** Hata geri alındı, sayı yine 1 ve koşu yeşil. Üç koşu birlikte kontrolün işe yaradığını gösterir.

**Gerçek vaka D08 (yan örnek).** Ağır komutları reddeden bir hook (araç çalışmadan önce devreye giren betik, ayrıntısı {{bolum:8}}) 16 vakalık bir testle sınandı ve sıfır yanlış verdi. Test gerçekten bakıyor mu diye hafif komut istisnası kasten bozuldu ve test iki yanlış verdi. Düşen test, testin işe yaradığını gösterdi. Ayrıntısı D08.

## Görsel değişikliği önce/sonra görmek

Bir arayüz, bir slayt ya da bir grafik değiştiyse metin raporu yetmez. Claude "düğmeyi hizaladım" diyebilir ve düğme hâlâ kaymış olabilir. Değişiklikten önce bir ekran görüntüsü al, sonra bir tane daha al ve yan yana bak. Belge `/verify` komutunu önerir: Claude uygulamayı derler, çalıştırır ve sonuca bakar, testlerin ve tip kontrolünün kaçırdığı sorunları yakalar. Görüntü yoksa "ne değişmiş ki" sorusunun cevabı da yoktur. [[12.5]]

## Alt ajan raporunu kanıtla eşleştirmek

Alt ajan kendi penceresinde çalışır ve ana oturuma bir özet döner. Özet, ajanın yaptığı şeyin anlatısıdır. "Dört dosyayı güncelledim ve testler geçti" cümlesini üç şeyle eşleştir: `git diff --stat` gerçekten dört dosya mı gösteriyor, test çıktısında sayı var mı, alt ajanın dokunduğunu söylediği her dosyada değişiklik görünüyor mu? Eşleşmeyen her parça bir soru işaretidir. Bunu kendin yapamıyorsan ayrı bir doğrulayıcı ajana "bu rapordaki her iddiayı kanıtla kontrol et" diye ver, ama yine ondan da çıktı iste. [[12.3]]

**Gerçek vaka D10.** Yapıştırılan bir denetim notundaki "uygulama yalnız bir ülkede satışta" cümlesi kaynağında kontrol edilmedi ({{bolum:1}}). Aynı oturumda bir sürüm notundaki "hepsinin görseli var" iddiası da 11 eksik görselle çürüdü. Rapor ne kadar özenli yazılmış olursa olsun, değişebilen bir durumu kaynağında kontrol etmeden aktarma. Ayrıntısı D10. [[12.3]]

## Bağımsız inceleme ve üç satır

Kendi yazdığın işi kendin incelemek zayıf bir kontroldür, çünkü aynı varsayımlarla bakarsın. Önemli bir değişikliği teslimden önce `/code-review` ile geçir. Komut güncel dalı ya da bir PR'ı, dalı veya yolu inceler. `--fix` bayrağı bulguları çalışma ağacına uygulatır, `--comment` ise GitHub'da satır içi yorum bırakır. Belgenin bir uyarısı da var: kendi yazdığın inceleme prompt'unda "stili atla" kısmını silme, yoksa inceleyici her zaman bir şey bulur ve bulgu listesi gürültüyle dolar. [[12.6]]

İş bitince ayrıca Claude'dan üç satır iste: neyi kaçırmış olabilir, hangi iddiası en zayıf, hangi kararı gerekçesiz. Bu satırlar övgüyü değil kırma denemesini tetikler. [[12.4]]

## Commit kapsamı ve teslim aşamaları

Bir commit tek bir mantıklı parça olsun. Kaynak kodu Git'te dursun ve commit'e neyin gireceğini sen tanımla. Başka bir oturum ya da başka bir iş aynı depoya yazıyorsa stage ve commit'i tek komutta yap. **Gerçek vaka D06:** değişiklikler stage edildi, üç dakikalık bir derleme sürerken başka bir oturum kendi raporunu commit'ledi ve commit index'in tamamını aldı. Dört dosya yanlış bir mesajın altına girdi. Kanıt `git log --stat` çıktısındaydı. [[15.1]]

Teslimin üç ayrı aşaması var ve her birini kendi kanıtıyla adlandır:

| Aşama | Anlamı | Kanıt |
|---|---|---|
| Yerel | Değişiklik bu makinede çalışıyor | Test sayısı, çıktı, görüntü |
| Push | Değişiklik uzak depoda | Dal adı, commit kimliği, CI (her push'ta testleri otomatik koşturan sistem) sonucu |
| Yayın | Kullanıcı artık görüyor | Yayındaki sürümün kendisine bakılmış olması |

"Bitti" demek bu üçünden hangisini kastettiğini söylemeden anlamsızdır. Push ve deploy yetkisini hedefe ve kapsama bağla: bir dala push izni vermek başka bir dala ya da yayına izin vermek demek değildir. [[12.7]] [[15.3]]

## Karar kuralları

- **"Geçti" gördüğünde sayıyı ara.** Sayı yoksa ya da sıfırsa kontrol boştur.
- **Yeni kontrolü kasten kırarak sına.** Düşmeyen kontrolü bitmiş sayma.
- **Görsel işte iki görüntü iste.** Önce, sonra, yan yana.
- **Alt ajan raporunu diff ve çıktıyla eşleştir.** Eşleşmeyen parçayı geri sor.
- **Önemli değişikliği ayrı bir gözle incele.** `/code-review`, gerekirse `--fix`.
- **Teslim aşamasını adlandır.** Yerel, push ya da yayın. Her birinin kendi kanıtı var.

## Hata biçimleri

**Kurgu senaryo: yeşil ama boş.** Ayşe, Claude'a bir hata düzelttirir ve yeni bir test yazdırır. Claude "yeni test geçiyor" der. Ayşe testi çalıştırır, yeşil görür, commit'ler. Haftalar sonra aynı hata geri gelir. Test dosyasının adı yanlış desenle başladığı için hiç keşfedilmemiş, hiç koşmamıştır. Hatayı geri koyup testin düştüğünü görmüş olsaydı sorun o gün çıkardı.

**Kurgu senaryo: raporun fazlası.** Emre bir alt ajana "tüm modülleri güncelle" der. Rapor altı modülü sayar. `git diff --stat` dördünü gösterir. İki modül hiç değişmemiştir ve rapor iki satırı niyetle değil beklentiyle yazmıştır.

```terminal Kurgu, şematik
# alt ajanın raporu
güncellenen modüller: auth, siparis, kdv, fatura, stok, rapor (6)

$ git diff --stat
 auth.py    | 14 ++++++++------
 siparis.py |  9 +++++----
 kdv.py     |  7 ++++---
 fatura.py  | 11 +++++------
 4 files changed, 22 insertions(+), 19 deletions(-)
```

Rapor altı modül sayıyor, `git diff --stat` dört dosya gösteriyor. Raporda adı geçip diff'te olmayan iki ad `stok` ve `rapor`. Bu iki isim ajana geri sorulacak soru listesidir.

## Alıştırma: kasten bozulan testin gerçekten düştüğünü göster

Bunu bir deneme deposunda ya da kendi çalışma dalında yap, işin sonunda değişiklikleri geri al.

1. Küçük bir fonksiyon seç ve Claude'dan onun için bir test yazmasını iste.
2. Testi kendi başına koştur. Durum satırının yanındaki test sayısını yaz. Sayı 1 ya da üstü olmalı, sıfırsa filtreni düzelt.
3. Fonksiyonun içine kasten bir hata koy, ör. bir `+` işaretini `-` yap. Testi yeniden koştur ve kırmızı olduğunu gör.
4. Test kırmızı olmadıysa testin yanlış şeye baktığını biliyorsun. Claude'a testin neden yakalamadığını sor ve testi düzelt.
5. Hatayı geri al, testi yeniden koştur ve yeşile döndüğünü gör. Bir sorun çıktıysa hepsini `git restore .` ile temizle.

**Bitti sayılması için:** üç çıktı: yeşil koşu (test sayısıyla), kasten bozulmuş koşu (kırmızı) ve düzeltilmiş koşu (yeşil), her birinin yanında test sayısı. Bir cümle: bu test gerçekten neye bakıyor.

## Bağlantılar

Kontrol listesi: [[12.1]] [[12.2]] [[12.3]] [[12.4]] [[12.5]] [[12.6]] [[12.7]] [[15.1]] [[15.3]]. Önceki bölüm: {{bolum:3}}. Ekler: {{ek:deneyimler}}, {{ek:komutlar}}.

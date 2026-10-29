# Rehberin tek kaynağı. Bölüm metni Markdown alt kümesiyle yazılır (yap.py EKLER bölümü).
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

B01 = r"""
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
"""

B05 = r"""
## Zihinsel model: rica ile garanti

Claude Code'a bir kuralı iki türlü verebilirsin. Ya Claude'a söylersin, ya da Claude Code'a uygulatırsın. Belge bu ikisini ayrı adlarla anar. Birinde **Claude karar verir**: prompt, CLAUDE.md, kural dosyası ve Claude'un kendi seçtiği skill'ler. Ötekinde **Claude Code uygular**: hook, deny kuralı ve yönetilen ayar. İlki çoğu zaman tutar. İkincisi her zaman tutar.

Bu ayrım CLAUDE.md'nin nasıl iletildiğinden gelir. CLAUDE.md sistem prompt'unun parçası değildir. Sistem prompt'undan sonra bir kullanıcı mesajı olarak modele verilir. Belge bunu açıkça yazar: Claude bu dosyaları bağlam olarak görür, zorlanan yapılandırma olarak değil, ve sıkı uyumun garantisi yoktur. Hook ise modelin kararına hiç girmez. Olayı gelince çalışır, Claude ne düşünürse düşünsün.

| Katman | Kim karar verir | Ne zaman yüklenir | Ne için |
|---|---|---|---|
| CLAUDE.md | Claude | Her oturumda | Her konuşmada geçerli bağlam: komutlar, tuzaklar, tercihler |
| `.claude/rules/` | Claude | Eşleşen dosyaya dokununca | Yalnız belli dosyalarda geçerli kural |
| Skill | Claude seçer, sen `/ad` ile zorlayabilirsin | Açıklama her zaman, gövde çağrılınca | Tekrarlanan prosedür |
| Alt ajan | Claude | Çağrılınca, kendi penceresinde | Yalıtılmış iş, sonuç özet döner |
| Hook (`command`, `http`) | Claude Code | Olayı gelince | Her seferinde olması gereken şey |
| Deny kuralı, yönetilen ayar | Claude Code | Her araç çağrısından önce | Hiçbir zaman olmaması gereken şey |
| Sandbox | İşletim sistemi | Her kabuk komutunda | Komut adından fazlasını yapsa bile tutan sınır |

Belgenin hook ile skill karşılaştırmasındaki iki cümle bütün bölümü özetler: skill "bir rica, garanti değil". Korkulukları hook'a koy.

## Karar kuralları

**İstisnası olmayan şey kesin katmana gider.** Belge bunu tek cümleyle söyler: bir şey her seferinde olmak zorundaysa onu hook, deny kuralı ya da yönetilen ayar yap. `.env` okunmayacaksa bu bir CLAUDE.md satırı değil, deny kuralıdır. Commit'ten önce testler koşacaksa bu bir hook'tur. [[7.1]] [[7.6]]

**Geri kalan her şeyi Claude'a bırak.** Belge burada da açık: çoğu zaman Claude'un karar vermesini istersin. Kırk hook'a ulaştıysan çoğu kural değil tercihtir. Kesin katman bakım ister, her hook test ister ve yanlış yazılmış bir hook işi tamamen durdurur. [[8.4]]

**Vurguyla uyum satın alınmaz.** Bir kural çiğneniyorsa başına IMPORTANT eklemek belgenin deyişiyle büyük olasılıkla düzeltmez. Eski modeller vurguya ihtiyaç duyuyordu. Güncel modeller düz yazılmış bir satırı izler, vurgu yığmak kuralı fazla uygulatır. Vurgu eklemeye devam ediyorsan o satır hook'a aittir. [[1.1]]

**CLAUDE.md'yi kısa tut.** Belge dosya başına 200 satırın altını hedefler. Uzun dosya hem bağlam harcar hem uyumu düşürür. Çelişen iki talimattan Claude birini rastgele seçebilir. Uzun prosedür skill'e, belli dosyalara özgü kural `.claude/rules/` altına gider. [[1.2]] [[1.4]]

**Yol kuralının bir bedeli var.** `paths` deseniyle yüklenen kural konuşma geçmişine girer. Sıkıştırmada özetlenip kaybolabilir, ancak eşleşen dosyaya yeniden dokununca geri gelir. Oturum boyunca kesin geçerli olması gerekiyorsa `paths` alanını kaldır ya da kökteki CLAUDE.md'ye taşı.

**Skill'in açıklaması tetiğidir.** Claude işini skill açıklamalarıyla karşılaştırıp hangisinin ilgili olduğuna kendisi karar verir. Açıklama belirsizse ya da başka bir skill'le örtüşüyorsa yanlış skill yüklenir ya da hiç yüklenmez. Mutlaka çalışması gerekiyorsa `/ad` ile kendin çağır. Yan etkili bir skill'i otomatik çağrıya `disable-model-invocation: true` ile kapat. [[9.3]] [[9.4]]

**Her hook kesin değildir.** `command` ve `http` tipindeki hook kesindir. `prompt` ve `agent` tipindeki hook kararı başka bir modele bırakır, belgeye göre bunlar da kesin değildir. Hook'un kendisi çökerse eylemi de durdurmak istiyorsan hata politikasını buna göre seç. [[8.5]]

**Deny kuralı bir güvenlik sınırı değildir.** Bash kuralları komutun metnini eşler, niyetini değil. `Bash(rm *)` kuralı `/bin/rm` ya da `bash -c 'rm ...'` biçimini durdurmaz. Bir dosyaya okuma yasağı `cat .env`'i yakalar ama dosyayı açan bir betiği yakalamaz. Gerçek sınır işletim sistemi düzeyindeki sandbox'tır. O da yalnız kabuk komutlarını sarar. Dosya okuma ve düzenleme araçları, web araçları ve hook'lar sandbox dışında çalışır, onları izin kuralları yönetir. Belge ikisini birlikte kullanmayı önerir. [[6.2]] [[7.5]]

## Bir kuralın yerini bulmak

Belgenin önerdiği tetikler kısa bir karar listesi verir:

| Gözlem | Yeri |
|---|---|
| Claude aynı şeyi iki kez yanlış yaptı | CLAUDE.md |
| Aynı uzun prompt'u tekrar tekrar yazıyorsun | Skill |
| Bir yan iş konuşmayı çıktıyla boğuyor | Alt ajan |
| Bir şeyin sormadan her seferinde olması gerekiyor | Hook |
| Bir şeyin hiçbir zaman olmaması gerekiyor | Deny kuralı, gerekirse sandbox |
| Aynı kurulum ikinci bir depoda da lazım | Plugin |

## Hata biçimleri

**Gerçek vaka: metin kuralı yeni oturuma ulaşmadı.** Dört paralel oturum aynı anda derleme koştu, makinenin yükü 720'ye çıktı. Oturumlara "ağır komutu kilitle sar" diye talimat verildi. Bir oturum kilitsiz bir derleme başlattı ve sonradan durdurmak zorunda kaldı. Metin kuralı o anki oturumlara ulaştı, yenilerine ve başka projelere ulaşmadı. Çalışan çözüm kesin katmandaydı: ağır komutları kilitle koşturan bir sarmalayıcı ve sırasız ağır komutu reddeden bir PreToolUse hook'u. Hook 16 vakalık bir testle sınandı. Ayrıntısı {{ek:deneyimler}} sayfasında D08.

**Gerçek vaka: kesin sandığın katman hiç yüklenmedi.** Proje dışı bir dosyayı import eden CLAUDE.md, headless koşumda içeriği yüklemedi. Çözüm aynı bilgiyi her oturumda bağlama koyan bir SessionStart hook'u oldu. Burada hook kuralı uygulatmadı, yalnız bağlama girmesini garanti etti. Kuralın kendisi yine Claude'un kararındaydı. Ayrıntısı D07.

**Kurgu senaryo: çoğu zaman tutan kural.** Mert'in ekibi CLAUDE.md'ye "commit'ten önce tip kontrolünü çalıştır" yazar. Haftalarca sorun çıkmaz. Bir gün uzun bir oturumun sonunda Claude tip kontrolünü atlayıp commit atar, kırık kod ana dala girer. Belge tam bu satırı örnek verir: çoğu zaman çalışır, her zaman değil. Ekip kuralı bir hook'a taşır. Artık tip kontrolü geçmeyen commit hiç oluşmaz.

## Alıştırma: aynı kuralı üç katmanda dene

Bunu gerçek bir iş deposunda değil, bu iş için açtığın bir deneme deposunda yap.

1. Depoya içinde sahte bir değer olan bir `.env` dosyası koy, ör. `DENEME_ANAHTARI=12345`.
2. **Rica katmanı.** CLAUDE.md'ye "`.env` dosyasını okuma" yaz. Yeni oturumda Claude'dan `.env` içindeki değeri söylemesini iste. Ne olduğunu kaydet.
3. **Kesin katman.** CLAUDE.md satırını sil. `.claude/settings.json` içine `Read(./.env)` için deny kuralı ekle. Yeni oturumda aynı isteği yap. Sonra Claude'dan değeri `cat .env` ile okumasını iste. İkisinin sonucunu kaydet.
4. **Kuralın sınırı.** Claude'dan `.env` dosyasını okuyup değeri yazdıran küçük bir betik yazmasını ve çalıştırmasını iste. Deny kuralı bunu durdurdu mu?
5. Platformun destekliyorsa `/sandbox` ile sandbox'ı aç ve 4. adımı tekrarla.

**Bitti sayılması için:** dört satırlık bir tablo. Her satırda katman, deneme ve sonuç olsun. Altına bir cümle yaz: bu depoda `.env`'i gerçekten koruyan katman hangisi. Sonra deneme deposunu sil.

## Bağlantılar

Kontrol listesi: [[1.1]] [[1.2]] [[1.4]] [[6.2]] [[7.1]] [[7.5]] [[7.6]] [[8.4]] [[8.5]] [[9.3]] [[9.4]]. Önceki bölüm: {{bolum:1}}. Ekler: {{ek:ipuclari}}, {{ek:dosyalar}}.
"""

REHBER = [
 dict(no=1, ad="01-zihinsel-model", seviye="temel", baslik="Zihinsel model: döngü, bağlam ve harness",
      ozet="Claude Code'la yaşanan her sürprizin açıklaması üç parçadan birindedir: model, araç ya da harness. Bağlam penceresi modelin gördüğü tek şeydir.", md=B01),
 dict(no=5, ad="05-talimat-mimarisi", seviye="orta", baslik="Talimat mimarisi: rica ile garanti",
      ozet="Bir kural ya Claude'a söylenir ya da Claude Code'a uygulatılır. Hangisinin nereye gideceğini bilmek, kuralın tutup tutmayacağını belirler.", md=B05),
]

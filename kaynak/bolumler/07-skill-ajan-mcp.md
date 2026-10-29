## Zihinsel model: aynı işi üçüncü kez anlatma

Bir işi üçüncü kez aynı cümlelerle anlatıyorsan o tarif bir dosyaya aittir. Claude Code bu dosya için dört kap sunar ve her kap farklı bir sorunu çözer. Sorunu yanlış kaba koyarsan ya bağlamını şişirirsin ya da hiç tetiklenmeyen bir şey yazarsın.

| Kap | Çözdüğü sorun | Nerede çalışır |
|---|---|---|
| Skill | Tekrar eden tarif ya da başvuru bilgisi | Ana konuşmada, bağlama eklenir |
| Alt ajan | Konuşmayı boğan yan iş, bağımsız göz | Kendi bağlam penceresinde, sana özet döner |
| MCP | Claude'un göremediği bir dış sistem | Dış sunucuda, Claude'a araç olarak görünür |
| Plugin | Aynı kurulum başka depoda ya da başka kişide lazım | Paketleme katmanı, içindekileri birlikte taşır |

Belgenin "Extend Claude Code" sayfası seçimi tetiklere bağlar. Tetikler kısa:

| Gözlem | Eklenecek şey |
|---|---|
| Aynı başlangıç prompt'unu tekrar tekrar yazıyorsun | Skill (sen `/ad` ile çağırırsın) |
| Aynı çok adımlı tarifi üçüncü kez sohbete yapıştırıyorsun | Skill |
| Bir tarayıcı sekmesinden ya da bir sistemden sürekli veri kopyalıyorsun | MCP |
| Yan iş konuşmayı çıktıyla dolduruyor | Alt ajan |
| Bir şeyin sormadan her seferinde olması gerekiyor | Hook ({{bolum:8}}) |
| İkinci bir depo aynı kuruluma ihtiyaç duyuyor | Plugin |

Skill ile alt ajan arasındaki fark bağlama bakarak anlaşılır. Skill konuşma penceresine eklenir. Alt ajan kendi penceresinde çalışır ve yalnız özet döndürür. İkisi birleşebilir: bir alt ajan skill'leri önceden yükleyebilir, bir skill de `context: fork` ile kendi alt ajan bağlamında koşabilir. {{bolum:5}} rica ile garanti ayrımını anlattı. Bu bölüm kapların kendisini anlatıyor.

## Skill: açıklama bir tetiktir

Skill dosyasının başındaki `description`, Claude'un skill'i ne zaman yükleyeceğine karar verdiği tek şeydir. Gövde ancak çağrılınca yüklenir. Belge ayrıntıyı şöyle koyar: açıklama ve `when_to_use` metni listede toplam 1.536 karakterde kesilir, bu yüzden ana kullanım durumunu başa yaz.

İyi bir açıklama üç şey taşır.

- **Ne yaptığı:** "Son etiketten bu yana değişikliklerden sürüm notu yazar."
- **Kullanıcının söyleyeceği ifadeler:** "Sürüm notu", "release notes" denince kullan.
- **Ne zaman kullanılmayacağı:** "Teknik changelog için kullanma." Bu cümle komşu işlerde yanlış yüklenmeyi keser. [[9.3]]

Belge sorun giderme bölümünde iki yönü de ayrı ayrı ele alır. Skill tetiklenmiyorsa açıklamaya kullanıcının doğal olarak söyleyeceği sözcükleri koy ve `/ad` ile doğrudan çağır. Çok sık tetikleniyorsa açıklamayı daralt. Frontmatter YAML'ı bozuksa skill gövdesi boş metadata ile yüklenir: `/ad` çalışır ama Claude açıklamayı eşleştiremez. Bu yüzden "elle çağırınca çalışıyor" tek başına tetik kanıtı değildir.

### Yan etkili skill'i kapat

Mesaj gönderen, deploy eden ya da dosya silen bir skill'in modelin kararıyla çalışmasını istemezsin. Frontmatter'a `disable-model-invocation: true` yaz. Belgeye göre bu durumda skill'in açıklaması bağlama hiç girmez, Claude kendiliğinden çalıştıramaz ve denerse Claude Code çağrıyı reddeder. Ama skill'i sen `/ad` ile çalıştırabilirsin. Bu alan araç izinlerinin ya da senin yetkinin yerini tutmaz, yalnız kimin tetikleyebileceğini belirler. [[9.4]]

Skill'in `allowed-tools` alanı da benzer bir karışıklık yaratır. Bu alan skill çalıştığı tur boyunca listedeki araçlara sormadan izin verir, kısıtlamaz. Bir skill'e araç kısıtı koymak istiyorsan deny kuralı ya da alt ajanın `tools` alanı gerekir.

Son bir tuzak: skill çağrıldığında içeriği konuşmaya girer ve orada kalır. Dosya sonraki turlarda yeniden okunmaz. Sıkıştırmadan sonra her skill'in yalnız başı geri eklenir (ilk 5.000 token) ve çok skill çağırdıysan eskileri tamamen düşebilir. Önemli kuralı skill dosyasının başına koy. Bir kural her seferinde geçerli olmak zorundaysa belgenin önerisi hook'tur.

## Alt ajan: ayrı bağlam, ayrı model

Alt ajan kendi bağlam penceresinde, kendi sistem prompt'u ve kendi araç listesiyle çalışır. Konuşmanı görmez, ona görevi bir devir mesajı anlatır. Üç karar vereceksin.

**Ne zaman alt ajan?** Belgenin ölçütü: görev çok çıktı üretiyor ama o çıktıya sonra ihtiyacın yok, ya da araç kısıtı koymak istiyorsun, ya da iş kendi içinde bütün ve özetle dönebilir. Sık gidip gelen, aşamaları ortak bağlama dayanan ya da küçük bir değişiklik olan işte ana konuşma daha iyidir, çünkü alt ajan sıfırdan başlar ve bağlam toplamak zaman alır.

**Hangi model?** Alt ajanın `model` alanı `sonnet`, `opus`, `haiku`, `fable`, tam bir model kimliği ya da `inherit` alabilir. Belge çözümleme sırasını verir: çağrı başına verilen `model` parametresi, sonra tanımdaki `model`, sonra `CLAUDE_CODE_SUBAGENT_MODEL` ortam değişkeni, en son ana konuşmanın modeli. Hata maliyeti düşük bir arama işini küçük modele vermek tasarruf sağlar. Hata maliyeti yüksek bir doğrulamayı küçük modele vermek ise bedelini sonradan ödetir. Aynı temsilî işte kalite, süre ve kullanımı karşılaştırmadan karar verme. [[5.1]]

**Eleştiri kimde?** Yazan bağlam kendi hatasına kör kalır, çünkü varsayımlarını kendisi koymuştur. Eleştiriyi ayrı bir alt ajana ver. İncelemeyi statik tutmak istiyorsan ajanın `tools` alanına yalnız `Read, Grep, Glob` yaz. `Bash` eklediğin ajan salt okunur sayılmaz, çünkü komut çalıştırabilir. Ayrı bağlam bağımsızlığı artırır, doğruluğu garanti etmez. Ajanın cevabı bulgu sayısı değil, dosya ve kanıt taşımalı. Bulgu yoksa neye baktığını ve neyi çalıştırmadığını yazmalı. [[9.1]]

Alt ajan açıklamaları da bağlama girer. Belge, özel ajanların açıklamalarının toplamı 15.000 token'ı aşınca başlangıçta uyarı verir. Açıklamayı kısa tut, ayrıntıyı ajanın sistem prompt'una koy.

## MCP: bağlı görünmek çalışmak demek değildir

MCP, Claude'u dış bir sisteme araç olarak bağlar. Bir uygulamaya erişeceksen önce o uygulamanın MCP'sini dene, çünkü API üzerinden giden çağrı ekranda tıklamaktan hızlı ve kesindir. Sıra: uygulamanın MCP'si, sonra tarayıcı, en son bilgisayar kontrolü. [[9.5]]

Bağlantıyı iki yerde sına.

1. `/mcp` ile sunucu durumuna bak. `claude mcp list` komutu `Connected`, `Needs authentication` ya da `Failed to connect` gösterir. Bu yalnız bağlantıyı söyler.
2. Zararsız gerçek bir okuma işlemi yaptır: bir kaydı listele, bir kaydı oku. İşlem doğru hesapta ve doğru hedefte sonuç veriyorsa bağlantı çalışıyordur. Yazma işlemini ayrıca, kendi yetki kapsamınla eşleştirerek dene.

**Kapsamı dar tut.** Belge MCP sunucusunu üç kapsamda tanımlar: yerel (yalnız bu proje, yalnız sen), proje (`.mcp.json`, depoyla paylaşılır) ve kullanıcı (bütün projelerin, yalnız senin). Kişisel ve kimlik bilgisi taşıyan sunucuyu yerel kapsamda tut. Ekiple paylaşılan sunucuyu proje kapsamına koy ama içeriğini kod gibi gözden geçir. Çalışan bir bağlantı doğru hesap ve en az yetki demek değildir. Okuma ve yazma yetkisini ayır, kullanmadığın bağlantıyı kaldır. [[9.7]]

Proje kapsamlı sunucular için güvenlik tarafı: etkileşimli oturum onay ister. `claude -p` onay penceresini gösteremediği için `.mcp.json` sunucularını sormadan yükler. Başkasının deposunda `-p` koşmadan önce {{bolum:6}} bölümündeki önlemleri uygula.

## Plugin: paketle, ama gerektiğinde

Plugin skill, ajan, hook ve MCP sunucusunu tek kurulum birimi yapar. Manifest `.claude-plugin/plugin.json` içindedir. Plugin skill'leri `/plugin-adi:skill` biçiminde ad alanı kazanır, böylece çakışmaz. Belgenin söylediği önemli bir ayrıntı: etkin plugin her oturumun parçasıdır, kullanmasan da bağlamına ve kullanımına yük bindirir. Tek bir depoda ve tek kişilik iş için dosyaları `.claude/skills/` altında tutmak yeter. İkinci bir depo ya da ekip arkadaşı gerektirince paketle. [[9.6]] [[10.3]]

Temiz bir makinede kurulumdan sonra skill'in listede göründüğünü doğrula. Ekip için tek kişinin ürettiği çıktıyla başkasının ürettiğini karşılaştır, biçim aynı olmalı.

## Karar kuralları

- **Tarifi üçüncü kez yazıyorsan skill yap.** İkinci kez yazıyorsan yalnız not al.
- **Açıklamayı kullanıcının söyleyeceği sözcüklerle ve "kullanma" cümlesiyle yaz.**
- **Yan etkisi olan her skill'e `disable-model-invocation: true` koy.**
- **Çok çıktı üreten yan işi alt ajana, eleştiriyi yazandan ayrı bağlama ver.**
- **Alt ajana `Bash` verdiysen salt okunur saymayı bırak.**
- **MCP için `Connected` yeterli değil. Gerçek bir okuma yaptır.**
- **Paketlemeyi ikinci kullanıcı gelince yap, öncesinde değil.**

## Hata biçimleri

**Kurgu senaryo: tek örnekle sınanan skill.** Zeynep `surum-notu` skill'ini yazar, bir kez çalıştırır, sonuç güzel çıkar. İki hafta sonra ekip arkadaşı "teknik changelog hazırla" der ve Claude yanlışlıkla bu skill'i yükler. Açıklamada "kullanma" sınırı yoktur. Zeynep bir olumsuz örnek (teknik changelog) ve bir hata örneği (hiç etiket olmayan depo) ekleyip yeniden sınar.

**Kurgu senaryo: bağlı ama yanlış hesap.** Hakan bir proje yönetimi MCP'si ekler, `/mcp` yeşil gösterir. İlk okuma işlemi başka bir çalışma alanının kayıtlarını döndürür, çünkü sunucu kişisel hesapla giriş yapmıştır. Durum ekranı yalnız bağlantıya bakar, hesabı sınamaz.

## Alıştırma: bir skill yaz ve olumlu, olumsuz örnekle sına

Herhangi bir git deposunda yap. Skill'i `.claude/skills/` altına koy.

1. Tekrar eden küçük bir iş seç. Örnek: son etiketten bu yana değişenlerden en fazla beş maddelik kullanıcıya dönük sürüm notu.
2. `.claude/skills/surum-notu/SKILL.md` dosyasını yaz. Açıklamada ne yaptığını, tetikleyici ifadeleri ve "teknik changelog için kullanma" sınırını belirt.
3. Sınama listesini önce yaz, sonra çalıştır. En az altı satır olsun: üç istek tetiklemeli (örn. "sürüm notu yaz", "release notes hazırla", "son sürümde ne değişti, kullanıcıya anlat"), iki istek tetiklememeli (örn. "teknik changelog üret", "bu dosyayı özetle"), bir tanesi hata durumu olmalı (örn. etiketi olmayan depo). Her satıra beklediğin sonucu yaz.
4. Her satırı **yeni bir oturumda** çalıştır. Önceki sohbet kalıntısı eksik yönergeleri maskeler. Hem doğal dille hem `/surum-notu` ile dene. Hangi isteğin skill'i yüklediğini kaydet.
5. Tetiklenmemesi gerekirken tetiklenen ya da tetiklenmesi gerekirken tetiklenmeyen satırlar için açıklamayı düzelt ve listeyi baştan koş. İstersen skill'i `skillOverrides` ile kapatıp aynı istekleri skill'siz çalıştırarak bir karşılaştırma tabanı al.

**Bitti sayılması için:** beklenen ve gerçekleşen sonucun yan yana durduğu altı satırlık bir tablo. Başarısız olan her satır için açıklamada neyi değiştirdiğini yaz. Başarısız vakaları sakla, bir sonraki değişiklikte tekrar koşarsın.

## Bağlantılar

Kontrol listesi: [[9.1]] [[9.2]] [[9.3]] [[9.4]] [[9.5]] [[9.6]] [[9.7]] [[9.8]] [[10.3]] [[5.1]]. Önceki bölümler: {{bolum:5}}, {{bolum:6}}. Sonraki bölüm: {{bolum:8}}. Ekler: {{ek:komutlar}}, {{ek:dosyalar}}.

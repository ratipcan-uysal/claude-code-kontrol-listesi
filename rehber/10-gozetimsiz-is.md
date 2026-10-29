# 10. Gözetimsiz iş: sen yokken çalışan sistem

_Uzman · Belge kontrolü: 29 Ekim 2026_

Gözetimsiz iş, hangi kararın verilebileceğini, neyin işi durduracağını ve bittiğin kanıtını önceden yazmaktır. En pahalı hata işin yapılmaması değil, yapılmadığının fark edilmemesidir.

## Zihinsel model: sen yokken karar veren bir sistem kuruyorsun

Gözetimsiz iş, "Claude'u çalıştırıp uzaklaşmak" değildir. Orada olmadığın sürece her kararı Claude verir, her tıkanıklıkta sana soramaz ve her sessizlik senin için bir sonuç gibi görünür. : **hangi kararı Claude verebilir**, **ne olursa durmalı** ve **bittiğini hangi kanıt gösterir**.

Gözetimsiz işin en pahalı hatası iş yapılmaması değil, yapılmadığının fark edilmemesidir. Sabah baktığında log boşsa ve hiçbir hata yoksa, iki ihtimal var: iş sessizce bitti ya da hiç başlamadı. İkisi dışarıdan aynı görünür. 
## Sen yokken hangi karar verilebilir

"Sormadan ilerle" tek başına yetmez. Hangi kararın serbest, hangisinin yasak olduğunu yazmak gerekir. Pratik ölçü geri alınabilirliktir:

| Karar türü | Gözetimsiz kural |
|---|---|
| Geri alınabilir ve kapsam içinde (dosya düzenleme, yerel commit, deneme) | Claude verir, varsayımı raporda yazar |
| Sonucu değiştiren seçim (hangi kütüphane, hangi veri kaynağı) | En makul varsayımla ilerler, varsayımı işaretler |
| Geri alınamaz ya da dışarıya etkili (push, deploy, silme, ödeme) | Yapmaz, adımı "engelli" işaretler, kalanı bitirir |
| İzin gerektiren adım | En sona bırakılır, gerektirmeyen her şey önce biter |

Bunu işe başlamadan görev dosyasına yaz. Yetki, kapsam, bütçe ve tıkanma davranışı net olsun. Her projeye sınırsız genel yetki yazma. İş tıkandığında "dur ve sor" yerine "o maddeyi atla, kalanı bitir, sonda yaz" de. Sabah ilk gördüğün şey çalışan bir sonuç olmalı, izin ekranı değil. [13.1](../README.md#13-gozetimsiz)

## Headless koşum: claude -p

`claude -p "..."` Claude'u etkileşimsiz çalıştırır. Betikten, zamanlayıcıdan ya da başka bir araçtan çağırabilirsin. Çıktıyı `--output-format json` ile makine okuyacak biçime çevirirsin.

Belge çıkış durumunu şöyle tanımlar: başarıda 0, koşum başarısız olursa sıfırdan farklı bir kod. Ama iş içinde oluşan bir hata, örneğin kimlik doğrulama eksikliği, sonuç olarak stdout'a basılır. Yani çıkış koduna tek başına güvenme. Başarıyı üç yerden birlikte oku: çıkış kodu, JSON'daki `is_error` alanı ve sonuç türü (`subtype`). Belgeye göre bütçe ya da tur sınırı gibi sınırlar dolduğunda koşum hata türüyle biter. Bu sınırların dolması başarı değildir, işin yarım kaldığı anlamına gelir. [14.6](../README.md#14-rutin)

Makinenin okuyacağı sonucu serbest metinden ayıklama. `--json-schema` ile şema ver, sonuç `structured_output` alanında gelir. Claude geçerli çıktı üretemezse (örneğin isteği reddettiyse) alan hiç gelmez. Betik önce alanın varlığına baksın. [14.7](../README.md#14-rutin)

```
claude -p "Bu haftanın hata kayıtlarını özetle" --output-format json \
  --json-schema '{"type":"object","properties":{"kritik":{"type":"integer"}},"required":["kritik"]}' \
  > sonuc.json
jq -e '.is_error == false and has("structured_output")' sonuc.json
```

İki sınır işaretleyici vardır:

- **`--max-turns`:** tur sayısını sınırlar, dolunca hatayla çıkar. Belgede var, ama yerel 2.1.284 `--help` çıktısında görünmedi. Kullanmadan önce kendi sürümünde dene.
- **`--max-budget-usd`:** tahmini harcamaya üst sınır koyar, yalnız `-p` ile çalışır. Belge bunun istemci tarafı bir tahmin olduğunu ve gerçek faturadan sapabileceğini, sınırın aşılabileceğini yazar. Sınırı gerçek bütçenin altında tut.

Arka plan işi için belgede bir sınır daha var. Ana konuşmanın başlattığı bir arka plan komutu hâlâ çalışıyorsa koşum onu bekler. Beklenen bir şey yokken 10 dakika kesintisiz boşta beklenirse Claude Code çalışan işi durdurur ve kısmi sonucunu atar (süre bir ortam değişkeniyle değişir). Uzun işi arka plana atıp turu kapatmak bu yüzden güvenilir değildir.

## Hedef, döngü ve zamanlama

Dört mekanizma sık karıştırılır. Her biri farklı bir şeyle başlar ve farklı bir şeyle durur.

| Mekanizma | Sonraki tur ne zaman başlar | Nerede yaşar | Ne zaman biter |
|---|---|---|---|
| `/goal` | Önceki tur bitince | Oturum | Bir model koşulu karşılanmış bulunca |
| `/loop` | Zaman aralığı dolunca | Açık oturum | Sen durdurunca ya da 7 gün sonra |
| Masaüstü zamanlanmış görev | Zaman gelince | Senin makinen | Sen silince |
| Bulut rutini (`/schedule`) | Zaman gelince | Anthropic'in bulutu | Sen silince |

**`/goal`** bir tamamlanma koşulu verir. Her turdan sonra ayrı bir model koşulun sağlanıp sağlanmadığına bakar ve sağlanmadıysa Claude'u yeni tura sokar. `-p` ile de çalışır ve koşulu tek koşumda sonuna kadar götürür. Değerlendirici komut çalıştırmaz, dosya okumaz. Yalnız Claude'un konuşmaya getirdiği kanıtı görür. Bu yüzden koşulu "testler geçiyor ve çıkış kodu 0" gibi Claude'un çıktısında görünecek bir şeye bağla.

**`/loop`** oturum içi bir zamanlayıcıdır. Oturum kapanınca durur. Tekrarlayan görev oluşturulduktan 7 gün sonra son kez çalışır ve kendini siler. Kalıcı zamanlama yerine geçmez. [14.5](../README.md#14-rutin)

**Masaüstü zamanlanmış görev** makinende çalışır. Belgeye göre görev yalnız masaüstü uygulaması açıkken ve bilgisayar uyanıkken tetiklenir. Uyku boyunca kaçan koşum için uygulama açılınca, son yedi gün içinde en son kaçan zamana tek bir telafi koşumu başlatır. "Bilgisayarı uyanık tut" ayarı boşta uykuyu engeller, kapağı kapatmak yine uyutur.

**Bulut rutini** (`/schedule`) bilgisayarından bağımsızdır. Belge bunun bir araştırma önizlemesi olduğunu ve davranışın, sınırların değişebileceğini söylüyor. Rutin her koşuda depoyu taze klonlar, yerel dosyalarına erişemez, değişikliklerini `claude/` önekli bir dala yazar. Belgeye göre oturum otomatik modda başlar. En küçük aralık 1 saattir. [14.1](../README.md#14-rutin)

## Ön koşullar

Ayrılmadan önce dört şeye bak. Biri eksikse gece boşa gider. [13.2](../README.md#13-gozetimsiz)

- **İzin listesi.** Projenin `.claude/settings.json` içindeki allow listesi, gözetimsiz koşumu ayakta tutan şeydir. Başka projedeki liste seni kurtarmaz.
- **Disk.** `df -h .` yeterli boş yer gösteriyor mu?
- **Yük.** `uptime` makinenin sakin olduğunu gösteriyor mu?
- **Uyku ve şarj.** Makine prizde mi, uyku engelleniyor mu? `pmset -g` bunu gösterir (macOS).

## Tekrar başlatılabilir adımlar

Uyku ya da çökme işi baştan başlatmamalı. Ara çıktıyı diske yaz, her adımın başında "bu adım bitti mi" diye bak. Kaynağı geçici dizinde tutma, proje dizinine ya da kalıcı bir yola koy. [13.3](../README.md#13-gozetimsiz)

## Karar kuralları

- **Sen yokken verilebilecek kararları önceden yaz.** Geri alınamaz adım engelli işaretlenir. [13.1](../README.md#13-gozetimsiz)
- **Çıkış kodu, `is_error` ve sonuç türünü birlikte oku.** Geçerli JSON başarı kanıtı değildir. [14.6](../README.md#14-rutin)
- **Makineye aktarılacak sonuca şema ver,** `structured_output` varlığını kontrol et. [14.7](../README.md#14-rutin)
- **Uzun işi ön planda tut,** log'u oturumdan bağımsız bir yola yaz. Arka plana düşen işi bitmesini bekleyerek ve çıkış satırını okuyarak uzlaştır. [13.4](../README.md#13-gozetimsiz)
- **"Ucuz" bir komutun süresini varsayma.** Yük altında uzar. [11.4](../README.md#11-paralel)
- **Makineden bağımsız olması gereken işi buluta ya da bulut rutinine ver.** Yerel dosya isteyen iş makinede kalır. [14.1](../README.md#14-rutin)
- **Rutinin kendisini izleyen küçük bir nöbet kur.** Hiç koşmayan rutin hata da vermez. [14.3](../README.md#14-rutin)
- **Sessizliği başarı sayma.** Kanıt log'un son satırı, çıkış durumu ve beklenen çıktı dosyasıdır.

## Hata biçimleri

**Gerçek vaka D01: mod sessizce değişti.** Zamanlanmış oturumların izinsiz ilerlemesi için bir mod ayarlanmıştı. Bir projenin 43 oturum kaydındaki 345 mod değeri tarandı ve bu mod hiç görünmüyordu. Mod ilk kullanımda onay penceresi istiyor, zamanlanmış oturum pencereyi gösteremeyince hata vermeden varsayılan moda düşüyordu. Gözetimsiz koşumu ayakta tutan şey projenin kendi izin listesiydi. Ayrıntısı [Gerçek deneyimlerden on ders](../ekler/deneyimler.md) sayfasında D01.

**Gerçek vaka D03: arka plandaki iş tur bitince öldü.** Zamanlanmış bir görev uzun bir veri çekimini arka planda başlattı ve turu "bekliyorum" diye kapattı. Oturum kapanınca süreç öldü, çıktı dizinle birlikte silindi. 83 dakika boyunca ağa tek istek gitmedi ve geriye tek satır kanıt kalmadı. Aynı iş ön planda ve kalıcı log'la 12 dakikada bitti. Ayrıntısı D03.

**Gerçek vaka D04: "ucuz" kontrol 120 kat uzadı.** Görev dosyası bir test komutunu yaklaşık 2,5 saniye diye tarif ediyordu. Bir nöbet koşumunda aynı komut 300 saniyelik ön plan sınırını aştı ve arka plana düştü. Makine yükü o dakikada 68'e çıkmıştı. Ders: arka plana düşen kontrolü bitmesini bekleyerek uzlaştır, yoksa D03 tekrarlanır. Ayrıntısı D04.

**Gerçek vaka D05: uyku engelleyici bataryada işe yaramadı.** Gece koşumu bir uyku engelleyiciyle sarılmıştı, makine prizde değildi. 19 saatte süreç 1,2 saniye işlemci zamanı kullandı ve çıktı dosyası boş kaldı. Prize takılınca aynı koşum 20 dakikada bitti. Ayrıntısı D05.

**Gerçek vaka D09: geçici dizin toptan silindi.** Çok günlük bir yazı serisinin kaynakları oturumun geçici çalışma dizinindeydi. Dizin ağacı bir akşam silindi. Metinler alt ajan kayıtlarından geri kuruldu, görsellerin yerel kopyası gelmedi. Ayrıntısı D09.

**Kurgu senaryo: sabah boş log.** Deniz her gece yapılan bir raporu `/loop` ile kurar ve ertesi sabah log'un boş olduğunu görür. Sebep, 7 gün dolduğu için görevin kendini silmesidir. Hata yoktu, çünkü koşum hiç tetiklenmemişti. Kalıcı zamanlamayı bulut rutinine ya da masaüstü göreve taşır ve yanına son başarılı koşumu kontrol eden bir nöbet ekler.

## Alıştırma: bir gece koşumu kur, sabah kanıtla oku

Gerçek bir iş deposunda değil, bu iş için açtığın bir deneme deposunda yap.

1. `gorev.md` yaz. İçine yetkili kapsamı, engel davranışını ve istenen çıktı dosyasını yaz. Örnek görev: depodaki her kaynak dosyanın satır sayısını `work/sonuc.json` içine yaz.
2. Ayrılmadan önce `df -h .`, `uptime`, `pmset -g` çıktılarını `work/on-kosul.txt` dosyasına kaydet. `/permissions` ile izin listesini incele.
3. Koşumu şu biçimde kur: JSON çıktı, tur sınırı, kendi log yolu, çıkış kodunun dosyaya yazılması.
   ```
   mkdir -p work/runs
   claude -p "$(cat gorev.md)" --output-format json --max-turns 30 \
     > work/runs/sonuc.json 2> work/runs/hata.log
   printf '%s\n' "$?" > work/runs/exit-code.txt
   ```
4. Koşumu zamanla ya da elle başlat. Başlamadan önce yarıda öldürüp yeniden başlatmayı bir kez dene, tamamlanan adımlar atlanıyor mu bak.
5. Sabah üç şeye bak: `exit-code.txt`, `sonuc.json` içinde `is_error` ve `subtype`, `work/sonuc.json` dosyası.

**Bitti sayılması için:** `exit-code.txt` içinde 0, `sonuc.json` içinde `is_error: false`, beklenen çıktı dosyası var ve içeriği görev tarifine uyuyor, log'un son satırı işin bittiğini gösteriyor. Bunlardan biri eksikse iş bitmiş sayılmaz, yalnız sessiz kalmıştır.

## Bağlantılar

Kontrol listesi: [13.1](../README.md#13-gozetimsiz) [13.2](../README.md#13-gozetimsiz) [13.3](../README.md#13-gozetimsiz) [13.4](../README.md#13-gozetimsiz) [13.5](../README.md#13-gozetimsiz) [13.6](../README.md#13-gozetimsiz) [14.1](../README.md#14-rutin) [14.2](../README.md#14-rutin) [14.3](../README.md#14-rutin) [14.4](../README.md#14-rutin) [14.5](../README.md#14-rutin) [14.6](../README.md#14-rutin) [14.7](../README.md#14-rutin). Ekler: [Gerçek deneyimlerden on ders](../ekler/deneyimler.md), [Komutlar ve kısayollar](../ekler/komutlar.md), [Sorun giderme](../ekler/sorun-giderme.md). Önceki bölüm: [Bölüm 9: Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md).

---

[← Bölüm 9](09-paralel-isler.md) · [İçindekiler](README.md) · [Bölüm 11 →](11-ekip-olcegi.md)

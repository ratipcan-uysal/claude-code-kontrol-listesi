## Zihinsel model: oturum, bir çalışma masasıdır

Bir oturumun bağlam penceresi küçük bir çalışma masasına benzer. Üzerinde konuşma, okunan dosyalar ve komut çıktıları durur. Masa doldukça önemli kâğıtlar altta kalır. Yeni bir iş için masayı boşaltmak, aynı masada üç işi birden yürütmekten hem ucuz hem güvenlidir. Belge bunu doğrudan söyler: `/clear` ilgisiz görevler arasında maliyetsizdir ve sonraki görev bir öncekinin geçmişine ödeme yapmaz.

Oturumları yönetmek beş soruya iner. Bu iş için yeni masa mı açayım? Masayı bir yere not alıp mı bırakayım? Aynı masaya mı döneyim? Masayı kopyalayıp başka bir yol mu deneyim? Yaptığım son şeyi geri mi alayım? {{bolum:1}} bölümündeki zihinsel modeli hatırla: Claude'un bildiği, pencerede olandır. Bu bölümdeki her komut pencerenin içeriğini değiştirir.

## Konu başına oturum

Bir oturum tek bir tutarlı işe ait olsun. Önceki işin dosyaları ve kararları pencerede kalırsa yeni işi de etkiler. Yeni bir konuya geçince `/clear` yaz. Belge ayrıca `/clear oauth-gecisi` gibi bir adla önceki konuşmayı etiketleyebileceğini söyler, böylece sonra `/resume` listesinde bulursun. [[2.1]] [[2.3]]

Belgenin bir başka uyarısı: Claude'u iki kez düzelttin ve hâlâ yanlış yapıyorsa üçüncü düzeltmeyi yazma. `/clear` yap ve öğrendiklerinle daha iyi bir prompt yaz. Kirli bağlamda yapılan üçüncü düzeltme genellikle ilk ikisinin üstüne eklenen bir karmaşa olur.

## Devir dosyası

Konuşma taşınmaz, dosya taşınır. İş yarım kalacaksa oturumu kapatmadan Claude'dan bir devir dosyası yazmasını iste: neyi bitirdin, neyi bitirmedin, hangi kararları verdin, sıradaki adım ne. Dosya projede durur, yeni oturum onu okuyarak kaldığı yerden başlar. Bu belgenin zorunlu kıldığı bir özellik değil, iş akışı önerisidir. Ama CLAUDE.md'nin ve dosyaların oturumlar arası tek taşıyıcı olduğu gerçeğine dayanır.

İyi bir devir dosyası üç şey içerir: bitenin kanıtı, bekleyen işin adımları ve "denedim, olmadı" listesi. Üçüncüsü en çok unutulandır ve yeni oturumun aynı çıkmaz sokağa girmesini önler. [[2.1]]

## /compact: ne kaybolur

`/compact` konuşmayı özetleyip sürdürür. Belgeye göre sıkıştırmadan sonra şu şeyler diskten geri gelir: proje kökündeki CLAUDE.md, kapsamsız kurallar, otomatik bellek ve plan modunda yazılan plan. Son okunan ya da düzenlenen dosyalardan en çok beşi yeniden okunur ve 5.000 token'dan büyük dosya yalnız yol olarak döner.

Şunlar özetin insafına kalır: sohbette verdiğin talimatlar, `paths` alanıyla yüklenen kurallar ve alt dizin CLAUDE.md dosyaları (bunlar ilgili dosyaya yeniden dokunulunca geri yüklenir), hook'ların eklediği bağlam ve araç çıktılarının ayrıntısı. Bu yüzden `/compact` kullanırken neyin korunacağını yaz: `/compact API değişikliklerini ve test komutlarını koru`. Önemli bir talimat sohbetteyse önce dosyaya taşı. [[2.6]]

## /resume ve --continue

Aynı konuşmaya dönmenin iki yolu var. `claude --continue` bu dizindeki son oturumu açar. Orada oturum yoksa belge bunu açıkça yazar: "No conversation found to continue" der ve çıkar. `/resume` (ya da `claude --resume`) bir seçici açar ve `/rename` ile ad verdiysen adla bulursun. Geçmişe dönmek yeni bir masa değil, eski masaya dönmektir: o gün pencerede ne varsa geri gelir, düne ait eski bilgi de dahil. [[2.7]]

## /branch ile /fork farkı

İkisi de konuşmayı kopyalar ama kopyanın nerede yaşadığı farklıdır.

| Komut | Ne yapar | Sen nerede kalırsın |
|---|---|---|
| `/branch [ad]` | Konuşmayı bu noktadan dallar | Dalın içine geçersin, orijinale `/resume` ile dönersin |
| `/fork [prompt]` | Kopyayı arka plan oturumunda sürdürür | Bulunduğun oturumda kalırsın |

Belgenin dediği: `/fork` kopyayı ayrı bir arka plan oturumu olarak çalıştırır. Agent view kapalıysa `/fork` bir fork edilmiş alt ajan başlatır. İki yolu yan yana denemek istiyorsan `/branch` yeterli. Birini arka planda koştururken kendi işine devam etmek istiyorsan `/fork` kullan. Yerel sürümün `/fork`'u desteklemeyebilir, belge daha yeni olabilir: `claude --version` ile bak. [[2.7]]

## /rewind ve sınırı

`/rewind` (ya da boş istemde `Esc Esc`) kodu, konuşmayı ya da ikisini bir önceki noktaya sarar. Menüde "Summarize from here" ve "Summarize up to here" seçenekleri de var, yani rewind aynı zamanda seçmeli bir `/compact` gibi de çalışır. Istemde yazı varsa çift `Esc` yazıyı siler, rewind menüsünü açmaz. Silinen yazıyı yukarı okla geri çağırırsın.

Sınırı bil. Belgeye göre rewind yalnız Claude'un dosya araçlarıyla düzenlediği dosyaları izler. Yalnız Bash komutuyla değişen bir dosya geri alınmaz. Oturum dışında elle yaptığın değişiklikler ve başka bir paralel oturumun düzenlemeleri de normalde yakalanmaz. Asıl güvence Git'tir. Riskli bir adımdan önce commit at, rewind'a yedek olarak güvenme. [[15.2]]

## Esc ile araya girmek ve /btw

`Esc` Claude'u işin ortasında durdurur ve o ana kadarki her şeyi korur. Belge ilk dakikayı izlemeyi önerir: Claude yanlış yöne giderse hemen `Esc` bas ve yönlendir. Geç kalırsan yanlış yönde yüz satır üretilir.

`/btw` ise ana işi bölmeden kısa bir soru sormaya yarar. Soru ve cevap konuşma geçmişine girmez, bu yüzden bağlamı şişirmez. Claude cevabı yalnız o anda konuşmada olan bilgiden verir, yeni dosya okumaz. Yani "az önce hangi yapılandırma dosyasından söz etmiştin?" iyi bir `/btw` sorusudur. "Şu dosyada ne var?" değildir.

## Karar kuralları

- **Konu değişti mi? `/clear`.** Konuyu etiketleyerek çık, sonra bulursun.
- **Yarım kalan iş mi? Önce devir dosyası, sonra çık.**
- **Sıkıştırmadan önce korunacakları yaz.** Sohbette kalan talimatı dosyaya taşı.
- **Dün üzerinde çalıştığın işe mi dönüyorsun? `--continue` ya da `/resume`.** Yeni bir yaklaşım için `/clear`.
- **İki yol mu deneyeceksin? `/branch`.** Biri arka planda koşsun istiyorsan `/fork`.
- **Son adım yanlış mıydı? `/rewind`, ama Bash'le değişen dosyayı Git'ten geri al.**
- **Claude yanlış yöne gidiyorsa `Esc`.** Kısa bir yan soru mu? `/btw`.

## Hata biçimleri

**Gerçek vaka: oturumlar arası ortak olan şey sandığından fazlaydı.** Birden çok oturum aynı depoda çalışırken stage edilen dosyalar, başka bir oturumun commit'iyle başka bir mesajın altına girdi. Oturum yönetimi yalnız konuşmayla ilgili değil, ortak kaynaklarla da ilgilidir. Ayrıntısı {{ek:deneyimler}} sayfasında D06. Stage ile commit'i tek adımda yapmak bu sorunu önler.

**Gerçek vaka: geçici dizin devir dosyası için kötü yerdi.** Birden çok gün sürecek bir işin kaynakları oturumun geçici çalışma dizinindeydi ve dizin toptan silindi. Devir dosyasını proje dizinine yaz. Ayrıntısı D09.

**Kurgu senaryo: rewind'ın görmediği dosya.** Defne, Claude'a bir betik çalıştırtır. Betik `rapor.csv` dosyasını yeniden üretir ve eski hâlini ezer. Sonuç yanlıştır, Defne `/rewind` yapar. Kod düzenlemeleri geri döner, `rapor.csv` yerinde kalır, çünkü yalnız Bash değiştirmiştir. Dosya Git'te olsaydı `git restore rapor.csv` bir saniyede çözerdi.

## Alıştırma: iki yolu dallayıp birini seç

Herhangi bir git deposunda yap. Kendi çalışma dalında kal.

1. Küçük bir iş seç ve iki makul yolu olduğundan emin ol, ör. bir listeyi önce sıralamak mı yoksa önce filtrelemek mi. Claude'a işi anlat ve "henüz kod yazma, yaklaşımı konuşalım" de. Konuşma bu noktaya gelince iki yol da açık kalır.
2. `/branch yol-a` yaz. Bu dalda birinci yolu uygulat, sonucu `git diff --stat` ile kaydet, sonra `git restore .` ile dosyaları temizle.
3. `/resume` ile ilk konuşmaya, yani dallanma noktasına dön. `/branch yol-b` yaz ve ikinci yolu uygulat. Sonucu yine `git diff --stat` ile kaydet.
4. İki diff'i yan yana oku. Hangisi daha küçük, hangisi daha okunur, hangisinin testi var? Birini seç. Seçmediğin yolun diff'i artık bir kayıttan ibaret, onu zaten geri almıştın.
5. Seçtiğin yolu seçtiğin dalda yeniden uygulat, commit'le ve bir devir dosyası yaz: ne seçtin, neden, öteki yolda ne gördün.

**Bitti sayılması için:** iki yolun diff özeti, seçimin gerekçesi bir cümle ve `/resume` listesinde iki dalın adı.

## Bağlantılar

Kontrol listesi: [[2.1]] [[2.3]] [[2.6]] [[2.7]] [[15.2]]. Önceki bölüm: {{bolum:2}}. Sonraki: {{bolum:4}}. Ekler: {{ek:komutlar}}, {{ek:sorun-giderme}}, {{ek:dosyalar}}.

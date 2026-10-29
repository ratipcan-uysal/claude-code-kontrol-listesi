# 9. Paralel işler: bağımsızlığı ölçmek

_Uzman · Belge kontrolü: 29 Ekim 2026_

Paralel çalışma yalnız sonuçları ve kaynakları gerçekten bağımsız işlerde kazandırır. Worktree dosya ve index çakışmasını çözer, port, tarayıcı, pano, simülatör ve makine yükü ortak kalır.

## Zihinsel model: paralel olmak bağımsız olmak demek değildir

Aynı anda üç iş başlatmak, işi üç kat hızlandırmaz. Hızlanma yalnız işler gerçekten birbirinden bağımsızsa gelir. Bağımsızlık da işin başlığına bakarak değil, sonucuna bakarak ölçülür. Kendine şunu sor: A işinin sonucu, B işinin ne yapacağını değiştirir mi? Değiştirmiyorsa iş paralel olabilir. Değiştiriyorsa ikisini aynı anda başlatmak yalnız çakışma üretir.

Ölçü iki katmanlıdır. Önce **sonuç bağımsızlığı**: iki işin çıktısı aynı dosyaya, aynı karara ya da birbirinin girdisine dokunuyor mu? Sonra **kaynak bağımsızlığı**: iki iş aynı git index'ini, aynı portu, aynı tarayıcı oturumunu, aynı panoyu ya da aynı simülatörü kullanıyor mu? Sonuçları bağımsız iki iş, ortak bir kaynak yüzünden yine de birbirini bozabilir.

## Üç paralellik biçimi

Claude Code'da paralel çalışmanın üç yolu var. Farkları bağlam, dosya sistemi ve bedel üzerinden okunur.

| Biçim | Bağlam | Dosyalar | En uygun iş |
|---|---|---|---|
| Alt ajan | Kendi penceresi, sana yalnız özet döner | Varsayılan olarak ana oturumla aynı dizin | Okuma ağırlıklı geniş araştırma |
| Ayrı oturum | Tamamen ayrı konuşma | Aynı checkout, istersen ayrı worktree | Uzun, birbirinden kopuk işler |
| Worktree | Oturumdan bağımsız bir dosya kopyası | Kendi dalı, kendi index'i | Aynı depoya yazan paralel işler |

Üçü birbirini dışlamaz. Alt ajan ya da ayrı oturum, worktree içinde de çalışabilir. Belgeye göre `isolation: worktree` ayarlı bir alt ajan deponun yalıtılmış bir kopyasında çalışır ve değişiklik yapmazsa worktree otomatik silinir. Yalnız okuyan bir alt ajana worktree gerekmez. Dosya yazan her paralel işe gerekir.

## Worktree'nin tam olarak ne yaptığı

`claude --worktree odeme-ekrani` komutu depoyu `.claude/worktrees/` altında yeni bir dala açar. Bu bir **taze checkout**'tur. İki sonucu var ve ikisi de sürpriz çıkarır.

**Varsayılan dal.** Belgeye göre yeni worktree, mevcut dalından değil deponun varsayılan dalından (genellikle `main`) açılır. Alt ajanların `isolation: worktree` kopyası da aynı kuralı izler. Yerelde commit'lediğin ama push etmediğin işler, ya da bir özellik dalındaki yarım iş worktree'de yoktur. İstersen `worktree.baseRef` ayarını `"head"` yaparsın. Bu ayar dal adı kabul etmez, yalnız `"fresh"` (varsayılan) ya da `"head"` alır.

**Ignore edilmiş dosyalar gelmez.** Worktree'ye yalnız git'in izlediği dosyalar gelir. `.env` gibi dosyaları otomatik taşımak için proje köküne `.worktreeinclude` yazarsın. Dosya `.gitignore` sözdizimini kullanır ve yalnız hem eşleşen hem ignore edilmiş dosyalar kopyalanır. Bağımlılıkları ise worktree'de yeniden kurman gerekir. Ayrıntı [Dosya konumları](../ekler/dosyalar.md) sayfasında.

Etkileşimli bir worktree oturumundan çıkarken Claude Code temiz worktree'yi siler, iş içerene sorar. `-p` ile koşan oturumlarda çıkış sorusu yoktur, yani temizlik de yoktur. Bu worktree'leri `git worktree remove` ile kendin kaldırırsın.

## Paylaşılan kaynaklar

Worktree yalnız dosya ve index çakışmasını çözer. Makinedeki geri kalan her şey hâlâ ortaktır.

- **Git index'i.** Aynı checkout'taki bütün oturumlar tek index'i paylaşır. Başkasının stage'ini senin commit'in alıp götürebilir. Ayrı worktree'nin index'i ayrıdır. [11.2](../README.md#11-paralel)
- **Port.** İki sunucu aynı porta bağlanamaz, ya da ikinci biri birincisini düşürür. Her projeye sabit ve ayrı port ver. [11.3](../README.md#11-paralel)
- **Tarayıcı oturumu.** Paylaşılan sekmeyi başka oturum öne getirir, sen kendi uygulamanı bozuk sanırsın. [11.3](../README.md#11-paralel)
- **Pano.** Makinede tek pano var. İki oturum değer yapıştırırsa biri ötekini ezer. Değeri doğrudan alana yaz, yazdıktan sonra geri oku.
- **Simülatör ve cihaz.** Tek simülatörü iki oturum sürerse ekrandaki durum her ikisine de yabancı olur.

Bu liste kapalı değil. Bir şey makinede tek bir örnek olarak duruyorsa, iki paralel iş için çakışma noktasıdır.

## Makine yükü ve ajan sayısı

Her paralel iş makinenin işlemcisini, belleğini ve diskini yer. Ajan sayısı "kaç tane açabilirim" sorusuyla değil, "kaç tane bağımsız iş var" sorusuyla belirlenir. Beş ajan başlatıp ancak iki gerçek bağımsız iş bulmuşsan, kalan üçü yük ve token harcar, hız kazandırmaz. Çok ajanlı iş akışı onlarca ajan çağırabilir ve belge bunun çok token harcadığını söyler. Kullanım farkına `/usage` ile bak. [11.6](../README.md#11-paralel)

Yük ölçümü tek bir eşiğe bağlanmaz. Bir dakikalık yük ortalaması on beş dakikalığın birkaç katıysa yük o pencerede fırlamıştır. CPU, bellek baskısı ve disk birlikte izlenir. [11.4](../README.md#11-paralel)

## Birleştirmenin bedeli

Paralel iş, sonunda birleştirmeyi ister ve bu bedel ajan sayısıyla büyür. Her worktree ayrı bir dal olduğu için her biri ayrı incelenir, ayrı test edilir ve ana dala ayrı katılır. İki dal aynı dosyaya dokunduysa çakışmayı birisi çözer. Birleştirme maliyeti işi bölmenin kazancından büyükse, bölme. Bağımsızlığı ölçerken şunu da hesaba kat: işleri bitirdikten sonra birleştirme için harcayacağın süre, paralelliğin sana kazandırdığı süreyi aşıyor mu?

## Bulut oturumu

Makineyi yormadan paralel iş çalıştırmanın bir yolu, işi bulut oturumuna göndermektir. Bulut oturumu depoyu taze klonlar ve değişikliklerini `claude/` önekli bir dala yazar. Yerel dosyalarına, yerel simülatörüne ve yerel portuna erişemez. Yerel cihaz isteyen iş yerelde kalır. Bilgisayar uyusa bile ilerler. [11.5](../README.md#11-paralel)

## Karar kuralları

- **Önce sonucu sor.** B, A'nın çıktısına bağlıysa ikisini sırala. [11.6](../README.md#11-paralel)
- **Dosya yazan her paralel işe ayrı worktree ver.** Yalnız okuyan iş worktree'siz de olur. [11.1](../README.md#11-paralel)
- **Worktree'ye yerel commit gerekiyorsa** önce push et ya da `worktree.baseRef: "head"` kullan.
- **Port, tarayıcı, simülatör gibi tek örnekli kaynaklara sahip çıkan iş sayısını bire indir** ya da her işe ayrı kaynak ver.
- **Ajan sayısını bağımsız iş sayısına eşitle,** makine yüküne göre aşağı çek. [11.4](../README.md#11-paralel)
- **Birleştirmeyi baştan planla.** Hangi dal hangi sırayla girecek, yazmadan başlama.
- **Makineden bağımsız kalması gereken uzun işi buluta gönder.** [11.5](../README.md#11-paralel)

## Hata biçimleri

**Gerçek vaka D06: başka oturumun commit'i değişikliklerimi götürdü.** Değişiklikler stage edildi, ardından üç dakikalık bir derleme koştu. Bu arada aynı repoda çalışan başka bir oturum kendi raporunu commit'ledi ve commit index'in tamamını aldı. Dört dosya başka bir mesajın altına girdi, asıl commit "değişiklik yok" diye boş döndü. İçerik doğruydu, yalnız mesaj yanlıştı. Ders: stage ile commit tek komutta olsun, arada derleme gerekiyorsa ayrı worktree kullan. Ayrıntısı [Gerçek deneyimlerden on ders](../ekler/deneyimler.md) sayfasında D06.

**Gerçek vaka D08: dört paralel oturum makineyi kilitledi.** Dört alt oturum ayrı worktree'lerde aynı anda derleme ve test koştu, başka projelerin derlemeleri de sürüyordu. Yük ortalaması 720'ye çıktı, sakin makinede 4'tü. Worktree dosyaları ayırmıştı, işlemciyi ayırmamıştı. "Ağır komutu kilitle sar" diye verilen metin talimatı yeni oturumlara ulaşmadı. Çalışan çözüm kesin katmandaydı: ağır komutları iki yuvalı kilitle koşturan bir sarmalayıcı ve sırasız ağır komutu reddeden bir hook. Ayrıntısı D08.

**Kurgu senaryo: iki özellik, tek ekran.** Ayşe iki ajanı iki worktree'de çalıştırır. Birine "profil ekranına avatar ekle", ötekine "profil ekranının yerleşimini yenile" der. Dosyalar ayrıdır, ama iki iş aynı ekranı yeniden yazıyor. Birleştirirken biri ötekinin işini siler. Sonuçlar bağımsız değildi, yalnız dosya adları ayrıydı.

## Alıştırma: iki bağımsız işi iki worktree'de bitir

Herhangi bir git deposunda yap, ama önce depoda en az bir commit olduğundan emin ol.

1. Birbirine dokunmayan iki küçük iş seç. Örnek: biri README'ye bir bölüm ekler, öteki bir yardımcı fonksiyona test yazar. İkisinin de çıktısının diğerini etkilemediğini bir cümleyle yaz.
2. İki ayrı terminal aç. Birinde `claude --worktree is-bir`, ötekinde `claude --worktree is-iki` çalıştır. `git worktree list` çıktısını kaydet.
3. Her oturumda işi yaptır ve o oturumun worktree'sinde commit'le. Commit'ten önce `git diff --cached` ile kapsamı gör.
4. Ana kopyaya dön. İki dalı sırayla birleştir ve her birleştirmeden sonra testi koş. Çakışma çıkarsa nedenini kaydet.
5. `git worktree remove` ile iki worktree'yi kaldır.

**Bitti sayılması için:** `git worktree list` iki ayrı satır göstermiş olsun, `git log --stat` her işin kendi commit'inde yalnız kendi dosyalarını göstersin, birleştirmeden sonra test sayısı (sıfır değil) kayıtlı olsun.

## Bağlantılar

Kontrol listesi: [11.1](../README.md#11-paralel) [11.2](../README.md#11-paralel) [11.3](../README.md#11-paralel) [11.4](../README.md#11-paralel) [11.5](../README.md#11-paralel) [11.6](../README.md#11-paralel). Ekler: [Gerçek deneyimlerden on ders](../ekler/deneyimler.md), [Dosya konumları](../ekler/dosyalar.md), [Komutlar ve kısayollar](../ekler/komutlar.md). Sonraki bölüm: [Bölüm 10: Gözetimsiz iş: sen yokken çalışan sistem](10-gozetimsiz-is.md).

---

[← Bölüm 8](08-hook-ile-garanti.md) · [İçindekiler](README.md) · [Bölüm 10 →](10-gozetimsiz-is.md)

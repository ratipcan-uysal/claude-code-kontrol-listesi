# 14. Projects: koordinatör ve thread'ler

_Uzman · Belge kontrolü: 29 Ekim 2026_

Proje, işi thread'lere bölen tek bir konuşmadır. Her thread repoyu temiz klonlayan bir bulut oturumudur ve makinendeki hook, izin ve skill'leri değil, proje talimatını, belleğini, connector'larını ve ortamını alır.

## Zihinsel model: bir koordinatör, çok thread, ortak makine yok

[Bölüm 9: Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md) paralel işi kendi makinende nasıl yöneteceğini anlattı. Projects aynı sorunu bir kademe yukarıdan çözer: paralel oturumları sen değil Claude başlatır ve izler. Belge bunu public beta olarak tanımlıyor. Yalnız Pro ve Max planlarında var, Team ve Enterprise'da henüz yok. Terminal CLI'da, VS Code ve JetBrains'te de yok. Projects'e claude.ai/code'dan, masaüstü uygulamasından ya da mobil uygulamadan girersin.

Proje, tek ve uzun süren bir konuşmadır. Belgeye göre Claude burada koordinatör gibi davranır: gelen işi alır, hangisinin thread olacağına karar verir, her thread'in ne yaptığını takip eder. Thread'ler işçidir. Her biri kendi bağlam penceresi olan ayrı bir oturumdur. Çoğu zaman bir bulut oturumudur, kendi dalında çalışır ve iş gerektirirse pull request açar. Koordinatör thread'lerin raporunu görür, attıkları her adımı görmez.

Ana fikir: **thread'ler senin makinende değil, temiz bir bulut ortamında doğar.** Her cloud thread şunlarla başlar:

- Projenin repoları ve dosyaları, proje talimatı ve proje belleği.
- Her reponun kökündeki `CLAUDE.md`, `.claude/CLAUDE.md` ve yola özel olmayan `.claude/rules/` dosyaları.
- claude.ai hesabındaki connector'lar.
- Projenin cloud environment'ı: ağ erişimi, ortam değişkenleri, network secret'lar ve kurulum betiği.

Belgeye göre thread'ler reponun skill'lerini, `.mcp.json` dosyasını, `.claude/settings.json` içindeki izin kurallarını, hook'larını ve `env` bloğunu yüklemez. Yani [Bölüm 8: Hook ile garanti: olay, çıkış kodu, sınama](08-hook-ile-garanti.md) ve [Bölüm 6: İzin ve güvenlik: mod, kural, sandbox](06-izin-ve-guvenlik.md) kurduğun garantilerin çoğu thread'e ulaşmaz. Normal bir bulut oturumu tek repolu olduğunda repo ayarlarını okur, proje thread'i okumaz.

## Kurulum kontrolü: ilk thread'den önce

Belgenin ön koşulları kısa.

- **Plan.** Pro ya da Max olacak, kenar çubuğunda **Projects** görünecek (doğrudan ya da **More** altında).
- **GitHub.** Kod github.com'da olacak. GitHub Enterprise Server, GitLab ve Bitbucket belgede dışarıda. Bağlı GitHub hesabının push erişimi olacak ve **Claude GitHub App** repoya kurulu olacak. `/web-setup` ile bağladığın token diğer bulut oturumlarına yeter, projenin thread'lerine yetmez. Bir organizasyonun reposunu yalnız organizasyon sahibi kurabilir. SSO zorunluysa Claude uygulamasına organizasyon için ayrıca izin vermen gerekir.
- **Bağlantı hatası.** Belgedeki üç mesaj (erişim yok, klonlama başarısız, "Claude can't access") aynı yere çıkar: App kurulu mu, askıda mı, hesaba bağlı mı. Mesajdaki **Install GitHub App** ya da **Select repositories on GitHub** düğmesine bas, sonra **Check again**.
- **Connector'lar.** İşin ihtiyaç duyduğu MCP sunucusu claude.ai connector listesinde bağlı görünmeli.

## Ortam ve sırlar: thread'e ne verirsin

**Repo seçimi.** Belgenin önerisi: sık dokunduğun bir iki repoyu projeye ekle, geri kalanını proje talimatında adlandır. Eklediğin repo her thread'de klonlanır ve `CLAUDE.md`'si baştan yüklenir. Eklemediğin repoyu, ilk görev gerektirdiğinde thread kendine ekleyebilir. Ama klonlama görevin ortasında olur, o reponun `CLAUDE.md`'si thread başlarken yoktu. Klasör eklersen proje yalnız ilk 100 dosyanın ve en fazla 200 MB'ın kopyasını alır, projede en çok 10 klasör olur. Yüzlerce dosya yüklemek yerine ayıkla.

**Proje talimatı.** Belgedeki sınır 16.000 karakter. Talimat her yeni thread'e ve proje konuşmasındaki Claude'a gider. Belge şu içeriği öneriyor: projenin amacı, işin nerede olduğu (repo, başlangıç dalı, PR adlandırma), thread'in işini nasıl kontrol edeceği, eksik bir şey olunca ne yapacağı, neyin önce onayını isteyeceği. Reponun kendi kuralları o reponun `CLAUDE.md`'sine gider, talimatta tekrar edilmez ([Bölüm 5: Talimat mimarisi: rica ile garanti](05-talimat-mimarisi.md)). Birden çok doğruluk kaynağı varsa çelişkide hangisinin kazanacağını yazmak belgede geçmiyor, bu bir iş akışı önerisi. Yazarsan yine de işe yarar, çünkü thread'ler birbirini göremez.

**Proje belleği.** Bu, makinendeki otomatik bellek değil. Ayrı bir `MEMORY.md` dizini ve dosyaları var. Claude'dan bir kararı ya da tuzağı "hatırlamasını" istersin. Her cloud thread dizini başta okur, diğer dosyaları gerektiğinde açar. **Project settings > Memory** altında dosyaları okur, düzenler, silersin. Eskiyen kayıt yanlış bilgiyi kalıcı yapar. Düzenli temizlemek belgede yok, iş akışı önerisi ([Bölüm 12: Sistemi iyileştirmek: hatayı katmana yazmak](12-sistemi-iyilestirmek.md)). Makinende koşan thread proje belleğini yüklemez, talimatı yükler.

**Model ve effort.** Belgeye göre yeni proje her yerde Opus kullanır. Thread'ler yüksek effort, koordinatör düşük effort çalışır. Ayarlar Thread model, Thread effort, Coordinator model ve Coordinator effort. Belge ilk toplu işten önce bunlara bakmanı öneriyor. Tek bir görev için ayrı model istersen görevde yazarsın.

**Ortam.** Ortamı bir kez kurarsın, bütün thread'ler onu kullanır. Varsayılan ağ düzeyi **Trusted**: paket kayıt defterleri, GitHub ve bulut SDK'ları gibi izinli alan adları. Başka bir alan adı lazımsa **Custom** seçip listeyi sen yazarsın. Ortam değişkeni ile network secret farkı önemli:

| | Ortam değişkeni | Network secret |
|---|---|---|
| Kim okur | Ortamı kullanan herkes | Oturum anahtarı hiç görmez |
| Nasıl çalışır | Oturumda sıradan değişken olur | Anthropic'in proxy'si, listelediğin host'lara giden isteğe anahtarı ekler |
| Ne zaman | Gizli olmayan ayar | API anahtarı ve token |

Network secret Pro, Max, Team ve Enterprise'ta var, yalnız Anthropic-hosted ortamda çalışır. Proxy bazı isteklere anahtar eklemez (GitHub, Anthropic API, genel paket kayıt defterleri gibi). Bu durumda anahtar ortam değişkeninde kalır.

**Kurulum betiği.** Yeni cloud oturumu başlarken Claude Code'dan önce çalışır, root olarak, Ubuntu 24.04'te. Sıfırdan farklı çıkarsa oturum başlamaz. Yaklaşık beş dakika altında biterse Anthropic dosya sistemini önbelleğe alır, sonraki oturumlar betiği atlar. Önbellek yaklaşık yedi gün yaşar, betiği ya da izinli host'ları değiştirince yeniden kurulur. Önbellek dosya sistemi görüntüsüdür: yüklü paketler kalır, arka planda çalışan süreç, başlatılmış veritabanı kalmaz. Betik çalışırken ortam değişkenleri henüz ayarlı değildir.

**Connector ve plugin.** Thread'ler MCP araçlarını claude.ai hesabındaki connector'lardan alır. Her thread hepsini kullanabilir, proje başına kurulum yok. Proje konuşmasının kendisinde connector yoktur, connector isteyen işi thread'e görev olarak ver. Plugin'ler **Project settings > Plugins** altından eklenir. Reponun `.claude/settings.json` dosyasında açık plugin'ler bulut thread'ine yüklenmez. Skill'ler için de aynı: repoda commit'lenen skill yüklenmez, hesabında açtığın skill'ler yüklenir.

## Karar kuralları

- **Projects mi, başka yol mu?** Hedef tek oturumu aşıyor, günlerce görev üretiyor ve makinen kapalıyken de ilerlemesi gerekiyorsa proje. Tek göreve tek bulut oturumu yeter. Her görev yerel makineni istiyorsa yerel oturum ya da agent view. Konuşmasız, takvime bağlı tek iş için scheduled task. Bir oturum içi yan işe alt ajan ([Bölüm 7: Yeniden kullanım: skill, alt ajan, MCP, plugin](07-skill-ajan-mcp.md)). Belge beş yolu yan yana karşılaştırıyor. [11.5](../README.md#11-paralel) [14.1](../README.md#14-rutin)
- **Dosya yazan her thread kendi dalında zaten yalıtılı.** Worktree'yi yalnız kendi makinende koşan thread için düşün. Belge aynı klasöre iki thread yazarsa birbirini ezebileceğini söylüyor. [Bölüm 9: Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md) [11.1](../README.md#11-paralel)
- **Talimatı ilk toplu işten önce yaz, tek küçük thread ile sına.** Belgenin "ilk toplu iş" sırası bu. Sonra "önce öner, onayımı bekle" ve "aynı anda en fazla iki thread" gibi sınırları gevşet. Bu sınırlar tercihtir, zorlama değildir.
- **Her PR'a ayrı thread** belgede yok. Belge her thread'in kendi dalında çalıştığını söylüyor. Bunu bir iş akışı önerisi olarak al: tek thread'e yığılmış iki PR, birbirinin CI hatasını da miras alır.
- **Thread'ler yanlış varsayım yaptıysa görevi değil boşluğu düzelt.** Koordinatöre "her açık thread için ne istediğimi, neyi varsaydığını, neyi bulamadığını listele" de. Eksiği talimata ya da ortama bir kez yaz, sonra tek thread gönder. [13.1](../README.md#13-gozetimsiz)
- **Kullanımı proje ayarlarında oku.** **Project settings > Usage** thread ve model bazında token'ı, konuşmaya giden payı gösterir. Zorlanan sınır: tüm projelerde günde 500 yeni thread. PR izleyen boşta thread, CI hatasında ya da yorumda uyanıp planını yine tüketir. [5.4](../README.md#5-model)
- **Eski thread'i diriltme.** Bir saati (Pro ve Max) aşmış boşta thread'e gelen takip mesajı bütün konuşmayı yeniden okutur. Yeni iş için taze thread çoğu zaman ucuzdur.
- **İzin onayı thread'in içinde verilir.** Proje konuşmasına "devam et" yazmak thread'e ulaşmaz. Thread'ler uygunsa auto mode'da çalışır, repodaki izin kuralları uygulanmaz. [6.7](../README.md#6-izin)
- **Gün aşan işte commit ve push iste.** Sandbox turlar arasında durur. Devam edilemezse thread taze klondan sürer ve commit'lenmemiş değişiklik kaybolabilir.

## Hata biçimleri

Bu bölümde D01-D10 arasından uygun gerçek vaka yok. Aşağıdakiler kurgu.

**Kurgu senaryo: kural thread'e hiç gitmedi.** Gizem'in `.claude/settings.json` dosyasında commit öncesi testi koşturan bir hook ve `.env` okumasını yasaklayan bir `permissions.deny` var. Gizem üç servis için proje kurar ve altı thread başlatır. Thread'ler testsiz commit atar. Belgeye göre proje thread'i reponun hook'unu çalıştırmaz ve izin kurallarını uygulamaz. Çözüm: "commit'ten önce `make test` koş, çıktının son satırını yaz" cümlesini proje talimatına koymak. Hook'a gerçekten ihtiyacı olan görev, kendi makinesinde Remote Control ile koşar.

**Kurgu senaryo: yanlış bellek, sessiz bozulma.** Gizem iki hafta önce Claude'a "staging adresi şu" diye hatırlattı. Adres değişti, proje belleğindeki kayıt kaldı. Yeni thread'ler eski adrese istek atıyor ve her biri "erişemedim" diye dönüyor. Çözüm: **Project settings > Memory**'de kaydı düzeltmek ve bir thread ile doğrulamak.

**Kurgu senaryo: anahtar ortam değişkenine kondu.** Gizem ödeme servisi tokenını ortam değişkenine yazar. Ortamı kullanan herkes değeri okuyabilir. Doğrusu network secret: anahtar oturuma hiç girmez, proxy isteğe ekler.

## Alıştırma: iki thread'lik küçük proje

Projects Pro ya da Max planı ister. Planın yoksa 1. adımdan sonra dur ve ne göreceğini belgeden oku. GitHub'da bir deneme deposu kullan.

1. claude.ai/code'da **Projects > New project** aç. Adı ve tek satırlık hedefi yaz, deneme deposunu ekle. GitHub App kurulu değilse mesajın verdiği düğmeyle kur.
2. **Project settings > Memory** altına dört satırlık proje talimatı yaz: dal başlangıcı, PR adlandırma, bitirmeden önce hangi komutu koşacağı, eksik bir şey olursa durup söyleyeceği.
3. İki bağımsız küçük iş ver: README'ye bölüm eklemek ve bir yardımcı fonksiyona test yazmak. "Önce önerip onayımı bekle" de, öneriyi onayla.
4. Her thread'i aç, ne yaptığını oku. Her biri için PR açtır.
5. **Overview**'da hangi thread **Waiting on you** altında olduğuna bak. Birine yanıt gerekiyorsa thread'in kendi kutusundan yanıtla.
6. **Project settings > Usage** sekmesini aç.

**Bitti sayılması için:** her thread'in PR bağlantısı, **Waiting on you** grubunda gördüğün (ya da boş olduğunu gördüğün) thread'in adı ve yanıtın, **Usage** ekranından iki thread ile koordinatörün token payı yan yana yazılmış üç satır.

## Bağlantılar

Kontrol listesinin Projects bölümü: [20.1](../README.md#20-projects) [20.2](../README.md#20-projects) [20.3](../README.md#20-projects) [20.4](../README.md#20-projects) [20.5](../README.md#20-projects) [20.6](../README.md#20-projects) [20.7](../README.md#20-projects). İlgili diğer maddeler: [11.1](../README.md#11-paralel) [11.5](../README.md#11-paralel) [13.1](../README.md#13-gozetimsiz) [14.1](../README.md#14-rutin) [5.4](../README.md#5-model) [6.7](../README.md#6-izin) [9.5](../README.md#9-yeniden) [9.6](../README.md#9-yeniden). Ekler: [Sorun giderme](../ekler/sorun-giderme.md), [Terimler sözlüğü](../ekler/sozluk.md), [Komutlar ve kısayollar](../ekler/komutlar.md). Önceki bölümler: [Bölüm 9: Paralel işler: bağımsızlığı ölçmek](09-paralel-isler.md), [Bölüm 10: Gözetimsiz iş: sen yokken çalışan sistem](10-gozetimsiz-is.md), [Bölüm 11: Ekip ölçeği: ortak ayar, dağıtım ve güven](11-ekip-olcegi.md).

---

[← Bölüm 13](13-bitirme-projesi.md) · [İçindekiler](README.md) · [Bölüm 15 →](15-claude-design.md)

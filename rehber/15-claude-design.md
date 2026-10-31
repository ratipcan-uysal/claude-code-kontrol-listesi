# 15. Arayüz tasarımı: Claude Design ve tahtalar

_Uzman · Belge kontrolü: 29 Ekim 2026_

Model yön verilmezse varsayılan stile döner, bu yüzden tasarımı tarif etmek yerine karşılaştırılabilir yönler çizdirip seçersin. Claude Design, tasarım skill'leri ve tasarım sistemi arasında seçim, yönlendirme ve ekran görüntüsüyle doğrulama.

## Zihinsel model: tarif etme, karşılaştır

Tasarımda Claude'a bir ekranı sözle tarif edersin, o da onu çizer. Sorun şurada: sözle tarif edilen tasarım senin kafanda bir şey, modelin elinde başka bir şey olur. Yön vermezsen model birkaç varsayılan stile döner. Anthropic'in Opus 5.5 rehberi bunu açıkça yazar ve "jenerik görünmesin" gibi genel bir talimatın çoğunlukla bir varsayılanı ötekiyle değiştirdiğini söyler. Rehberin önerisi istemediğin kalıpları adıyla saymaktır.

Bu yüzden tasarım işinde üç alışkanlık edin:

- **Anlatma, çizdir.** Bir yönü paragrafla tarif etmek yerine karşılaştırılabilir 2-3 yönü görsel olarak iste ve görsele bakarak seç. [16.2](../README.md#16-tasarim)
- **Kalıpları adla.** Sevmediğin şeyleri tek tek yaz. Claude'un yerine ne seçtiğine bak, o da sevmediğin bir şeyse listeye ekle. [16.5](../README.md#16-tasarim)
- **Tasarım dilini bir kez yaz.** Renk, tipografi ve boşluk kuralları bir dosyada ya da bir design system'de dursun. Her turda sohbetle yeniden anlatırsan kayar. [16.4](../README.md#16-tasarim)

Bunlar sonucun nasıl iyileşeceğini söyler. Önce hangi aracı seçeceğine karar vermen gerekir.

## Hangi araç ne işe yarar

Belgede tasarımla ilgili birkaç ayrı parça var. Karıştırılmaları kolay.

| Araç | Ne üretir | Ne zaman |
|---|---|---|
| Claude Design | Düzenlenebilir bir tuval: sohbetin yanında canlı tasarım, satır içi yorum, tuvalde doğrudan düzenleme | Ekranı, akışı ya da prototipi görsel olarak keşfedeceksen |
| `/design` skill'i | Claude Code içinden aynı iş: tek tuval üzerinde artboard'lar, Claude Design artifact'i olarak yayınlanır | Terminalden çıkmadan UI seçenekleri çizdirmek istediğinde |
| Artifact (genel) | Oturumun ürettiği canlı bir sayfa | Seçenekleri yan yana göstermek, bir değişikliği bağlamıyla paylaşmak |
| `/slides` | Claude Slides sunumu | Sunum gerekiyorsa. Arayüz tasarımı için değil |
| `/dataviz` | Grafik ve pano için tasarım rehberi | Veri görselleştirirken: grafik biçimi, renk, erişilebilirlik |
| `/design-sync` | Repondaki React design system'ini Claude Design'a yükler | Tasarımların gerçek bileşenlerinle çıkmasını istediğinde |

`/design` belgeye göre ekranlar, akışlar, açılış sayfaları ve posterler için çalışır. Artboard'ları masaüstü tarayıcıda düzenlersin, düzenlemeler kendiliğinden kaydolur ve her artboard'ı PNG ya da PDF olarak dışa aktarırsın. Seçtiğin artboard'ı uygulatmak için Claude'a hangisini istediğini söylersin. Yetenek, belgede Pro, Max, Team ve Enterprise için araştırma önizlemesi olarak duyuruldu. Komut sayfası `v2.1.265` ve üstünü, artifact'lerin açık olduğu bir oturumu ve hesapta Design şablonunun açık olmasını şart koşar. Kurum şablonu kapattıysa `/design` tasarım çizmez. Amazon Bedrock, Google Cloud ve Microsoft Foundry üzerinde artifact yoktur, komut da yoktur. Duyuru sayfası daha düşük bir sürüm (`v2.1.234`) yazar. Güvenilir olan komut sayfasıdır, o yüzden yerel sürümünü `claude --version` ile bak. [Komutlar ve kısayollar](../ekler/komutlar.md) sayfasında komutların kısa hâli var.

`/design consent` Claude'a Claude Design erişimi verir, `/design revoke` geri alır. Claude senden `/design consent` yazmanı isterse bunu Claude Code komut satırına kendin yaz.

Bir şey daha: standalone Claude Design sitesi (claude.ai/design) 14 Aralık 2026'da kapanıyor. Claude Design artık Claude'un içinde, bir artifact şablonu olarak yaşıyor. Eski sitede kalan design system'leri taşımak sana düşer.

## Karar kuralları

**Keşif için Claude Design ya da `/design`, kod için Claude Code.** Yön arıyorsan tuval ve artboard'lar doğru yerdir. Sonra seçileni kod olarak uygulatırsın. Support belgesi Claude Design'dan Claude Code'a devri de anlatır: tasarımı yerel kodlama agent'ına ya da web üzerindeki Claude Code'a gönderirsin. Claude Code ekran görüntüsünden değil var olan işten devam eder.

**Tasarım dilini yaz, her seferinde anlatma.** Artifact belgesi bunun en basit yolunu verir: renk, tipografi ve boşluk değerlerini projenin CLAUDE.md dosyasına ya da bir tema dosyasına yaz. Öncelik sırası da açık: senin prompt'un, sonra design system'in, sonra Claude'un kendi seçimleri. Gerçek bileşenler gerekiyorsa `/design-sync` kullan. Bu skill repondaki React design system'ini dönüştürüp yükler. İlk senkron, büyük bir repoda birkaç saat sürebilir. Support belgesi senkronun kaynak kadar iyi olacağını da söyler: dağınık bir kod tabanı çıktıda görünür. [16.4](../README.md#16-tasarim)

**Referansın hangi yönünü istediğini söyle.** "Bunun gibi yap" demek renk mi, düzen mi, ton mu olduğunu bırakır. Screenshot yükle ve şunu yaz: "Bundan yalnız bilgi hiyerarşisini al, rengini ve tipografisini alma." Kaynaklı ilham araştırması ayrı bir adım olarak [16.1](../README.md#16-tasarim) maddesinde.

**Gerçek içerikle çizdir.** Placeholder metinle her tasarım iyi görünür. Gerçek başlığı, gerçek rakamı, gerçek listeyi ver. Uç durumları da iste: iki satıra taşan uzun Türkçe başlık, boş durum, hata durumu, 390 piksel genişlik. Support belgesi de duyarlılığı erken düşünmeyi öneriyor.

**Bir yön yetmez.** Support belgesi "2-3 alternatif düzen göster" ve "başka bir yaklaşımı dene" demeyi örnekler. Yeni yönü denemeden önce eldekini kaydet: belgeye göre Claude Design'da henüz sürüm geçmişi yok. "Şu ana kadar olanı kaydet ve tamamen farklı bir yaklaşım dene" demek bu yüzden işe yarar.

**Doğru kanalı seç.** Support belgesi şunu söyler: yapısal değişiklik ve yeni bölüm için sohbet, tek bileşenlik düzeltme için satır içi yorum, hızlı görsel ince ayar için tuvalde doğrudan düzenleme. Yorumların bazen kaybolduğu bilinen bir sorun, o zaman geri bildirimi sohbete yapıştır.

**Beğenmediğinde yönü değiştir.** Aynı yönü rötuşlamak aynı fikrin varyasyonunu üretir. "Bu yönden çık, kart dizisi yerine tek odak alanı dene" gibi neyin çalışmadığını ve ne yapılacağını söyle. [16.3](../README.md#16-tasarim)

## Doğrulama

Tasarımı gözle sınamak zorundasın, çünkü metin raporu "güzel oldu" diyebilir. Bak:

- Ekran görüntüsüyle, tam ekran ve alt alanlar dahil. Sayfanın altını kimsenin açmadığı bir yer sayma.
- Dar ekranda (390 piksel) ve koyu temada.
- Önce/sonra yan yana. Değişikliği hatırlamaya çalışma. [12.5](../README.md#12-dogrulama)
- Uzun metinle ve boş veriyle.
- Koda aktarırken. Tasarım ile uygulanmış sayfa aynı değildir. Aktarıldıktan sonra kodu çalıştırıp aynı ekran görüntüsünü al ve tasarımın yanına koy. Bu belgede yazılı bir adım değil, iş akışı önerisi.

Support belgesi Claude'a kontrast oranlarını, bilgi hiyerarşisini ve erişilebilirliği inceletmeyi de öneriyor. Bunu gözle bakmanın yerine değil, yanına koy.

## Hata biçimleri

**Yazarın tasarım oturumlarından: alt alanlar atlandı.** Yazar tasarım önerisini anlatılmış değil çizilmiş ister. Yine de çizilen ekranlarda alt alanların eksik olduğunu 7 kez yazmak zorunda kaldı ("alttaki alanları atlamışsın"). Bu yüzden kural oldu: her yön tam ekran ve alt alanlar dahil gösterilir.

**Yazarın tasarım oturumlarından: aynı yönün rötuşu.** "Beğenmedim" geldiğinde aynı yönü düzeltmeye devam etmek 25 kez tekrarlanan bir döngü oldu. Kural: beğenilmeyen yön rötuşlanmaz, farklı bir yön önerilir.

Bu iki sayı yazarın kendi oturumlarından. Resmî bir ölçüm değil, ama yönün değişmesi gerektiğini söyleyen belgedeki tavsiyeyle örtüşüyor.

**Kurgu senaryo: jenerik görünmesin.** Pelin bir alışkanlık uygulamasının ana ekranını ister ve "modern ve jenerik olmayan" yazar. Claude krem arka plan ve italik vurgulu başlık getirir. Pelin "daha az krem" der, Claude bu kez koyu mor bir gradient seçer. İkisi de yeni bir varsayılandır. Pelin sonunda sevmediği kalıpları tek tek yazar: krem zemin, italik vurgu, gradient, hap biçimli düğme. Dördüncü istekte Claude yalnız renkleri değil, ekranın düzenini de değiştirir.

## Alıştırma: üç yön, bir seçim

Bunu bir kod değiştirmeyen ekran üzerinde yap. Gerçek bir ekranını al (ör. bir ayarlar ekranı) ve gerçek içeriğini hazırla.

1. `/design` ile (ya da Claude Design'da) aynı ekran için üç farklı yön iste. Her yön tam ekran ve alt alanlar dahil olsun. Prompt'a gerçek başlıkları ve en az bir uzun Türkçe başlığı koy.
2. Üç yönün görüntüsünü kaydet. Birini seç.
3. Seçmediğin iki yönde ve seçtiğinde sevmediğin her kalıbı adıyla bir **red listesi**ne yaz (arka plan, vurgu biçimi, düğme biçimi, etiketler).
4. Listeyi prompt'a koy ve seçilen yönü yeniden iste. Claude'un yerine seçtiği şeye bak, sevmediysen listeye ekle.
5. Sonucu 390 piksel genişlikte ve gerçek içerikle aç. Boş durumu da iste.
6. Eski ve yeni hâli yan yana koy.

**Bitti sayılması için:** üç yönün görüntüsü, yazılı red listesi, son tasarımın önce/sonra görüntüsü ve 390 piksel görüntüsü. Eksik biri varsa alıştırma bitmedi.

## Bağlantılar

Kontrol listesi: [16.1](../README.md#16-tasarim) [16.2](../README.md#16-tasarim) [16.3](../README.md#16-tasarim) [16.4](../README.md#16-tasarim) [16.5](../README.md#16-tasarim) [12.5](../README.md#12-dogrulama). İş tarifi için [Bölüm 2: İş vermek: bitiş çizgisini çizmek](02-is-vermek.md). Hareketli görüntü almak için [Bölüm 16: Hareketli görüntü: ajan videoyu izleyemez](16-hareketli-goruntu.md). Ekler: [İpuçları ve püf noktaları](../ekler/ipuclari.md), [Komutlar ve kısayollar](../ekler/komutlar.md).

Kontrol listesindeki karşılığı: [16.6](../README.md#16-tasarim).

---

[← Bölüm 14](14-projects.md) · [İçindekiler](README.md) · [Bölüm 16 →](16-hareketli-goruntu.md)

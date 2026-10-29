## Zihinsel model: her hata bir katmanın adresini taşır

Claude Code yanlış bir şey yaptığında ilk refleks "daha açık yazayım" olur. Çoğu zaman yanlış çözümdür, çünkü hatanın hangi katmandan geldiğini bilmeden düzeltme yazarsın. {{bolum:1}} üç parçayı anlatmıştı: model karar verir, araçlar iş yapar, harness bunları sarar. Sistemi iyileştirmek bu üç parçaya sorulan tek bir soruyla başlar: bu başarısızlık hangisinden geldi?

| Belirti | Katman | Düzeltme nerede |
|---|---|---|
| Claude kuralı bilmiyordu ya da unuttu | Bağlam | CLAUDE.md, rule, bellek, ya da kuralı kesin katmana taşı |
| Claude kuralı gördü ama kötü bir seçim yaptı | Model kararı | Daha iyi örnek, daha dar görev, daha güçlü model, doğrulama adımı |
| Komut çalışmadı, izin istedi, hook engelledi, dosya yüklenmedi | Harness | Ayar, izin listesi, hook, yükleme yolu |

Ayrım pratik sonuç verir. Bağlam hatasında kuralı yazarsın, ama o kural tek yerde ve doğru katmanda durur. Model kararı hatasında kural eklemek işe yaramaz, çünkü Claude kuralı zaten biliyordu. Harness hatasında hiçbir metin yardım etmez, ayarı düzeltirsin. Üçünü karıştıran ekip CLAUDE.md'sini şişirir ve sorun yine de geri gelir. Belge de aynı yönde uyarır: uzun dosya hem bağlam harcar hem uyumu düşürür, çelişen iki talimattan Claude birini rastgele seçebilir.

## Dersi doğru katmana yaz

Bir ders öğrendiğinde dosyayı seçmeden önce şunu sor: bu cümle nerede doğru olmaktan çıkıyor?

- **Her projede doğruysa** kullanıcı düzeyine yaz: `~/.claude/CLAUDE.md`. Makine ve araç gerçekleri buraya gider: izin motoru, kabuk, zamanlayıcı davranışı.
- **Yalnız bu koda aitse** proje CLAUDE.md'sine yaz. Mimari, kıyas kuralı, sürüm sabitlemesi buradadır.
- **Yalnız bu depo ile bu makinenin kesişimiyse** `CLAUDE.local.md`'ye yaz ve gitignore'a ekle. Yerel yol, sanal ortam konumu gibi şeyler.
- **Tarihli ölçüm ve kanıt ise** ayrı bir kanıt dosyasına yaz. Kuralın kendisi kısa kalır, ölçümün gövdesi orada durur. [[18.1]] [[18.4]]

Yanlış katman sessiz bir kayıptır. Makine gerçeğini proje dosyasına yazarsan diğer projeler onu hiç görmez. Proje gerçeğini kullanıcı dosyasına yazarsan başka depolarda gürültü olur.

## Karar kuralları

**Üçüncü tekrar kuraldır.** Aynı düzeltmeyi ilk kez yapman tesadüf, ikincisi bir işaret, üçüncüsü kuraldır. Düzeltmeleri say. Üçe ulaşınca kuralı yaz, ama önce katmanı seç: istisnası olmayan şey hook ya da deny kuralına gider, tercih CLAUDE.md'ye. Belgenin bölüm {{bolum:5}}'te geçen tetik listesi aynı mantıkla çalışır: "Claude aynı şeyi iki kez yanlış yaptı" CLAUDE.md'ye girer. [[18.3]]

**Kuralı kısa yaz, kanıtı ayrı tut.** Bağlamda yer alan her satır her oturumda bedel öder. Kuralın tek cümlesi CLAUDE.md'de, ölçümün gövdesi ayrı bir dosyada olsun. Kuralın sonuna "kanıt: kanit.md, başlık" gibi bir atıf koy. Böylece Claude gerektiğinde açar, her oturumda taşımaz. [[18.4]]

**Bekleyeni hemen dosyaya yaz.** "Sonra", "unutma", "şimdilik bırak" denen şey oturum içi hafızada kalırsa devirde kaybolur. Proje kökünde bir bekleyenler dosyası tut, CLAUDE.md'de buna dair tek kural olsun. "Neler kaldı?" sorusunun cevabı dosyadan gelmeli. [[18.2]]

**Bakımı ritme bağla.** Küçük ve düzenli bakım büyük temizlikten ucuzdur.

| Ritim | İş | Araç |
|---|---|---|
| Haftalık | Kullanımı ve bekleyenleri gözden geçir | `/usage`, bekleyenler dosyası |
| Aylık | CLAUDE.md'leri buda, izin listesi ve hook testlerini yokla | `/doctor prompt-audit`, `/fewer-permission-prompts` |
| Çeyreklik | Kendi kullanım analizini çıkar, önceki çeyrekle karşılaştır | `/insights`, oturum kayıtları |

Aylık budamada dikkat et: seyrek ama kritik bir kuralı yalnız geçen ay tetiklenmedi diye silme. Dosyanın küçük olması tek başına başarı ölçütü değildir. [[19.1]] [[19.3]] [[19.4]] [[19.5]]

**Araçları ne için kullandığını bil.** `/usage` kullanım ve limit durumunu gösterir. Pro, Max, Team ve Enterprise planlarında neyin limitini tükettiğinin dökümünü ve öneriler de sunar, önerileri uygulatan `f` kısayolu v2.1.305 ve sonrasını ister. `/insights` makinendeki son oturumları tarar ve neyle uğraştığını, nerede sürtünme yaşadığını gösteren bir HTML rapor yazar. Tek çalıştırmada henüz görmediği en çok 200 oturumu analiz eder. `/doctor` kurulumun, ayarların, eklentilerin ve CLAUDE.md dosyalarının sağlık kontrolünü yapar, düzeltmeleri sen onaylayınca uygular. `/doctor prompt-audit` (v2.1.283 ve sonrası) talimat dosyalarını tarar: eski modeller için yazılmış talimatları, var olmayan dosya ya da komut referanslarını ve birbiriyle çelişen dosyaları arar. Önerileri bir rapor olarak verir ve sen istemeden hiçbir dosyayı değiştirmez. [[19.1]] [[19.5]]

**Yeni model çıkınca talimatları yeniden sına.** Belgede "model çıkınca şunu yap" diye bir döngü yok, bu bir iş akışı önerisi. Gerekçesi şu: eski modeller için yazdığın vurgu, ek hatırlatma ya da ayrıntılı adım listesi yeni modelde gereksiz ya da zararlı olabilir. Bölüm {{bolum:5}}'te anlatıldığı gibi vurgu yığmak güncel modellerde kuralı fazla uygulatabilir. Önce `/doctor prompt-audit` ile adayları çıkar, sonra aşağıdaki karşılaştırmayla budamanın bir şeyi bozup bozmadığına bak.

**Modeli aynı görevle karşılaştır.** Genel izlenim ve tek bir başarılı cevap model seçimini kanıtlamaz. Kendi işinden temsilî iki üç görev seç. Her birini iki ayarla aynı prompt ve aynı başlangıç durumuyla headless koştur. Sonucu, tur sayısını ve maliyeti kaydet, ölçütü önceden belirle. Belgede hazır bir karşılaştırma tarifi yok, bu parçalarla kurarsın. [[5.6]]

```
for m in sonnet opus; do
  claude -p "$(cat gorev.md)" --model $m --output-format json \
    --no-session-persistence > sonuc-$m.json
done
```

**Sürüm ve ortam farkını kaydet.** Bir karşılaştırmanın değeri, hangi sürümde yapıldığına bağlı. Raporuna `claude --version` çıktısını, platformu ve sağlayıcıyı yaz. Belgede olan özellik eski sürümde ya da başka sağlayıcıda bulunmayabilir. Bu bölümdeki iki örnek: `/doctor prompt-audit` v2.1.283, `/usage` içindeki `f` kısayolu v2.1.305 ister. [[19.6]]

## Hata biçimleri

**Gerçek vaka: dersin katmanı (D09).** {{ek:deneyimler}} sayfasındaki D09'da çok günlük bir yazı serisinin kaynakları oturumun geçici dizinindeydi ve dizin bir akşam toptan silindi. Vakanın dersi ("birden çok gün sürecek işin kaynağı geçici dizinde tutulmaz") bir makine gerçeğidir, bu yüzden bu rehberin ölçütüne göre kullanıcı düzeyi dosyaya ait. Aynı cümle bir proje CLAUDE.md'sine yazılsaydı başka projeler aynı kayıpla karşılaşırdı. Ölçümün gövdesi (silme tarihi, neyin geri kurulabildiği) kısa kuralın dışında, kanıt sayfasında durur. Sınırı da vaka yazıyor: silmenin nedeni ölçülmedi.

**Gerçek vaka: eski rapor canlı sistem sanıldı (D10).** On gün önceki bir denetim "uygulama yalnız bir ülkede satışta" diyordu. Cümle kullanıcının yapıştırdığı notta da vardı ve sayfaya bakılmadan doğru kabul edildi. Yönetim panelinde uygulama 175 ülkede satıştaydı. Bu rehber olayı bir model kararı hatası olarak sınıflar: Claude'a eksik bilgi verilmemişti, eski rapora güvenmeyi seçti. Bu yüzden düzeltme uzun bir yasak listesi değil, kısa bir kural olur: değişebilen bir durumu yazmadan önce kaynağın kendisine bak, kullanıcının yapıştırdığı not da bir rapordur. Ayırıcı kanıt kaynağın o anki değeri ve okuma tarihidir.

**Kurgu senaryo: sönmeyen CLAUDE.md.** Deniz'in proje dosyası altı ayda 380 satıra çıkar. Her hatadan sonra yeni bir kural eklenir, hiçbiri silinmez. Bir gün iki kural çelişir, Claude birini seçer ve Deniz sebebini anlayamaz. `/doctor prompt-audit` çelişkiyi ve var olmayan iki dosyaya yapılan atıfı bulur. Deniz uzun prosedürleri skill'e taşır, 140 satır kalır.

## Alıştırma: önce ve sonra

Bunu kendi proje talimatlarının bir kopyasında yap. Gerçek dosyayı karşılaştırma bitene dek değiştirme.

1. Üç temsilî iş seç: biri küçük bir düzeltme, biri araştırma, biri çok adımlı bir değişiklik. Her birini bir `gorev-N.md` dosyasına yaz. Başarı ölçütünü de oraya yaz.
2. Mevcut talimatlarla her işi headless koştur. Sonucu, tur sayısını ve maliyeti kaydet.
3. `/doctor prompt-audit` çalıştır. Önerilerden en az üçünü uygula: eski vurgular, çelişkiler, var olmayan referanslar. Her silinen satırı bir cümleyle gerekçelendir.
4. Üç işi budanmış talimatlarla aynı koşullarda yeniden koştur.
5. Sonuçları ölçütüne göre karşılaştır.

**Bitti sayılması için:** üç satırlık bir önce/sonra tablosu (iş, sonuç, tur, maliyet), silinen satırların listesi ve `claude --version` çıktısı. Altına tek cümle yaz: budama hangi katmandaki hatayı çözdü, hangisini çözmedi.

## Bağlantılar

Kontrol listesi: [[18.1]] [[18.2]] [[18.3]] [[18.4]] [[19.1]] [[19.3]] [[19.4]] [[19.5]] [[19.6]] [[5.6]]. Önceki bölüm: {{bolum:11}}. Ekler: {{ek:komutlar}}, {{ek:deneyimler}}, {{ek:sorun-giderme}}.

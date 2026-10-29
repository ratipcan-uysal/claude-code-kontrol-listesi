# Ek sayfaların tek kaynağı. Biçim ve [[3.1]] madde bağlantısı için yap.py'deki EKLER bölümüne bak.
EK_TARIH = "29 Ekim 2026"

DENEYIMLER = r"""
Bu sayfadaki on vaka, bu listenin yazarının kendi makinesinde tuttuğu tarihli ölçüm defterinden alındı. Proje adları, yollar ve kişisel veriler çıkarıldı. Her vaka bir gözlemdir: o makinede, o sürümde, o koşulda görüldü. Genel kural gibi okuma, kendi ortamında aynı belirtiyi gördüğünde ilk bakılacak yer olarak kullan.

Vakaların ortak dersi şu: en pahalı hatalar bir şeyin kırılmasından değil, bir şeyin **hiçbir şeye bakmadan başarılı görünmesinden** çıkıyor.

## D01 · Gözetimsiz oturumda izin modu sessizce değişti

**Gözlenen:** Zamanlanmış oturumların izinsiz ilerlemesi için `bypassPermissions` modu ayarlanmıştı. Bir projenin 43 oturum kaydındaki 345 mod değeri tarandı. Bu mod hiç görünmüyordu. Mod ilk kullanımda bir onay penceresi istiyor, zamanlanmış oturum pencereyi gösteremediği için oturum hata vermeden varsayılan moda düşüyordu.

**Ders:** Ayarladığın mod ile oturumun gerçekte açıldığı mod ayrı şeylerdir. Gözetimsiz koşumu ayakta tutan şey projenin kendi izin listesiydi.

**Ayırıcı kanıt:** Oturum kaydındaki etkin mod değeri. Ayar dosyasındaki değer kanıt değildir.

**Sınır:** 29 Ağustos 2026 gözlemi. Davranış sürüme ve yönetilen politikaya göre değişebilir. İlgili maddeler: [[6.7]], [[13.2]].

## D02 · Hiç test koşmayan filtre yeşil döndü

**Gözlenen:** Test komutuna süitin okunur adı filtre olarak verildi. Eşleşen test olmadı, çıktı "başarılı" dedi. Aynı gün iki kez rapora "test geçiyor" diye girmek üzereydi. Aynı gün iki benzer yeşil daha görüldü: hiçbir dosya bulamadığı için geçen lint ve dar pencere yüzünden körleşen lint.

**Ders:** Durum satırını değil sayıyı oku. Sıfır test koşmak geçmek değildir.

**Ayırıcı kanıt:** Çıktıdaki koşulan test sayısı. Filtreyi tip ya da fonksiyon adıyla verince sayı sıfırdan çıktı.

**Sınır:** Belirli bir test aracının filtre davranışı. Başka araçlarda ilke aynı, sözdizimi farklı. İlgili maddeler: [[12.1]], [[12.2]].

## D03 · Arka plana atılan iş, tur bitince iz bırakmadan öldü

**Gözlenen:** Zamanlanmış bir görev uzun bir veri çekimini arka planda başlattı ve turu "bekliyorum" diye kapattı. Komut başlamadan önce rastgele bekleme yapıyordu. Oturum kapanınca süreç öldü, görev çıktısı dizinle birlikte silindi. 83 dakika boyunca ağa tek istek gitmedi ve geriye tek satır kanıt kalmadı.

**Ders:** Gözetimsiz oturumda uzun işi arka plana atıp turu kapatma. Log'u oturumdan bağımsız bir yola yaz. Aynı iş ön planda ve kalıcı log'la 12 dakikada bitti.

**Ayırıcı kanıt:** Normal komutun yarım çıktısı log'da kalır. Önce bekleyen komut ise "hiç başlamadı" ile "öldü" arasında fark bırakmaz.

**Sınır:** 1 Eylül 2026, tek bir masaüstü kurulumu. İlgili maddeler: [[13.3]], [[13.4]].

## D04 · "Ucuz" kontrol yük altında 120 kat uzadı

**Gözlenen:** Görev dosyası bir test komutunu "yaklaşık 2,5 saniye" diye tarif ediyordu. Bir nöbet koşumunda aynı komut 300 saniyelik ön plan sınırını aştı ve arka plana düştü. Testler sonunda geçti. Makine yükü o dakikada 68'e çıkmıştı, eşzamanlı oturumlar yüzünden.

**Ders:** "Ucuz" bir ölçüm değil varsayımdır. Kontrol arka plana düştüyse turu kapatma, bitmesini bekle ve çıkış satırını oku. Yoksa D03 tekrarlanır ve dışarıdaki nöbetçi makineyi ölü sanıp yanlış alarm verir.

**Ayırıcı kanıt:** `uptime` yük ortalamaları. Bir dakikalık değer on beş dakikalığın birkaç katıysa yük o pencerede fırlamıştır.

**Sınır:** 2 Eylül 2026. İlgili maddeler: [[11.4]], [[13.4]].

## D05 · Uyku engelleyici, bataryada uykuyu engellemedi

**Gözlenen:** Gece koşumu bir uyku engelleyiciyle sarılmıştı. Makine prizde değildi. 19 saatte süreç 1,2 saniye işlemci zamanı kullandı. Sistem günlüğünde aynı gece 257 uykuya giriş kaydı vardı. Çıktı dosyası 19 saat boyunca boş kaldı. Makine prize takılınca aynı koşum 20 dakikada bitti.

**Ders:** Batarya ve düşük şarj koşumu öldürmez, dondurur. Donma sessizdir. Gece koşumunun ön koşulu makinenin şarjda olmasıdır.

**Ayırıcı kanıt:** Geçen süreye değil işlemci süresine bak. Oran sıfıra yakınsa süreç uyuyor demektir.

**Sınır:** macOS, 5 Eylül 2026. İlgili madde: [[13.2]].

## D06 · Başka oturumun commit'i benim değişikliklerimi götürdü

**Gözlenen:** Değişiklikler stage edildi, ardından üç dakikalık izole derleme yapıldı. Bu arada aynı repoda çalışan başka bir oturum kendi raporunu commit'ledi. Commit index'in tamamını aldı. Dört dosya başka bir mesajın altına girdi, benim commit'im "değişiklik yok" diye boş döndü.

**Ders:** Git index'i aynı checkout'taki bütün oturumlar arasında ortaktır. Stage ile commit'i tek komutta yap. Arada derleme gerekiyorsa index'i değil geçici bir kopyayı ya da ayrı worktree'yi kullan.

**Ayırıcı kanıt:** `git log --stat` ile dosyaların hangi commit'e girdiğine bak.

**Sınır:** 28 Eylül 2026. İçerik doğruydu, yalnız commit mesajı yanlıştı. Paylaşılan dalda geçmiş yeniden yazılmadı. İlgili maddeler: [[11.1]], [[11.2]].

## D07 · Proje dışı import headless koşumda yüklenmedi

**Gözlenen:** Ortak kurallar ayrı bir dosyaya taşındı ve dört projenin CLAUDE.md'sine `@~/...` import'u eklendi. `claude -p` ile koşulan oturum dosyanın içeriğini görmedi, yalnız import satırını gördü. Proje dışı import onayı proje yolu başına tutuluyordu. Her worktree ayrı kayıt sayılıyordu, headless koşum onay penceresini hiç göstermiyordu. Symlink de çözmedi.

**Ders:** Her oturuma girmesi gereken proje dışı bilgiyi import'a bırakma. SessionStart hook'u aynı içeriği her koşumda bağlama koydu ve model kuralı kelimesi kelimesine aktardı.

**Ayırıcı kanıt:** Dosya okuma araçları kapalı bir headless oturumda "bu kural ne diyor?" diye sor.

**Sınır:** 15 Ekim 2026. İlgili maddeler: [[1.5]], [[8.1]].

## D08 · Dört paralel oturum makineyi kilitledi, metin kuralı yetmedi

**Gözlenen:** Dört alt oturum ayrı worktree'lerde aynı anda derleme ve test koştu. Başka projelerin derlemeleri de sürüyordu. Yük ortalaması 720'ye çıktı, sakin makinede 4'tü. Oturumlara "ağır komutu kilitle sar" diye metin talimatı verildi. Bir oturum kilitsiz başlattığı derlemeyi sonradan durdurmak zorunda kaldı.

**Ders:** Metin kuralı yeni oturuma ve başka projeye ulaşmaz. Çalışan yol iki parçalıydı: ağır komutları iki yuvalı kilitle koşturan bir sarmalayıcı ve sırasız ağır komutu reddeden bir PreToolUse hook'u.

**Ayırıcı kanıt:** Hook 16 vakalık bir testle sınandı, sıfır yanlış verdi. Hafif komut istisnası bozulunca iki yanlış verdi, yani test gerçekten bakıyordu.

**Sınır:** 26 Ekim 2026. Tek yuva fazla dar çıktı: uzun bir cihaz testi kilidi 30 dakika tuttu, diğerleri boşta bekledi. İlgili maddeler: [[8.4]], [[11.4]], [[11.6]].

## D09 · Geçici dizin toptan silindi, çok günlük iş gitti

**Gözlenen:** Bir yazı serisinin kaynakları, görselleri ve durum dosyası oturumun geçici çalışma dizinindeydi. Dizin ağacı bir akşam toptan silindi. Metinler alt ajan kayıtlarındaki dosya okuma sonuçlarından geri kuruldu. Görsellerin yerel kopyası geri gelmedi.

**Ders:** Birden çok gün sürecek işin kaynağı geçici dizinde tutulmaz. Proje dizinine ya da kalıcı bir yola yaz. Geçici dizin yalnız o turun ara çıktısı içindir.

**Ayırıcı kanıt:** Yeniden yaratılan dizinlerin hepsi aynı dakikanın zaman damgasını taşıyordu.

**Sınır:** 27 Ekim 2026. Silmenin nedeni ölçülmedi. İlgili maddeler: [[13.3]], [[18.2]].

## D10 · Eski rapor, canlı sistemin yerine okundu

**Gözlenen:** On gün önceki bir denetim "uygulama yalnız bir ülkede satışta" diyordu. Cümle aynı gün iki kez tekrarlandı, biri kullanıcının yapıştırdığı notta. Sayfaya bakılmadan doğru kabul edildi ve buna göre bir karar önerildi. Yönetim panelinde uygulama 175 ülkede satıştaydı. Aynı oturumda ikinci bir örnek: bir sürüm notundaki "hepsinin görseli var" iddiası yeni sürümde 11 eksik görselle çürüdü.

**Ders:** Mağaza ayarı, sayı, kapsam gibi değişebilen bir durumu eski rapordan alma. Kullanıcının yapıştırdığı not da bir rapordur. Yazmadan ya da öneri yapmadan önce kaynağın kendisine bak.

**Ayırıcı kanıt:** Kaynağın şu anki değeri ve okuma tarihi.

**Sınır:** 28 Ekim 2026. İlgili maddeler: [[12.3]], [[18.4]].
"""

SOZLUK = r"""
Terimler ilk geçtiği maddede kısaca tanımlanır. Bu sayfa hepsini bir arada verir. Her satır terimin bu listede ne anlama geldiğini söyler. Ürün davranışının tamamı için ilgili resmî belgeye bak.

## Oturum ve bağlam

| Terim | Bu listede ne demek |
|---|---|
| Oturum | Claude ile tek bir konuşma ve onun araç geçmişi. Kapatıp açınca konuşma bağlamı sıfırlanır, dosyalar kalır. |
| Bağlam (context) | Modelin o anda görebildiği her şey: mesajlar, okunan dosyalar, araç çıktıları, yüklenen talimatlar. Sınırlıdır ve dolar. |
| Token | Modelin metni işlediği parça. Bağlam ve kullanım token'la ölçülür. Kelimeyle birebir eşleşmez. |
| Sıkıştırma (`/compact`) | Uzayan konuşmanın özetle değiştirilmesi. Yer açar, ayrıntı kaybettirebilir. |
| Checkpoint | Claude'un dosya düzenlemelerinden önce aldığı yerel geri dönüş noktası. Git'in yerini tutmaz. |
| Devir dosyası | Oturum kapanmadan önce durumun yazıldığı dosya. Yeni oturum oradan devam eder. |
| Otomatik bellek | Claude'un oturumlar arasında kendi tuttuğu notlar. Talimat dosyasından ayrıdır, eskiyebilir. |

## Talimat ve ayar

| Terim | Bu listede ne demek |
|---|---|
| CLAUDE.md | Her oturumun başında yüklenen talimat dosyası. Üç düzeyi var: kullanıcı, proje ve alt dizin. |
| `CLAUDE.local.md` | Yalnız bu makinede geçerli proje notu. Git'e girmez. |
| Kural dosyası (`.claude/rules/`) | Yalnız eşleşen dosyalara dokunulunca yüklenen talimat. |
| `settings.json` | İzin, hook, model ve ortam ayarlarının dosyası. Kullanıcı, proje, yerel ve yönetilen katmanları vardır. |
| Yönetilen politika | Kurumun yönettiği ve kullanıcının ezemediği ayar katmanı. |
| Prompt | Claude'a verilen istek metni. |
| Output style | Claude'un cevap üslubunu değiştiren hazır ya da özel ayar. |

## İzin ve güvenlik

| Terim | Bu listede ne demek |
|---|---|
| İzin modu | Claude'un araç kullanmadan önce ne zaman onay soracağını belirleyen mod. Plan modu bunlardan biridir. |
| Allow / ask / deny | İzin kuralının üç sonucu: sormadan izin ver, sor, reddet. |
| Plan modu | Claude'un yalnız okuyup plan yazdığı, dosya değiştirmediği mod. |
| Sandbox | Komutların dosya sistemi ve ağ erişimini işletim sistemi düzeyinde sınırlayan yalıtım. |
| Prompt injection | Okunan sayfa, belge ya da e-postadaki metnin kullanıcı talimatı gibi davranmaya çalışması. |

## Genişletme

| Terim | Bu listede ne demek |
|---|---|
| Hook | Belirli bir olayda (araç öncesi, araç sonrası, oturum başı gibi) otomatik çalışan betik. Modelin kararına bağlı değildir. |
| Skill | Gerektiğinde yüklenen talimat ve dosya paketi. Açıklaması her zaman bağlamdadır, gövdesi yalnız kullanılınca yüklenir. |
| Slash komutu | `/` ile başlayan komut. Bir kısmı yerleşik, bir kısmını skill ve plugin'ler ekler. |
| Alt ajan (subagent) | Kendi bağlamında çalışan ve sonucu ana oturuma özet olarak dönen yardımcı Claude. |
| MCP | Claude'u dış sistemlere (veritabanı, iş takibi, tarayıcı gibi) araç olarak bağlayan açık protokol. |
| Plugin | Skill, ajan, hook ve MCP ayarlarını tek pakette dağıtma biçimi. |
| Statusline | Terminal altında sürekli görünen, kendi betiğinle üretilen durum satırı. |

## Çalışma biçimi

| Terim | Bu listede ne demek |
|---|---|
| Headless (`claude -p`) | Etkileşimsiz koşum. İstek verilir, sonuç metin ya da JSON olarak döner, oturum biter. |
| Effort | Modelin düşünmeye ayıracağı çaba düzeyi. |
| Worktree | Aynı Git deposunun ayrı bir klasördeki ikinci çalışma kopyası. Paralel yazarları ayırır. |
| Rutin | Zamanlanmış ya da tetiklenmiş, gözetimsiz koşan Claude görevi. Bulutta ya da masaüstünde çalışır. |
| Gözetimsiz koşum | Kullanıcı başında yokken ilerleyen iş. Soru soramaz, izin bekleyemez. |
| Advisor | Zor kararda ikinci, daha güçlü bir modelin görüşünü alma özelliği. |
| Harness | Modelin çevresindeki çalışma düzeni: araçlar, izinler, bağlam yönetimi. Claude Code bir harness'tır. |
"""

KOMUTLAR = r"""
Claude Code'a üç yoldan komut verilir. Oturumun içinde `/` ile başlayan **slash komutu**, kabukta `claude` ile başlayan **CLI bayrağı** ve **klavye kısayolu**. Aynı iş çoğu zaman üçünden biriyle yapılır: geçmiş oturuma `/resume` ile oturumun içinden, `claude --resume` ile kabuktan dönülür.

Bu sayfa günlük işte fark yaratan komutları işe göre gruplar. Belgedeki komut tablosu 120 satırdan uzun, hepsi burada yok. Belge yerel CLI 2.1.284'ten yeni, bazı komutlar senin sürümünde görünmeyebilir. Emin olmak için oturumda `/help` yaz ya da `claude --version` ile sürümü gör. Kaynaklar: [komutlar](https://code.claude.com/docs/en/commands), [CLI referansı](https://code.claude.com/docs/en/cli-reference), [etkileşimli mod](https://code.claude.com/docs/en/interactive-mode).

## Slash komutları, işe göre

### Bağlam

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/context` | Bağlamın neyle dolduğunu görmek için | Talimat, araç ve mesaj payını ayrı gösterir. Tahmin yerine buna bak. [[2.2]] |
| `/compact [odak]` | Uzayan oturumda yer açmak için | Ayrıntı kaybettirir. Neyin korunacağını yaz. [[2.6]] |
| `/clear` | Konu değişince | Konuşmayı sıfırlar, dosyalara dokunmaz. [[2.3]] |
| `/btw [soru]` | Ana işi bölmeden kısa bir şey sormak için | Soru ve cevap konuşmaya eklenmez. |
| `/recap` | Uzun oturumda nerede kaldığını görmek için | Tek satırlık özet. Devir dosyasının yerini tutmaz. |

### Oturum ve geri dönüş

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/resume [ad]` | Eski bir oturuma dönmek için | `/rename` ile ad verdiysen adla bulunur. [[2.7]] |
| `/branch [ad]` | Aynı noktadan başka bir yol denemek için | Seni dala geçirir, orijinal korunur. |
| `/fork [prompt]` | Konuşmayı arka planda ikinci bir oturumda sürdürmek için | `/branch` ile aynı değil: sen burada devam edersin. |
| `/rewind` | Kodu, konuşmayı ya da ikisini geri sarmak için | Boş girdide Esc Esc ile de açılır. Yalnız Bash'le değişen dosyayı geri almaz. [[15.2]] |
| `/rename [ad]` | Oturumu sonra bulabilmek için | Ad vermezsen kendisi üretir. |
| `/export [dosya]` | Konuşmayı metin olarak saklamak için | Hassas içerik varsa paylaşmadan önce oku. |
| `/diff` | Çalışma ağacındaki değişikliği görmek için | Claude'un yaptığı düzenlemeler dahil. |

### Model, çaba ve kullanım

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/model [model]` | Modeli değiştirmek için | Seçim varsayılan olarak kaydedilir. Yalnız bu oturum için seçicide ayrı seçenek var. [[5.2]] |
| `/effort [düzey]` | Düşünme çabasını işe göre ayarlamak için | Düzeyler modele bağlı. [[5.3]] |
| `/fast` | Hızlı modu açıp kapatmak için | Model kataloğuna ve hesaba bağlı. |
| `/advisor` | Zor kararda ikinci bir modelin görüşü için | [[5.5]] |
| `/usage` | Oturum maliyeti, plan limiti ve istatistik için | `/cost` ve `/stats` aynı komutun takma adı. [[5.4]] |

### Talimat, ayar ve izin

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/init` | Projeye ilk CLAUDE.md taslağı için | Taslağı gerçek komutlarla düzelt. [[1.2]] |
| `/memory` | Yüklenen talimat dosyalarını ve otomatik belleği görmek için | Import'un yüklenip yüklenmediğine buradan bak. [[1.5]] [[1.7]] |
| `/status` | Sürüm, model, hesap ve yüklenen ayar dosyaları için | `Setting sources` dosyaları listeler, anahtar bazında kaynak göstermez. [[1.8]] |
| `/config` | Ayar arayüzü ya da `key=value` ile ayar yazmak için | Takma adı `/settings`. Hangi katmana yazdığına dikkat et. |
| `/permissions` | allow, ask, deny kurallarını yönetmek için | [[6.1]] [[6.3]] |
| `/fewer-permission-prompts` | Geçmişten salt okunur komutlar için allow listesi önerisi | Öneriyi kabul etmeden önce tek tek oku. [[6.6]] |
| `/sandbox` | Sandbox'ı açıp kapatmak için | Yalnız desteklenen platformlarda. [[7.5]] |
| `/hooks` | Etkin hook'ları görmek için | Yalnız gösterir. Hook'un çalıştığını göstermez, onu testle sına. [[8.4]] |
| `/statusline` | Durum satırını kurmak için | [[8.3]] |
| `/doctor` | Kurulum, ayar ve eklenti sorunlarını taramak için | Claude hiç açılmıyorsa kabukta `claude doctor`. |

### Genişletme

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/skills` | Yüklü skill'leri görmek için | Açıklaması zayıf skill listede olsa da çağrılmaz. [[9.3]] |
| `/reload-skills` | Diske eklenen skill'i yeniden başlatmadan almak için | |
| `/plugin` | Plugin kurmak ve yönetmek için | [[9.6]] |
| `/mcp` | MCP sunucularının durumunu görmek, yeniden bağlamak için | Bağlı görünmek aracın çalıştığını kanıtlamaz. [[9.5]] |
| `/agents` | Alt ajan yönetimi | Yeni sürümlerde arayüz açmaz, Claude'dan istemeni ya da `.claude/agents/` dosyasını düzenlemeni söyler. |

### İnceleme ve uzun iş

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/plan [görev]` | Belirsiz büyük işte önce plan için | Shift+Tab ile de plan moduna geçilir. [[3.3]] |
| `/goal [koşul]` | Koşul sağlanana kadar Claude'un turlar boyunca sürmesi için | Koşul doğrulanabilir olmalı. [[3.1]] |
| `/code-review` | Diff'i ya da PR'ı doğruluk hataları için incelemek için | Takma adı `/review`. [[12.6]] |
| `/security-review` | Dal değişikliklerini güvenlik için incelemek için | `origin` remote gerekir. |
| `/loop [aralık] [prompt]` | Oturum açıkken bir işi tekrar tekrar koşmak için | Oturum kapanınca durur. Kalıcı iş için `/schedule`. [[14.5]] |
| `/schedule` | Bulutta zamanlanmış görev kurmak için | Bilgisayar kapalıyken de koşar. [[14.1]] |
| `/tasks` | Arka plandaki işleri görmek için | Arka plan işi bitmeden turu kapatma. [[13.4]] |

## CLI bayrakları

| Bayrak | Ne yapar | Dikkat |
|---|---|---|
| `-c`, `--continue` | Bu dizindeki son oturumu sürdürür | |
| `-r`, `--resume [ad]` | Adla ya da seçiciyle oturum sürdürür | |
| `--fork-session` | Sürdürürken yeni oturum kimliği açar | `--resume` ya da `--continue` ile. [[2.7]] |
| `-n`, `--name` | Oturuma ad verir | Sonra `--resume <ad>` ile bulunur. |
| `-p`, `--print` | Headless koşum: cevabı yazar, çıkar | Betik ve rutinlerin temeli. |
| `--output-format` | `text`, `json`, `stream-json` | Yalnız `-p` ile. [[14.6]] |
| `--json-schema` | Şemaya uyan doğrulanmış JSON | Sonuç `structured_output` alanında. Alan yoksa üretilememiştir. [[14.7]] |
| `--max-turns` | Tur sınırı, dolunca hatayla çıkar | Yerel 2.1.284 `--help` çıktısında görünmedi, kullanmadan önce dene. [[14.2]] |
| `--max-budget-usd` | Tahmini harcama sınırı | Yalnız `-p` ile. |
| `--no-session-persistence` | Oturumu diske yazmaz | Karşılaştırma koşumlarında listeyi kirletmez. |
| `--model` | Bu oturumun modeli | Yalnız başlatılan oturuma uygulanır. [[5.6]] |
| `--effort` | Bu oturumun çaba düzeyi | |
| `--permission-mode` | Başlangıç izin modu | Gözetimsiz koşumda etkin modu ayrıca doğrula. [[6.7]] |
| `--allowedTools`, `--disallowedTools` | Sormadan izinli ya da yasak araçlar | Kalıcı kural için proje ayarı daha izlenebilir. |
| `--settings` | Yalnız bu oturum için ayar dosyası ya da JSON | Öncelikte yönetilen katmanın hemen altında. [[1.8]] |
| `--add-dir` | Ek çalışma dizini | |
| `--append-system-prompt` | Sistem prompt'unun sonuna ekleme | `--system-prompt` tamamen değiştirir. |
| `--mcp-config` | MCP sunucularını JSON'dan yükler | |
| `-w`, `--worktree` | Ayrı bir git worktree'de başlatır | [[11.1]] |
| `--bare` | Hook, skill, MCP, bellek ve CLAUDE.md keşfini atlar | Sorunun yapılandırmadan gelip gelmediğini ayırmak için. |
| `--safe-mode` | Bütün özelleştirmeleri kapatarak başlatır | Sorun giderme için. |
| `claude doctor` | Oturum açmadan kurulum teşhisi | |

## Klavye kısayolları

| Kısayol | Ne yapar |
|---|---|
| `Esc` | Cevabı keser, yapılan iş korunur. İzin isteminde reddeder. |
| `Esc` `Esc` | Girdi boşsa rewind menüsünü açar. Girdi doluysa taslağı temizler. |
| `Shift+Tab` | İzin modları arasında döner. Plan modu da bu döngüde. |
| `Ctrl+C` | Çalışan işi keser. Boş girdide iki kez basınca çıkar. |
| `Ctrl+B` | Çalışan Bash komutunu ya da ajanı arka plana alır. |
| `Ctrl+O` | Transkript görünümü: araç çağrılarının ayrıntısı. |
| `Ctrl+R` | Girdi geçmişinde geriye doğru arar. |
| `Ctrl+T` | Claude'un görev listesini gösterir ya da gizler. |
| `Ctrl+G` | Girdiyi metin editöründe düzenler. Uzun prompt için. |
| `Ctrl+S` | Girdiyi kenara koyar. Boş girdide geri getirir. |
| `Ctrl+V` | Panodan görsel yapıştırır. iTerm2'de `Cmd+V`. |
| `Option+P` / `Alt+P` | Girdiyi silmeden model değiştirir. |
| `\` sonra `Enter`, ya da `Ctrl+J` | Çok satırlı girdi. Her terminalde çalışır. |
| `!` ile başlamak | Komutu doğrudan kabukta çalıştırır, çıktı oturuma eklenir. |
| `@` ile başlamak | Dosya yolu tamamlar, dosyayı bağlama ekler. |
| Boş girdide `?` | Kısayol yardımını gösterir. |

macOS'ta `Option` kısayolları için terminalde Option tuşunu Meta olarak ayarlamak gerekir.

## Sık karıştırılanlar

- **`/clear` ile `/compact`:** `/clear` konuşmayı sıfırlar. `/compact` özetleyip sürdürür, özette ayrıntı kaybolabilir.
- **`/branch` ile `/fork`:** `/branch` seni yeni dala geçirir. `/fork` kopyayı arka planda koşturur, sen burada kalırsın.
- **`/rewind` ile Git:** Rewind Claude'un dosya araçlarıyla yaptığı değişikliği geri alır. Yalnız Bash'le değişen dosyayı, alt ajan düzenlemelerinin çoğunu ve oturum dışı değişikliği geri almaz. Asıl geri dönüş Git'tir.
- **`/status` ile `/config`:** `/status` neyin yüklendiğini gösterir. `/config` ayarı değiştirir.
- **`/hooks` ile hook testi:** `/hooks` yapılandırmayı gösterir, hook'un doğru çalıştığını kanıtlamaz.
"""

SORUN_GIDERME = r"""
Bir belirti çoğu zaman birkaç nedenden biridir. Aşağıdaki tablo her belirti için **ilk ayırıcı kontrolü** verir: nedenleri birbirinden ayıran en ucuz bakış. Aynı denemeyi tekrarlamak yerine yeni kanıt topla.

Hangi başlığın uyduğunu bilmiyorsan oturumda `/doctor` koş. Claude hiç açılmıyorsa kabukta `claude doctor`. Sorunun senin yapılandırmandan gelip gelmediğini ayırmak için `claude --safe-mode` ya da `claude --bare` ile başlat. Kaynak: [resmî sorun giderme](https://code.claude.com/docs/en/troubleshooting).

## Talimat ve ayar

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| CLAUDE.md'deki kural uygulanmıyor | `/memory` listesinde dosya var mı? | Yüklenmiyorsa yol ya da import onayı. Yükleniyorsa kural belirsiz ya da başka kuralla çelişiyor. [[1.2]] [[1.5]] |
| Import edilen dosya bazen görünüyor, bazen görünmüyor | Etkileşimli mi headless mi, worktree'de mi? | Proje dışı import onayı proje yolu başına tutulur. Her oturumda gereken bilgi için SessionStart hook'u. [[1.5]] [[8.1]] |
| Ayar değişikliği etki etmiyor | `/status` içinde `Setting sources` | Daha yüksek öncelikli katman aynı anahtarı ezmiş olabilir. Listeler birleşir, ezilmez. [[1.8]] |
| Model ayarı tutmuyor | `env` içinde `ANTHROPIC_MODEL` var mı? | Kabuktaki değişken dosyadaki `model` anahtarını geçer. [[1.8]] |
| Otomatik bellek eski bilgi veriyor | Kaydın tarihi ve kaynağın bugünkü hali | Eski kaydı düzelt ya da sil. [[1.7]] |

## İzin ve hook

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Aynı komut için sürekli izin soruluyor | Komutta `$(...)`, `${...}`, `source` var mı? | Bu parçaları içeren komut allow kuralıyla eşleşmeyip her seferinde sorabilir. Komutu onlarsız yaz, venv'i aktive etmek yerine yorumlayıcıyı doğrudan çağır. [[6.4]] |
| Gözetimsiz koşum izin ekranında takıldı | Oturumun gerçek etkin modu | Ayarlanan mod ile açılan mod farklı olabilir. Projenin kendi allow listesine bak. [[6.7]] [[13.2]] |
| Hook hiç çalışmıyor | `/hooks` listesinde var mı, eşleşme deseni doğru mu? | Betiği aynı JSON girdisiyle elle çalıştır. [[8.4]] |
| Hook çalışıyor ama engellemiyor | Hook async mi, çıkış kodu 2 mi? | Async hook engelleyemez. Olayın exit 2 davranışını belgede kontrol et. [[8.5]] [[8.6]] |
| İki hook'un sonucu her seferinde farklı | Aynı olaya eşleşen birden çok hook var mı? | Paralel çalışırlar. Bağımlı adımları tek betikte birleştir. [[8.7]] |

## Bağlam ve performans

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Bağlam çabuk doluyor | `/context` dağılımı | Büyük dosyayı parça parça okut, geniş aramayı alt ajana ver. [[2.4]] [[2.5]] |
| Otomatik sıkıştırma art arda tetikleniyor | `/context` içinde `Messages` payı | Odak vererek `/compact`, gerekirse `/clear` ve devir dosyası. [[2.6]] |
| Oturum dondu | `Ctrl+C` tepki veriyor mu? | Vermiyorsa terminali kapat, aynı dizinde `claude --resume`. Konuşma kaybolmaz. |
| Bellek ya da işlemci çok yüksek | Büyük derleme dizinleri, eklentiler | `.gitignore`'a ekle, `claude --safe-mode` ile eklenti ve MCP'yi ayır, yeniden başlatıp `--continue`. |
| `@dosya` ya da arama sonuç vermiyor | `claude doctor` çıktısında Search satırı | Paketli ripgrep çalışmıyor olabilir. Belgedeki ripgrep adımları. |

## Genişletme

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Skill hiç devreye girmiyor | `/skills` listesinde var mı? | Varsa açıklama, isteğin diliyle eşleşmiyor. Açıklamaya tetik kelimelerini ve sınırını yaz. [[9.3]] [[9.8]] |
| Yeni skill görünmüyor | Dosya doğru dizinde mi? | `/reload-skills`. |
| MCP aracı listede ama veri gelmiyor | `/mcp` durumu ve küçük bir okuma denemesi | Bağlantı, yetki ve sorgu kapsamını ayrı sına. [[9.7]] |
| Alt ajan raporu "bitti" diyor ama iş yok | Diff ve dosya | Rapor kanıt değildir. Dosyanın kendisine bak. [[12.3]] |

## Doğrulama, koşum ve yayın

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Testler geçti ama hata sürüyor | Koşulan test sayısı | Filtre hiçbir şeye eşleşmemiş olabilir. Hatayı geri koyup testin düştüğünü gör. [[12.1]] [[12.2]] |
| Headless betik başarılı diyor ama sonuç boş | JSON'da `is_error` ve `structured_output` | Yalnız `subtype` alanına güvenme. [[14.6]] [[14.7]] |
| Gece koşumu sabah bitmemiş, çıktı boş | Süreç yaşıyor mu, işlemci süresi ne, makine şarjda mı? | Arka plan işi tur bitince ölmüş ya da makine uyumuş olabilir. Bkz. deneyimler D03 ve D05. [[13.3]] [[13.4]] |
| Rutin hiç çalışmamış gibi | Zamanlandı mı, başladı mı, çıktı yazdı mı? | Üç aşamayı ayrı kontrol et. Sessizliği başarı sayma. [[14.3]] |
| Commit'te başkasının dosyaları var | `git log --stat` | Aynı checkout'ta başka oturum stage etmiş. Ayrı worktree. [[11.1]] [[11.2]] |
| Önizlemede değişiklik görünmüyor | Sunucu hangi dizinden, hangi porttan çalışıyor? | Başka oturumun sunucusuna bakıyor olabilirsin. [[11.3]] |
| Rewind sonrası bazı dosyalar eski halinde değil | Dosya Bash'le mi değişti? | Checkpoint onu izlemez. Git ile geri al. [[15.2]] |
| Belgedeki komut yok | `claude --version` | Belge yerel sürümden yeni olabilir. Güncelle ya da `/help` ile kontrol et. [[19.6]] |

## Yardım isterken

"Çalışmıyor" yerine dört şey yaz: beklenen, gözlenen, tekrar koşulu ve son değişiklik. Büyük log'u sohbete yapıştırma, dosyaya yaz ve ilgili kısmı okut.

```text
Beklenen: PreToolUse hook'u rm -rf içeren komutu reddetsin.
Gözlenen: komut sormadan çalıştı.
Tekrar: yeni oturum, proje kökünde, hook .claude/settings.json içinde.
Son değişiklik: hook'a async: true eklendi.
İstek: nedeni ayır, en küçük düzeltmeyi öner, aynı koşulda sına.
```
"""

EKLER = [
 dict(ad="komutlar", baslik="Komutlar ve kısayollar",
      ozet="Slash komutları işe göre, en çok işe yarayan CLI bayrakları, klavye kısayolları ve sık karıştırılan çiftler.", md=KOMUTLAR),
 dict(ad="sorun-giderme", baslik="Sorun giderme",
      ozet="Belirti, ilk ayırıcı kontrol ve sonraki adım. Talimat, izin, hook, bağlam, genişletme ve koşum sorunları.", md=SORUN_GIDERME),
 dict(ad="deneyimler", baslik="Gerçek deneyimlerden on ders",
      ozet="Tarihli ölçüm defterinden anonimleştirilmiş vakalar: gözlenen, ders, ayırıcı kanıt ve sınır.", md=DENEYIMLER),
 dict(ad="sozluk", baslik="Terimler sözlüğü",
      ozet="Listede geçen terimlerin bir cümlelik karşılıkları, konu başına gruplanmış.", md=SOZLUK),
]

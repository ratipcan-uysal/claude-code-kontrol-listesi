# İpuçları ve püf noktaları

_Belge kontrolü: 29 Ekim 2026_

Bu sayfa belgede yazan ama gözden kaçan ayarları, kısayolları ve tuzakları toplar. Her ipucu resmî belgeyle karşılaştırıldı. Belgede olmayan bir yöntem önerildiğinde bu açıkça yazıldı. Bazı ayarlar yeni sürüm ister. Sürüm şartı belgede yazıyorsa burada da yazıyor. Kendi sürümünü `claude --version` ile gör.

## Ayarlar

### Commit ve PR imzasını kaldır

Claude Code commit'lere varsayılan olarak `Co-Authored-By` satırı, PR gövdesine "Generated with Claude Code" satırı ekler. İkisini de `~/.claude/settings.json` içinden kapat:

```json
{
  "attribution": {
    "commit": "",
    "pr": "",
    "sessionUrl": false
  }
}
```

Boş metin o atfı gizler. `sessionUrl: false` bulut oturumlarındaki oturum bağlantısını da kaldırır. İnternette dolaşan `"includeCoAuthoredBy": false` satırı kullanımdan kalktı. Hâlâ okunuyor ama `attribution` ayarlanınca yok sayılıyor, yani yukarıdaki blokla birlikte yazmanın etkisi yok. Kısa yol `"attribution": false` 2.1.281 ve sonrasını ister. Daha eski sürüm bu değeri reddeder ve ayar dosyasının **tamamını** atlar. CLAUDE.md'ye "kendini imzalama" yazmak da işe yarar, ama kalıcı çözüm ayardır. [15.4](../README.md#15-git)

### Konuşma kayıtlarının ömrünü ayarla

`cleanupPeriodDays` kayıtların kaç gün tutulacağını belirler. Varsayılan 30. Eski bir oturuma aylar sonra dönmek istiyorsan büyüt, gizlilik için küçült. `0` geçersizdir, en az 1. Bu süre dolunca `/rewind` ve `/resume` de o oturumu bulamaz.

```json
{ "cleanupPeriodDays": 90 }
```

### `auto` ve `bypassPermissions` yalnız kullanıcı dosyasında çalışır

`permissions.defaultMode` için bu iki değer proje ya da yerel ayara yazılırsa etki etmez. `~/.claude/settings.json` dosyasına yaz. Böylece klonladığın bir depo seni sessizce izinsiz moda sokamaz. [6.7](../README.md#6-izin)

### Ortam değişkenini ayar dosyasına koy

`settings.json` içindeki `env` alanı her oturuma ve alt süreçlere ortam değişkeni verir. Kabuk profilini kirletmeden projeye özel değer tanımlarsın.

```json
{ "env": { "BASH_DEFAULT_TIMEOUT_MS": "300000" } }
```

Bash komutlarının varsayılan zaman aşımı 120 saniye, üst sınırı 600 saniyedir. Uzun derleme ya da test koşuyorsan bu iki değeri büyütmek, komutun yarıda kesilmesini önler. [13.4](../README.md#13-gozetimsiz)

### Kendi git kurallarını kullanıyorsan yerleşiklerini kapat

`includeGitInstructions: false` Claude'un bağlamından yerleşik commit ve PR talimatlarını ve git durum özetini çıkarır. Kendi commit skill'in ya da CLAUDE.md kuralların varsa çatışmayı önler.

### İki hesap, iki yapılandırma

`CLAUDE_CONFIG_DIR` bütün ayarları, kayıtları ve plugin'leri başka bir dizine taşır. İş ve kişisel hesabı ayırmak için:

```sh
alias claude-is='CLAUDE_CONFIG_DIR=~/.claude-is claude'
```

### Telemetriyi kapatırken dikkat

`DISABLE_TELEMETRY` değişkeni tanımlı olduğu sürece, değeri `0` ya da `false` olsa bile telemetri kapalı kalır. Yeniden açmak için değişkeni kaldırmak gerekir. Bu değişken `/skill-doctor` gibi bazı özellikleri de kapatır.

### Güncellemeleri bir hafta geriden al

`autoUpdatesChannel: "stable"` otomatik güncellemeyi yaklaşık bir hafta geriden ve büyük gerilemesi olan sürümleri atlayarak yapar. Varsayılan `latest`. Gözetimsiz koşumların bir sabah yeni sürümle bozulmasını istemiyorsan kullan. [19.6](../README.md#19-bakim)

```json
{ "autoUpdatesChannel": "stable" }
```

### Cevap dilini sabitle

`language` ayarına yazdığın değer Claude'a "hep bu dilde cevap ver" diye iletilir. Ses dikteyi ve otomatik oturum başlıklarını da etkiler. Değer doğrulanmaz, `"Türkçe"` yazman yeter.

## Talimatlar

### Yeni model çıkınca talimatlarını buda

Talimatların bir kısmı eski bir modelin eksiğini kapatmak için yazılmıştır. Yeni model o eksiği taşımıyorsa bu satırlar işe yaramaz, hatta zarar verir. Belge iki şey söylüyor. Büyük harfli vurgu ve "CRITICAL: You MUST" tarzı dil güncel modellerde kuralı aşırı uygulatabilir, düz bir cümle yeterli. Yeni model varsayılan haliyle daha iyi sonuç veriyorsa eski talimatları kaldırmayı değerlendir.

Bundan bir deneme yöntemi çıkar. Belgede bu döngü olarak yazmıyor, bir iş akışı önerisidir: şüphelendiğin talimatları kaldır, temsilî birkaç işi yeni modelle koş, yalnız modelin gerçekten kaçırdığı kuralları geri ekle. [5.6](../README.md#5-model) [19.3](../README.md#19-bakim)

### `/doctor prompt-audit` eski talimatları işaretler

`/doctor prompt-audit` talimat dosyalarını tarar. Eski modeller için yazılmış talimatları, artık var olmayan dosya ya da komuta işaret eden satırları ve birbiriyle çelişen dosyaları raporlar. Sen onaylamadan hiçbir dosyaya dokunmaz. Varsayılan kapsam CLAUDE.md, CLAUDE.local.md, AGENTS.md ve `.claude/` ile `~/.claude/` altındaki kurallar, skill'ler, komutlar, alt ajanlar ve stillerdir. Tek dosya ya da dizin için yol ver. 2.1.283 ve sonrasında var.

```text
/doctor prompt-audit
/doctor prompt-audit .claude/skills/deploy
```

### CLAUDE.md'ye bağlam harcamayan not yaz

CLAUDE.md içindeki `<!-- ... -->` blok yorumları bağlama girmeden silinir. Bakımcıya not, kuralın gerekçesini ya da tarihini bırakırsın, modelin dikkati dağılmaz. [18.4](../README.md#18-bilgi)

### Sıkıştırmadan sonra ne kalır

`/compact` sonrasında proje kökündeki CLAUDE.md diskten yeniden yüklenir. Kaybolan yalnız konuşmada verdiğin talimattır. Oturum boyunca geçerli kalması gereken bir kuralı sohbete değil dosyaya yaz. [2.6](../README.md#2-baglam)

### Büyük depoda ilgisiz CLAUDE.md'leri dışla

Bir monorepoda başka ekiplerin CLAUDE.md dosyaları da yüklenir. `claudeMdExcludes` glob ya da mutlak yolla bunları dışarıda bırakır. Değerler katmanlar arasında birleşir. Kurumun yönetilen CLAUDE.md'si dışlanamaz.

```json
{ "claudeMdExcludes": ["**/legacy/**/CLAUDE.md"] }
```

### Ek dizinin talimatını da yükle

`--add-dir` ya da `/add-dir` ile eklenen dizinin skill'leri yüklenir ama CLAUDE.md'si yüklenmez. O dizinin kuralları da geçerli olsun istiyorsan `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` ver. [1.5](../README.md#1-talimat)

## Oturum

### Oturumlara ad ver

`claude -n odeme-refactor` ya da oturum içinde `/rename odeme-refactor`. Sonra `claude --resume odeme-refactor` ile adıyla dönersin. Uzun kimlik aramak gerekmez. [2.7](../README.md#2-baglam)

### Uzun prompt'u editörde yaz

`Ctrl+G` girdiyi varsayılan metin editöründe açar. Çok paragraflı bir brief'i terminal satırında yazmaktan kolaydır. `/config` içinden Claude'un son cevabını da editöre yorum olarak getirebilirsin.

### Ana işi bölmeden soru sor

`/btw neden bu kütüphaneyi seçtin?` cevabı gösterir ama konuşmaya eklemez. Bağlam büyümez, ana iş yön değiştirmez.

### Kod bloğunu tek tuşla al

`/copy` son cevabı panoya kopyalar. Cevapta birden çok kod bloğu varsa seçici açılır, `w` ile seçtiğini dosyaya yazar. SSH üzerinden pano çalışmıyorsa işe yarar.

### Bitiş koşulu olan iş için `/goal`

`/goal bütün testler geçiyor ve lint temiz` Claude'u koşul sağlanana kadar turdan tura çalıştırır. Her turdan sonra ayrı bir model koşulu değerlendirir. Koşul doğrulanabilir olmalı. [3.1](../README.md#3-gorev)

### Konuşmanın yalnız bir kısmını sıkıştır

`/rewind` menüsünde geri sarmanın yanında "Summarize from here" seçeneği var. Seçtiğin mesajdan sonrasını özetler, öncesini olduğu gibi bırakır. `/compact` bütün konuşmayı özetler. Baştaki kararlar önemliyse ve sondaki uzun deneme gereksizse bu daha az ayrıntı kaybettirir. [2.6](../README.md#2-baglam)

### Yazdığın taslağı kaybetme

Girdide yazı varken Esc Esc yazıyı siler ama geçmişe kaydeder, yukarı okla geri gelir. Yarım bir prompt'u kenara koyup başka bir şey sormak için `Ctrl+S`: girdiyi saklar, boş girdide tekrar basınca geri getirir.

### Prompt'u silmeden model değiştir

macOS'ta `Option+P`, diğerlerinde `Alt+P` modeli değiştirir ve yazdığın girdi yerinde kalır. Option kısayolları için terminalde Option tuşunu Meta olarak ayarlaman gerekir. `/model` seçicisinde `s` tuşu seçimi yalnız bu oturum için yapar, varsayılanı değiştirmez. [5.2](../README.md#5-model)

### Kabuk komutunu Claude'a sormadan çalıştır

Satır başına `!` koyarsan komut doğrudan çalışır ve çıktısı oturuma eklenir. `! git status` Claude'un bir tur harcamasından ucuzdur ve Claude çıktıyı görür. Uzun süren komutu `Ctrl+B` arka plana alır.

### Kayıt dosyasından oturum aç

`claude --resume` oturum kimliği yerine bir `.jsonl` kayıt yolunu da kabul eder. 2.1.223 ve sonrasında kimlik araması bütün projeleri tarar, oturumu hangi dizinde açtığını hatırlaman gerekmez.

### Hedef oturumla birlikte geri gelir

`/goal` ile koyduğun hedef `--continue` ya da `--resume` ile dönünce geri yüklenir. Kaldırmak için `/goal clear`. Zaman aralığıyla tekrar için `/loop`, ayar dosyasında kalıcı bir koşul için Stop hook'u var. [14.5](../README.md#14-rutin)

## Bağlam ve çıktı

### Büyük araç çıktısının sınırları

Bash çıktısı varsayılan olarak 30.000 karakterde kesilir, `BASH_MAX_OUTPUT_LENGTH` ile 150.000'e kadar çıkar. MCP aracı çıktısının sınırı 25.000 token, `MAX_MCP_OUTPUT_TOKENS` ile değişir. Sınırı büyütmek bağlamı da büyütür. Büyük çıktıyı dosyaya yazdırıp ilgili kısmını okutmak çoğu zaman daha iyidir. [2.5](../README.md#2-baglam)

### Çıktı token'ını büyütmenin bedeli

`CLAUDE_CODE_MAX_OUTPUT_TOKENS` tek cevabın uzunluk sınırını büyütür. Ama bu pay bağlamdan ayrılır, otomatik sıkıştırma daha erken tetiklenir. Uzun dosya yazdırırken işe yarar, her oturumda açık bırakma.

### Headless koşuma bütçe koy

`claude -p` ile `--max-budget-usd` tahmini harcama sınıra gelince koşumu durdurur. Döngüye giren bir betiğin sabaha kadar harcamasını önler. Tur sınırı için `--max-turns` var, ama yerel 2.1.284 yardım çıktısında görünmüyor, kullanmadan önce dene. [14.2](../README.md#14-rutin)

### Sistem prompt'una ekle, değiştirme

`--append-system-prompt` ve `--append-system-prompt-file` varsayılan sistem prompt'unun sonuna metin ekler. `--system-prompt` ise tamamını değiştirir, araç kullanım talimatları dahil. Çoğu iş için ekleme yeter.

## Hata ayıklama

### `--safe-mode` ile `--bare` farklı işler

`claude --safe-mode` bütün özelleştirmeleri kapatır: CLAUDE.md, skill, plugin, hook, MCP, bellek. Giriş, model ve izinler normal kalır. Bir sorunun senin yapılandırmandan gelip gelmediğini ayırmanın en hızlı yolu budur. `--bare` ise betikler içindir: keşfi atlar, OAuth'u da okumaz, kimlik `ANTHROPIC_API_KEY` ile gelmelidir.

### Ayarın neden etki etmediğini bul

Üç kontrol yeter. `/status` içindeki `Setting sources` yüklenen dosyaları gösterir. `/doctor` ayrıştırılamayan ayar dosyasını bulur. `/context` bağlamda gerçekte nelerin durduğunu gösterir. [1.8](../README.md#1-talimat)

## Genişletme

### Hook'un `if` alanı her olayda çalışmaz

`if` alanı hook'u araç adı ve argümanıyla süzer: `"Bash(git *)"`, `"Edit(*.ts)"`. Eşleşmeyince süreç hiç başlamaz, başlatma maliyeti de olmaz. Ama `if` yalnız araç olaylarında değerlendirilir: PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest ve PermissionDenied. Başka bir olaya `if` konmuş hook **hiç çalışmaz**. Tek kural alır, `&&` ya da liste kabul etmez. [8.2](../README.md#8-hook) [8.4](../README.md#8-hook)

### Yan etkili skill'i otomatik çağrıya kapat

Skill frontmatter'ında `disable-model-invocation: true` olan skill'i Claude kendi başına yüklemez. Yalnız sen `/ad` yazınca çalışır. Yayın, silme ya da mesaj gönderme gibi işler için. `context: fork` skill'i ayrı bir alt ajan bağlamında çalıştırır, ana bağlamı doldurmaz. `allowed-tools` yalnız o turda izinsiz kullanılacak araçları açar. [9.4](../README.md#9-yeniden)

### Worktree'li alt ajan nereden dallanır

Alt ajan tanımında `isolation: worktree` onu geçici bir worktree'de çalıştırır. Bu worktree senin o anki dalından değil, deponun varsayılan dalından açılır. Commit'lenmemiş değişikliklerin ve dalındaki yeni commit'ler alt ajanda görünmez. Değişiklik yoksa worktree kendiliğinden temizlenir. [11.1](../README.md#11-paralel)

### Kullanılmayan skill'leri bul

`/skill-doctor` her skill'in bağlamda ne kadar yer tuttuğunu ve ne sıklıkla kullanıldığını gösterir. Hiç çağrılmayan ama açıklaması her oturumda bağlamda duran skill'i kapatmak için. 2.1.252 ve sonrasında var.

### Başka araçtan geç

`/import codex`, `/import gemini` ve `/import cursor` o aracın talimatlarını, MCP sunucularını, komutlarını, ajanlarını ve skill'lerini getirir. Önce `--dry-run` ile ne geleceğini gör.

### Skill'i yalnız ilgili dosyada yükle

Skill frontmatter'ındaki `paths` alanı skill'i yalnız eşleşen dosyalarla çalışırken otomatik yükler. `user-invocable: false` skill'i `/` menüsünden gizler, yalnız Claude çağırır. Sadece arka plan bilgisi taşıyan skill için uygundur. [9.3](../README.md#9-yeniden)

### Alt ajanı CLAUDE.md'siz başlat

Alt ajan tanımında `omitClaudeMd: true` onu kullanıcı, proje ve yerel CLAUDE.md olmadan başlatır. Bağımsız bir inceleme ajanının senin varsayımlarınla yüklenmesini istemiyorsan işe yarar. 2.1.271 ve sonrasında var. [9.1](../README.md#9-yeniden)

### Gitignore'daki dosyaları worktree'ye taşı

Yeni worktree'de `.env` gibi git'in yok saydığı dosyalar olmaz, uygulama açılmaz. Proje kökündeki `.worktreeinclude` dosyasına yazdığın desenler yeni worktree'ye kopyalanır. [11.1](../README.md#11-paralel)

### MCP onaylarını sıfırla

`.mcp.json` sunucularına verdiğin "evet" ya da "hayır" kalıcıdır. Yanlış cevapladıysan `claude mcp reset-project-choices`. Yalnız kendi verdiğin MCP yapılandırmasını kullanmak için `--strict-mcp-config` ile `--mcp-config`. [9.7](../README.md#9-yeniden)

### Arka plan hook'u Claude'u uyandırabilir

`async: true` hook engelleyemez. `asyncRewake` ise arka planda çalışır ve çıkış kodu 2 ile Claude'u boştayken bile uyandırır, çıktısı sistem notu olarak gelir. Uzun bir testin sonucunu beklemeden çalışmaya devam edip bitince haber almak için. [8.6](../README.md#8-hook)

### Kendi kullanımını gör

`/insights` son oturumlarından bir rapor üretir: hangi projelerde ne yaptığın, nerede takıldığın, hangi özellikleri denemediğin. Rapor `~/.claude/usage-data/report.html` dosyasına yazılır. [19.5](../README.md#19-bakim)

## Ekip ve güvenlik

### Her komutu denetim için sar

`CLAUDE_CODE_SHELL_PREFIX` Bash komutlarını, hook'ları, durum satırını ve yerel MCP sunucularını verdiğin komutla sarar. Kurum, çalıştırılan her komutu bununla günlüğe yazar.

### Politikayı ekipler arasında böl

Yönetilen ayar dizinindeki `managed-settings.d/` altına konan `*.json` dosyaları alfabetik sırayla birleşir. Güvenlik ekibi `10-guvenlik.json`, platform ekibi `20-platform.json` yazar, aynı dosyayı paylaşmaz.

### Ekibe açılışta duyuru göster

`companyAnnouncements` bir metin dizisidir. Claude Code açılırken bunlardan birini gösterir. Yeni bir kuralı, iç dokümanın adresini ya da bakım saatini duyurmak için. [10.3](../README.md#10-ekip)

### Prompt geçmişi süre dolunca silinmez

Konuşma kayıtları `cleanupPeriodDays` sonunda silinir, ama yazdığın prompt'ların tutulduğu `~/.claude/history.jsonl` silinmez. Bir prompt'a gizli bilgi yapıştırdıysan o dosyada kalır. [7.1](../README.md#7-guvenlik)

### Hook'ları kapatmak durum satırını da kapatır

`disableAllHooks: true` bütün hook'ları kapatır. Durum satırı ve dosya önerisi komutu da aynı mekanizmayla çalıştığı için onlar da kapanır. Bir hook'u geçici olarak devre dışı bırakmak istiyorsan yalnız onu kaldır.

---

[Kontrol listesi](../README.md) · [Rehber](../rehber/README.md) · [Komutlar ve kısayollar](komutlar.md) · [Sorun giderme](sorun-giderme.md) · [Dosya konumları](dosyalar.md) · [Gerçek deneyimlerden on ders](deneyimler.md) · [Terimler sözlüğü](sozluk.md)

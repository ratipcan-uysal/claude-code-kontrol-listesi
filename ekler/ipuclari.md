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

`settings.json` içindeki `env` alanı her oturuma ve alt süreçlere ortam değişkeni verir. Kabuk profilini kirletmeden, projeye özel değer tanımlamak için kullanılır.

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

CLAUDE.md içindeki `<!-- ... -->` blok yorumları bağlama girmeden silinir. Bakımcıya not, kuralın gerekçesi ya da tarih bırakmak için kullanılır, modelin dikkatini dağıtmaz. [18.4](../README.md#18-bilgi)

### Sıkıştırmadan sonra ne kalır

`/compact` sonrasında proje kökündeki CLAUDE.md diskten yeniden yüklenir. Kaybolan yalnız konuşmada verdiğin talimattır. Oturum boyunca geçerli kalması gereken bir kuralı sohbete değil dosyaya yaz. [2.6](../README.md#2-baglam)

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

### Kendi kullanımını gör

`/insights` son oturumlarından bir rapor üretir: hangi projelerde ne yaptığın, nerede takıldığın, hangi özellikleri denemediğin. Rapor `~/.claude/usage-data/report.html` dosyasına yazılır. [19.5](../README.md#19-bakim)

---

[Kontrol listesi](../README.md) · [Komutlar ve kısayollar](komutlar.md) · [Sorun giderme](sorun-giderme.md) · [Dosya konumları](dosyalar.md) · [Gerçek deneyimlerden on ders](deneyimler.md) · [Terimler sözlüğü](sozluk.md)

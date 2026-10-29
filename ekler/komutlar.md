# Komutlar ve kısayollar

_Belge kontrolü: 29 Ekim 2026_

Claude Code'a üç yoldan komut verilir. Oturumun içinde `/` ile başlayan **slash komutu**, kabukta `claude` ile başlayan **CLI bayrağı** ve **klavye kısayolu**. Aynı iş çoğu zaman üçünden biriyle yapılır: geçmiş oturuma `/resume` ile oturumun içinden, `claude --resume` ile kabuktan dönülür.

Bu sayfa günlük işte fark yaratan komutları işe göre gruplar. Belgedeki komut tablosu 120 satırdan uzun, hepsi burada yok. Belge yerel CLI 2.1.284'ten yeni, bazı komutlar senin sürümünde görünmeyebilir. Emin olmak için oturumda `/help` yaz ya da `claude --version` ile sürümü gör. Kaynaklar: [komutlar](https://code.claude.com/docs/en/commands), [CLI referansı](https://code.claude.com/docs/en/cli-reference), [etkileşimli mod](https://code.claude.com/docs/en/interactive-mode).

## Slash komutları, işe göre

### Bağlam

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/context` | Bağlamın neyle dolduğunu görmek için | Talimat, araç ve mesaj payını ayrı gösterir. Tahmin yerine buna bak. [2.2](../README.md#2-baglam) |
| `/compact [odak]` | Uzayan oturumda yer açmak için | Ayrıntı kaybettirir. Neyin korunacağını yaz. [2.6](../README.md#2-baglam) |
| `/clear` | Konu değişince | Konuşmayı sıfırlar, dosyalara dokunmaz. [2.3](../README.md#2-baglam) |
| `/btw [soru]` | Ana işi bölmeden kısa bir şey sormak için | Soru ve cevap konuşmaya eklenmez. |
| `/recap` | Uzun oturumda nerede kaldığını görmek için | Tek satırlık özet. Devir dosyasının yerini tutmaz. |

### Oturum ve geri dönüş

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/resume [ad]` | Eski bir oturuma dönmek için | `/rename` ile ad verdiysen adla bulunur. [2.7](../README.md#2-baglam) |
| `/branch [ad]` | Aynı noktadan başka bir yol denemek için | Seni dala geçirir, orijinal korunur. |
| `/fork [prompt]` | Konuşmayı arka planda ikinci bir oturumda sürdürmek için | `/branch` ile aynı değil: sen burada devam edersin. |
| `/rewind` | Kodu, konuşmayı ya da ikisini geri sarmak için | Boş girdide Esc Esc ile de açılır. Yalnız Bash'le değişen dosyayı geri almaz. [15.2](../README.md#15-git) |
| `/rename [ad]` | Oturumu sonra bulabilmek için | Ad vermezsen kendisi üretir. |
| `/export [dosya]` | Konuşmayı metin olarak saklamak için | Hassas içerik varsa paylaşmadan önce oku. |
| `/diff` | Çalışma ağacındaki değişikliği görmek için | Claude'un yaptığı düzenlemeler dahil. |

### Model, çaba ve kullanım

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/model [model]` | Modeli değiştirmek için | Seçim varsayılan olarak kaydedilir. Yalnız bu oturum için seçicide ayrı seçenek var. [5.2](../README.md#5-model) |
| `/effort [düzey]` | Düşünme çabasını işe göre ayarlamak için | Düzeyler modele bağlı. [5.3](../README.md#5-model) |
| `/fast` | Hızlı modu açıp kapatmak için | Model kataloğuna ve hesaba bağlı. |
| `/advisor` | Zor kararda ikinci bir modelin görüşü için | [5.5](../README.md#5-model) |
| `/usage` | Oturum maliyeti, plan limiti ve istatistik için | `/cost` ve `/stats` aynı komutun takma adı. [5.4](../README.md#5-model) |

### Talimat, ayar ve izin

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/init` | Projeye ilk CLAUDE.md taslağı için | Taslağı gerçek komutlarla düzelt. [1.2](../README.md#1-talimat) |
| `/memory` | Yüklenen talimat dosyalarını ve otomatik belleği görmek için | Import'un yüklenip yüklenmediğine buradan bak. [1.5](../README.md#1-talimat) [1.7](../README.md#1-talimat) |
| `/status` | Sürüm, model, hesap ve yüklenen ayar dosyaları için | `Setting sources` dosyaları listeler, anahtar bazında kaynak göstermez. [1.8](../README.md#1-talimat) |
| `/config` | Ayar arayüzü ya da `key=value` ile ayar yazmak için | Takma adı `/settings`. Hangi katmana yazdığına dikkat et. |
| `/permissions` | allow, ask, deny kurallarını yönetmek için | [6.1](../README.md#6-izin) [6.3](../README.md#6-izin) |
| `/fewer-permission-prompts` | Geçmişten salt okunur komutlar için allow listesi önerisi | Öneriyi kabul etmeden önce tek tek oku. [6.6](../README.md#6-izin) |
| `/sandbox` | Sandbox'ı açıp kapatmak için | Yalnız desteklenen platformlarda. [7.5](../README.md#7-guvenlik) |
| `/hooks` | Etkin hook'ları görmek için | Yalnız gösterir. Hook'un çalıştığını göstermez, onu testle sına. [8.4](../README.md#8-hook) |
| `/statusline` | Durum satırını kurmak için | [8.3](../README.md#8-hook) |
| `/doctor` | Kurulum, ayar ve eklenti sorunlarını taramak için | Claude hiç açılmıyorsa kabukta `claude doctor`. |

### Genişletme

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/skills` | Yüklü skill'leri görmek için | Açıklaması zayıf skill listede olsa da çağrılmaz. [9.3](../README.md#9-yeniden) |
| `/reload-skills` | Diske eklenen skill'i yeniden başlatmadan almak için | |
| `/plugin` | Plugin kurmak ve yönetmek için | [9.6](../README.md#9-yeniden) |
| `/mcp` | MCP sunucularının durumunu görmek, yeniden bağlamak için | Bağlı görünmek aracın çalıştığını kanıtlamaz. [9.5](../README.md#9-yeniden) |
| `/agents` | Alt ajan yönetimi | Yeni sürümlerde arayüz açmaz, Claude'dan istemeni ya da `.claude/agents/` dosyasını düzenlemeni söyler. |

### İnceleme ve uzun iş

| Komut | Ne zaman | Dikkat |
|---|---|---|
| `/plan [görev]` | Belirsiz büyük işte önce plan için | Shift+Tab ile de plan moduna geçilir. [3.3](../README.md#3-gorev) |
| `/goal [koşul]` | Koşul sağlanana kadar Claude'un turlar boyunca sürmesi için | Koşul doğrulanabilir olmalı. [3.1](../README.md#3-gorev) |
| `/code-review` | Diff'i ya da PR'ı doğruluk hataları için incelemek için | Takma adı `/review`. [12.6](../README.md#12-dogrulama) |
| `/security-review` | Dal değişikliklerini güvenlik için incelemek için | `origin` remote gerekir. |
| `/loop [aralık] [prompt]` | Oturum açıkken bir işi tekrar tekrar koşmak için | Oturum kapanınca durur. Kalıcı iş için `/schedule`. [14.5](../README.md#14-rutin) |
| `/schedule` | Bulutta zamanlanmış görev kurmak için | Bilgisayar kapalıyken de koşar. [14.1](../README.md#14-rutin) |
| `/tasks` | Arka plandaki işleri görmek için | Arka plan işi bitmeden turu kapatma. [13.4](../README.md#13-gozetimsiz) |

## CLI bayrakları

| Bayrak | Ne yapar | Dikkat |
|---|---|---|
| `-c`, `--continue` | Bu dizindeki son oturumu sürdürür | |
| `-r`, `--resume [ad]` | Adla ya da seçiciyle oturum sürdürür | |
| `--fork-session` | Sürdürürken yeni oturum kimliği açar | `--resume` ya da `--continue` ile. [2.7](../README.md#2-baglam) |
| `-n`, `--name` | Oturuma ad verir | Sonra `--resume <ad>` ile bulunur. |
| `-p`, `--print` | Headless koşum: cevabı yazar, çıkar | Betik ve rutinlerin temeli. |
| `--output-format` | `text`, `json`, `stream-json` | Yalnız `-p` ile. [14.6](../README.md#14-rutin) |
| `--json-schema` | Şemaya uyan doğrulanmış JSON | Sonuç `structured_output` alanında. Alan yoksa üretilememiştir. [14.7](../README.md#14-rutin) |
| `--max-turns` | Tur sınırı, dolunca hatayla çıkar | Yerel 2.1.284 `--help` çıktısında görünmedi, kullanmadan önce dene. [14.2](../README.md#14-rutin) |
| `--max-budget-usd` | Tahmini harcama sınırı | Yalnız `-p` ile. |
| `--no-session-persistence` | Oturumu diske yazmaz | Karşılaştırma koşumlarında listeyi kirletmez. |
| `--model` | Bu oturumun modeli | Yalnız başlatılan oturuma uygulanır. [5.6](../README.md#5-model) |
| `--effort` | Bu oturumun çaba düzeyi | |
| `--permission-mode` | Başlangıç izin modu | Gözetimsiz koşumda etkin modu ayrıca doğrula. [6.7](../README.md#6-izin) |
| `--allowedTools`, `--disallowedTools` | Sormadan izinli ya da yasak araçlar | Kalıcı kural için proje ayarı daha izlenebilir. |
| `--settings` | Yalnız bu oturum için ayar dosyası ya da JSON | Öncelikte yönetilen katmanın hemen altında. [1.8](../README.md#1-talimat) |
| `--add-dir` | Ek çalışma dizini | |
| `--append-system-prompt` | Sistem prompt'unun sonuna ekleme | `--system-prompt` tamamen değiştirir. |
| `--mcp-config` | MCP sunucularını JSON'dan yükler | |
| `-w`, `--worktree` | Ayrı bir git worktree'de başlatır | [11.1](../README.md#11-paralel) |
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

---

[Kontrol listesi](../README.md) · [Rehber](../rehber/README.md) · [Sorun giderme](sorun-giderme.md) · [Dosya konumları](dosyalar.md) · [İpuçları ve püf noktaları](ipuclari.md) · [Gerçek deneyimlerden on ders](deneyimler.md) · [Terimler sözlüğü](sozluk.md)

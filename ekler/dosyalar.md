# Dosya konumları

_Belge kontrolü: 29 Ekim 2026_

Claude Code davranışını birkaç düzine dosyadan alır ve yaptığı işi de dosyalara yazar. Bir ayar beklediğin gibi çalışmıyorsa, bir bilgi bir oturumda var ötekinde yoksa ya da disk doluyorsa cevap çoğu zaman bu sayfadaki bir yoldadır.

Yollar macOS ve Linux içindir. Windows'ta `~/.claude`, `%USERPROFILE%\.claude` olur. `CLAUDE_CONFIG_DIR` ortam değişkeni verilirse `~/.claude` altındaki her şey, `~/.claude.json` ve kimlik dosyası da o dizine taşınır. Kaynaklar: [ayarlar](https://code.claude.com/docs/en/settings), [.claude dizini](https://code.claude.com/docs/en/claude-directory), [bellek](https://code.claude.com/docs/en/memory), [MCP](https://code.claude.com/docs/en/mcp).

## Ayar dosyaları

Öncelik yüksekten düşüğe: yönetilen, komut satırı, proje yerel, paylaşılan proje, kullanıcı. İzin listeleri katmanlar arasında birleşir. Hangi dosyaların yüklendiğini `/status` içindeki `Setting sources` satırı gösterir. [1.8](../README.md#1-talimat)

| Yol | Kapsam | Ne için | Git |
|---|---|---|---|
| `~/.claude/settings.json` | Kullanıcı, bütün projeler | Kişisel izinler, hook'lar, `env`, model, atıf | Girmez |
| `.claude/settings.json` | Proje, ekip | Ekibin ortak izinleri, hook'ları, plugin'leri | Girer [10.1](../README.md#10-ekip) |
| `.claude/settings.local.json` | Proje, yalnız sen | Bu projede kişisel ayar. "Bir daha sorma" dediğin izinler buraya yazılır | Girmez. Claude Code dosyayı yaratırken global git excludes'a ekler |
| `/Library/Application Support/ClaudeCode/managed-settings.json` | Yönetilen (macOS) | Kurum politikası. Kullanıcı ve proje ayarları bunu ezemez | Girmez. IT dağıtır |
| `/etc/claude-code/managed-settings.json` | Yönetilen (Linux, WSL) | Aynı | Girmez |
| `C:\Program Files\ClaudeCode\managed-settings.json` | Yönetilen (Windows) | Aynı. Eski `ProgramData` yolu artık okunmaz | Girmez |
| `managed-settings.d/*.json` | Yönetilen, parçalı | Politikayı ekipler arasında bölmek. Dosyalar alfabetik sırayla birleşir | Girmez |
| `managed-mcp.json` | Yönetilen | Kurumun sabit MCP sunucu seti | Girmez |

Bozuk bir ayar dosyası bütünüyle atlanır, tek satır bile uygulanmaz. Bir ayar hiç etki etmiyorsa önce `/doctor` ile dosyanın ayrıştırılıp ayrıştırılmadığına bak.

## `~/.claude.json`

Claude Code'un kendi durum dosyası. Elle düzenlemen gerekmez. İçinde hesap bilgisi, kullanıcı ve local kapsamlı MCP sunucuları, proje başına güven kararları ve `/config` ekranının yazdığı genel ayarlar durur. Giriş anahtarı bu dosyada değildir: macOS'ta Keychain'de, Linux ve Windows'ta `~/.claude/.credentials.json` dosyasındadır.

Dosya her yeniden yazımda eski kopyasını `~/.claude/backups/` altına bırakır, en yeni beşi tutulur.

## Talimat dosyaları

| Yol | Ne zaman yüklenir | Git |
|---|---|---|
| `~/.claude/CLAUDE.md` | Her oturumda, bütün projelerde | Girmez [1.1](../README.md#1-talimat) |
| `./CLAUDE.md` ya da `./.claude/CLAUDE.md` | Projede her oturumda | Girer [1.2](../README.md#1-talimat) |
| `./CLAUDE.local.md` | Projede her oturumda, yalnız bu makinede | Girmez, `.gitignore`'a sen eklersin [1.3](../README.md#1-talimat) |
| Alt dizindeki `CLAUDE.md` | Claude o dizinde bir dosyaya dokununca. Çalışma dizininin üstündekiler açılışta yüklenir | Girer |
| `.claude/rules/*.md` | `paths` deseniyle eşleşen dosyaya dokununca | Girer [1.4](../README.md#1-talimat) |
| `~/.claude/rules/*.md` | Aynı, bütün projelerde | Girmez |
| `AGENTS.md` | Çalışma dizininde ve üstünde hiç CLAUDE dosyası yoksa | Girer [1.6](../README.md#1-talimat) |
| Yönetilen `CLAUDE.md` | Her oturumda. Kullanıcı dışlayamaz | Girmez |

İki ince nokta var. Birincisi, `CLAUDE.local.md` eklemek de `AGENTS.md`'nin okunmasını durdurur. İkisini birlikte istiyorsan `CLAUDE.md` içine `@AGENTS.md` yaz. İkincisi, `--add-dir` ile eklenen dizinin `CLAUDE.md`'si varsayılan olarak yüklenmez.

## Otomatik bellek

Claude'un kendi tuttuğu notlar `~/.claude/projects/<proje>/memory/` altında durur. `MEMORY.md` bir dizindir ve her oturumda ilk 200 satırı ya da ilk 25 KB'ı yüklenir. Konu dosyaları açılışta yüklenmez, Claude gerektiğinde okur. Aynı deponun bütün worktree'leri tek bellek dizinini paylaşır. Bellek makineye yereldir, başka makineye ve buluta gitmez. [1.7](../README.md#1-talimat)

Kapatmak için `/memory` ekranı, ayarda `autoMemoryEnabled: false` ya da `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Yerini `autoMemoryDirectory` değiştirir. Alt ajanların kalıcı belleği ayrı tutulur: `agent-memory/<ad>/`.

## Skill, ajan, komut ve stil

| Yol | Ne | Git |
|---|---|---|
| `~/.claude/skills/<ad>/SKILL.md` | Kişisel skill, bütün projelerde | Girmez |
| `.claude/skills/<ad>/SKILL.md` | Proje skill'i | Girer [9.2](../README.md#9-yeniden) |
| `~/.claude/agents/*.md`, `.claude/agents/*.md` | Alt ajan tanımları | Proje olan girer |
| `~/.claude/commands/*.md`, `.claude/commands/*.md` | Eski biçim özel komut. Hâlâ çalışır, aynı adlı skill varsa skill kazanır. Yeni iş için skill tercih et | Proje olan girer |
| `~/.claude/output-styles/`, `.claude/output-styles/` | Cevap üslubu tanımları | Proje olan girer |
| `~/.claude/keybindings.json` | Klavye kısayolu değişiklikleri. `/keybindings` açar | Girmez |
| `~/.claude/statusline.sh` | Durum satırı betiği. Yolu `settings.json` içindeki `statusLine` alanında | Girmez [8.3](../README.md#8-hook) |
| `.worktreeinclude` | Git'in yok saydığı dosyalardan hangilerinin yeni worktree'ye kopyalanacağı | Girer [11.1](../README.md#11-paralel) |

## MCP

| Kapsam | Nerede durur | Kimle paylaşılır |
|---|---|---|
| local (varsayılan) | `~/.claude.json` içinde bu projenin altında | Kimseyle |
| project | Proje kökünde `.mcp.json` | Ekiple, git üzerinden |
| user | `~/.claude.json` | Kimseyle, bütün projelerinde açık |
| managed | Sistem dizininde `managed-mcp.json` | Kurum |

İsim karışıklığına dikkat: MCP'nin "local" kapsamı `~/.claude.json` içindedir, `settings.local.json` ile ilgisi yoktur. `.mcp.json` ilk kullanımda onay ister. Headless koşumda soru sormadan yüklenir. [9.7](../README.md#9-yeniden)

## Hook ve plugin

Hook'lar ayrı bir dosyada değil, ayar dosyalarının `hooks` alanında tanımlanır: kullanıcı, proje, yerel ve yönetilen katman. Bunlara ek olarak plugin içindeki `hooks/hooks.json`, skill ve alt ajan frontmatter'ı da hook taşıyabilir. Bulut oturumları yerel `~/.claude/settings.json` dosyasını okumaz. [8.1](../README.md#8-hook)

Plugin'ler `~/.claude/plugins/` altında durur. Burada sürüm başına önbellek (`cache/`), plugin'in güncellemelerde korunan verisi (`data/`) ve marketplace kopyaları (`marketplaces/`) vardır. Bir plugin'in kendi yapısında yalnız `.claude-plugin/plugin.json` manifest dizinindedir. `skills/`, `agents/`, `hooks/` ve `.mcp.json` plugin kökünde durur. [9.6](../README.md#9-yeniden)

## Oturum verisi

Hepsi `~/.claude/` altındadır. Çoğu `cleanupPeriodDays` ayarına göre silinir, varsayılan 30 gündür.

| Yol | İçerik | Silinir mi |
|---|---|---|
| `projects/<proje>/<oturum>.jsonl` | Konuşma kaydı: mesajlar, araç çağrıları ve sonuçları | Süre dolunca. Silinen oturum `/resume` listesinden de kalkar |
| `projects/<proje>/<oturum>/subagents/`, `tool-results/` | Alt ajan kayıtları, taşan büyük araç çıktıları | Aynı |
| `file-history/<oturum>/` | Claude'un düzenlediği dosyaların önceki hali. `/rewind` buradan geri yükler | Aynı. Silinmişse rewind dosya geri getiremez |
| `plans/` | Plan modu dosyaları. Yeri `plansDirectory` ile değişir | Aynı |
| `debug/` | `--debug` ya da `/debug` açıkken oturum günlükleri | Aynı |
| `shell-snapshots/` | Açılışta alınan kabuk alias ve fonksiyonları | Temiz çıkışta |
| `usage-data/report.html` | `/insights` raporu | Aynı süreyle |
| `history.jsonl` | Yazdığın prompt'lar. Yukarı ok ve `Ctrl+R` buradan okur | Sen silene kadar kalır |
| `todos/`, `statsig/`, `logs/` | Eski sürümlerin dizinleri. Artık yazılmaz | Temizlik içini boşaltır |
| `.credentials.json`, `agent-memory/`, `jobs/`, `daemon/` | Saklanması gereken durum | Silme |

Oturumun geçici çalışma dizini macOS'ta `/private/tmp/claude-<uid>/<proje>/<oturum>/scratchpad/` altındadır. Kayıtla birlikte silinir, işletim sistemi de silebilir. Birden çok gün sürecek işi oraya koyma. [13.3](../README.md#13-gozetimsiz)

## Mahremiyet

Konuşma kayıtları ve `history.jsonl` şifrelenmez. Claude'un okuduğu her şey, bir `.env` dosyasının içeriği dahil, düz metin olarak diske yazılır. Azaltmanın yolları: `cleanupPeriodDays` değerini düşürmek, `CLAUDE_CODE_SKIP_PROMPT_HISTORY=1` ile kayıt tutmamak, headless koşumda `--no-session-persistence`, gizli dosyaya okuma yasağı. [7.1](../README.md#7-guvenlik)

Bir projenin bütün yerel izini `claude purge` siler: kayıtlar, bellek, dosya geçmişi ve `~/.claude.json` içindeki proje girdisi. Önce `--dry-run` ile ne gideceğini gör. 2.1.288'den önceki sürümlerde komutun adı `claude project purge`.

---

[Kontrol listesi](../README.md) · [Rehber](../rehber/README.md) · [Komutlar ve kısayollar](komutlar.md) · [Sorun giderme](sorun-giderme.md) · [İpuçları ve püf noktaları](ipuclari.md) · [Gerçek deneyimlerden on ders](deneyimler.md) · [Terimler sözlüğü](sozluk.md)

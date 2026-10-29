## Zihinsel model: yapılandırma bir bağımlılıktır

Tek başına çalışırken `.claude/settings.json` senin dosyandır. Ekipte çalışırken bu dosya git ile herkesin makinesine gider ve ilk oturumda ne yapacağına sen karar vermezsin, depoyu klonlayan karar verir. Bu yüzden ekip ölçeğinde tek soru şudur: bu dosyayı kim yazdı, kim inceledi, kim çalıştırıyor?

Claude Code ayarı dört sahiple okur. Öncelik yukarıdan aşağıdır: yönetilen ayarlar, komut satırı, `settings.local.json`, `settings.json`, kullanıcı ayarları. Üstteki sahip alttakini ezer.

| Sahip | Dosya | Kime ulaşır | Kim değiştirir |
|---|---|---|---|
| Kurum | `managed-settings.json` (sistem dizini), MDM profili ya da claude.ai konsolu | Politikanın ulaştığı herkes | Yönetici |
| Ekip | `.claude/settings.json` | Depoyu klonlayan herkes | Pull request |
| Kişi, bu proje | `.claude/settings.local.json` | Yalnız sen | Sen |
| Kişi, her proje | `~/.claude/settings.json` | Yalnız sen | Sen |

Belgenin ince bir ayrımı var ve ekip kurarken en çok bu yanıltır: depoda duran ayar her zaman hemen işlemez. `permissions.allow` kuralları, `additionalDirectories` ve `extraKnownMarketplaces` girdileri, her ekip üyesi klasöre güven verdikten sonra geçerli olur. O zamana dek yeni gelen hâlâ izin sorusu görür. Sınırlayan kurallar (`deny`, `ask`) bundan etkilenmez, çünkü yetki vermezler. Kısacası: ekip dosyası bir öneridir, kurum dosyası bir kuraldır. Ayrıntısı için {{bolum:5}} ve {{bolum:6}}.

## Karar kuralları

**Ortak olanı commit'le, kişisel olanı yerelde tut.** Ekibin izin listesi, hook'ları ve ortak plugin'leri `settings.json`'a gider. Kendi modelin, kendi kısayolların `settings.local.json`'a. Claude Code yerel dosyayı oluşturduğunda onu git dışında bırakır. Dosyayı elle oluşturduysan `.gitignore`'a kendin eklemelisin. Bir ekip dosyası senin tercihinle çakışırsa kendi yerel dosyanda ezersin, commit gerekmez. [[10.1]]

**CLAUDE.md'ye kod gibi davran.** Proje CLAUDE.md'sindeki bir satır bütün ekibin oturumunu değiştirir. Değişikliği pull request'ten geçir, gerekçesini commit mesajına yaz. Aksi hâlde altı ay sonra kimse bir kuralın neden orada durduğunu bilmez ve silmeye cesaret edemez. Kişisel tercihler `CLAUDE.local.md`'ye gider, o da gitignore'dadır. Büyük monorepoda başka ekiplerin CLAUDE.md dosyaları seni de etkiler, `claudeMdExcludes` ile hariç tutabilirsin. [[10.2]]

**Tekrar eden işi skill'e çevir, dağıtımı büyüklüğe göre seç.** Bir depoya özgü prosedür `.claude/skills/` altında commit'lenir ve klonlayan herkes alır. Birden çok depoda aynı skill lazımsa plugin yap. Plugin, skill'leri, hook'ları ve MCP sunucularını tek birim olarak taşıyan bir dizindir. Bir marketplace de plugin'leri listeleyen bir kataloktur. Depoya ekleyebilirsin, kurum çapında da dağıtabilirsin. [[10.3]]

**Kuralı Claude'a değil, makineye uygulat.** Kurumun "şu dosya okunmasın" dediği şey `managed-settings.json` içinde `permissions.deny` olarak durur. `allowManagedPermissionRulesOnly: true` ile kullanıcı, proje ve yerel dosyalardaki izin kuralları devre dışı kalır. CLAUDE.md burada yetmez, nedenini {{bolum:5}} anlatıyor.

**Yönetilen ayarı yayma yöntemini altyapına göre seç.** Dört yol var: claude.ai konsolundan sunucu tarafı yönetim, macOS ve Windows için MDM, sistem dizinine bırakılan dosya ve Windows kullanıcı kaydı. Dosya yoluysa macOS'ta `/Library/Application Support/ClaudeCode/`, Linux'ta `/etc/claude-code/` altına koyarsın. Birkaç ekip aynı politikayı paylaşıyorsa her ekip kendi dosyasını `managed-settings.d/` dizinine koyar. Dosyalar alfabetik sırayla birleşir, bu yüzden `10-telemetri.json` ve `20-guvenlik.json` gibi numaralı adlar sıra verir. Listeler birleşir, tekil değerlerde sonraki dosya kazanır. Aynı makineye birden çok kaynak ulaşırsa varsayılan davranış en yüksek öncelikli tek kaynağı kullanmaktır, hepsini birleştirmek için `managedSourcesBehavior: "merge"` gerekir (v2.1.242 ve sonrası). Politikanın gerçekten işlediğini `/status` içindeki `Setting sources` satırından doğrula.

**Duyuruyu hatırlatma için kullan, kural için değil.** `companyAnnouncements` ayarı başlangıçta kurumun duyurusunu gösterir. Birden çok duyuru varsa her oturumda rastgele biri çıkar. İyi bir duyuru kısa bir hatırlatmadır: "Müşteri verisi yalnız kurum hesabıyla." Zorlama yoktur, yalnız görünürlük sağlar.

**Hesap ve veri sınırını baştan çiz.** Şirket işini şirketin onayladığı hesapla yap, çünkü veri politikası hesap türüne bağlı. Belgeye göre Team, Enterprise ve API gibi ticari hesaplarda Anthropic, Claude Code'a gönderilen kod ve prompt'larla model eğitmez (müşteri açıkça aksini seçmedikçe). Free, Pro ve Max hesaplarında eğitim izni ayarı geçerlidir. İç alan adı, müşteri verisi ve iç depo adresleri hiçbir kişisel hesaba ve özel depoya gitmesin. Paylaşmadan önce tarama yaptır. [[7.2]]

**Yeni depodaki hook ve MCP ayarını çalıştırmadan önce oku.** Ortak hook'lar ekip için en güçlü araçtır ve tam bu yüzden en riskli olanıdır: hook senin yetkinle kabukta komut çalıştırır. Ayar dosyalarındaki hook'lar, `env` bloğu ve `apiKeyHelper` gibi yardımcı komutlar güven penceresini göstermeyen `claude -p` ile de çalışır ({{bolum:6}}). Tanımadığın bir depoyu otomasyonda çalıştırmadan önce `.claude/settings.json`, hook betikleri ve `.mcp.json` içeriğini oku. [[7.7]]

**Onboarding'i üret, elle yazma.** `/team-onboarding` son 30 günlük oturum geçmişinden, komutlardan ve MCP kullanımından bir rehber üretir. Yeni ekip üyesi bunu ilk mesaj olarak yapıştırabilir. Team ve Enterprise aboneleri için paylaşılabilir bir bağlantı da döner. Çıktıyı yine de bir insan okusun: geçmişten çıkan alışkanlık ekibin istediği alışkanlık olmayabilir.

## Hata biçimleri

**Kurgu senaryo: "bende çalışıyordu".** Selin'in ekibi `.claude/settings.json` dosyasına bir izin listesi koyar ve herkesin sormadan test çalıştıracağını varsayar. Yeni katılan Volkan depoyu klonlar, güven penceresini kapatıp `claude -p` ile bir betik koşturur. Allow kuralları uygulanmaz, betik izin sorusunda takılır, stderr'e düşen `this workspace has not been trusted` uyarısını da kimse okumaz. Çözüm ekip dosyasını suçlamak değil, yeni gelenin ilk adımına "klasörü interaktif aç, güven penceresindeki kuralları oku" maddesini koymaktır.

**Kurgu senaryo: duyuru kural sanıldı.** Barış, `companyAnnouncements` içine "`.env` dosyasını okuma" yazar ve işi bitmiş sayar. Duyuru yalnız başlangıçta görünür, hiçbir okumayı engellemez. Doğru yer yönetilen `permissions.deny` kuralıdır.

**Gerçek vaka: katman bölünmesi.** {{ek:deneyimler}} sayfasındaki D07, bir kuralın "kesin" sandığın katmana hiç ulaşmadığını gösterir. Proje dışı import headless koşumda yüklenmedi ({{bolum:1}}). Ekip ölçeğinde aynı örüntü şöyle görünür: bir kişide çalışan yapılandırma, başka bir kişinin makinesinde sessizce eksik kalır. Ayırıcı kanıt, kuralı gerçekten çalıştıran oturumda "bu kural ne diyor?" diye sormaktır.

**Plugin deposu ayarıyla yetinmek.** Marketplace girdisi göreli yolla listelenmiş bir plugin, deponun ayarından kurulur. Plugin dış bir kaynağa işaret ediyorsa yalnız ayarla kurulmaz. Her katılımcı önce `claude plugin install <ad>@<marketplace> --scope project` komutunu çalıştırır, o zamana dek "enabled in project settings but isn't installed" uyarısını görür.

## Alıştırma: ekip paketi ve temiz klon

Bunu bir deneme deposunda yap.

1. Depoda `.claude/settings.json` oluştur. İçine bir `permissions.deny` kuralı koy, örneğin `Read(./.env)`, ve `permissions.allow` altına yalnız bir salt okunur komut ekle.
2. Depoya bir skill ekle: `.claude/skills/ozet/SKILL.md`. Skill, açıklaması "değişen dosyaları özetler" olan üç satırlık bir prosedür olsun.
3. `.claude/settings.local.json` oluştur ve kendi kişisel bir tercihini yaz. Dosyanın git dışında kaldığını `git status` ile gör.
4. Her şeyi commit'le, ardından depoyu başka bir dizine klonla: `git clone <depo> ../temiz-klon`.
5. Temiz klonda yeni bir oturum aç. Güven penceresindeki kuralları oku, kabul et, sonra `/ozet` komutunu çalıştır. `.env` okumasını dene ve reddedildiğini gör.
6. Aynı skill'i bir plugin'e çevir: `ekip-paketi/.claude-plugin/plugin.json` ve `ekip-paketi/skills/ozet/SKILL.md`. `claude --plugin-dir ./ekip-paketi` ile yükle. Skill artık `/ekip-paketi:ozet` adıyla görünür.

**Bitti sayılması için:** temiz klondan alınmış üç kanıt: güven penceresinin listelediği kurallar, `/ozet` çıktısı ve reddedilen `.env` okuması. Altına bir cümle yaz: kişisel tercihin klona geçmediğini nereden gördün.

## Bağlantılar

Kontrol listesi: [[10.1]] [[10.2]] [[10.3]] [[7.2]] [[7.7]]. Önceki bölüm: {{bolum:10}}. Ekler: {{ek:dosyalar}}, {{ek:komutlar}}, {{ek:deneyimler}}.

## Zihinsel model: üç ayrı soru, üç ayrı katman

İzin ve güvenlik tek bir konu gibi görünür ama üç ayrı soruya cevap verir. Her sorunun cevabı farklı bir katmandan gelir. Katmanları karıştırırsan yanlış yere kural yazarsın.

| Soru | Katman | Kim uygular |
|---|---|---|
| Claude bu aracı sormadan kullanabilir mi? | İzin modu ve izin kuralları | Claude Code |
| Çalışan komut makinede neye erişebilir? | Sandbox | İşletim sistemi |
| Okuduğu metin Claude'u yönlendirebilir mi? | Dış içeriğe güvenmeme alışkanlığı, onay noktaları | Sen ve auto modundaki sınıflandırıcı |

İlk katmanı {{bolum:5}} içinde gördün: izin kuralını Claude Code uygular, model uygulamaz. Belge bunu açık yazar: prompt ve CLAUDE.md Claude'un ne denediğini şekillendirir, Claude Code'un neye izin verdiğini değiştirmez. Bu bölüm o katmanı derinleştirir ve diğer ikisini yanına koyar.

Kuralların nasıl bir araya geldiğini tek cümleyle hatırla: deny önce gelir, sonra ask, sonra allow. İlk eşleşen kazanır ve kuralın ne kadar özel olduğu sırayı değiştirmez. Geniş bir deny kuralı, dar bir allow kuralının açtığı kapıyı kapatır. Allow kuralıyla deny kuralından istisna çıkaramazsın. Bir PreToolUse hook'u "allow" dese bile deny ve ask kuralları yine değerlendirilir.

{{sekil:b06-izin-karar-sirasi|Bir araç çağrısının geçtiği sıra. İlk beş basamak Claude Code içinde karar verir, altıncı basamak komut çalışırken devreye girer}}

Şekilde dördüncü basamaktan sonra gelen mod, kural yazılmamış durumda geçerli olan varsayılandır. Hook'un exit 2 verdiği çağrı bu sıranın dışında, en başta durur.

## İzin modları: hangisi ne zaman

Mod, kural yazılmamış durumda Claude'un neyi sormadan yapabileceğini belirler. Kurallar modun üstüne biner. Belgedeki tabloyu kendi cümlelerimle özetliyorum:

| Mod | Sormadan ne yapar | Ne zaman seç |
|---|---|---|
| `default` (arayüzde Manual) | Yalnız okuma | Hassas iş, tanımadığın kod |
| `acceptEdits` | Okuma, çalışma dizinindeki dosya düzenlemeleri, `mkdir`, `mv`, `cp` gibi basit dosya komutları | Sonucu `git diff` ile sonradan inceleyeceğin iş |
| `plan` | Okuma ve araştırma, düzenleme yok | Değiştirmeden önce depoyu anlamak |
| `auto` | Hemen her şey, ama arka planda bir sınıflandırıcı model her işlemi gözden geçirir | Yönünü güvendiğin uzun işler |
| `dontAsk` | Yalnız önceden izin verilenler, sorulacak her şey reddedilir | CI ve kilitli betikler |
| `bypassPermissions` | Hemen her şey, güvenlik kontrolleri kapalı | Yalnız yalıtılmış konteyner ya da sanal makine |

Üç ayrıntı kararını değiştirir.

- **`auto` güvenlik garantisi değildir.** Belge uyarıyı kendisi yazar: istem sayısını azaltır, hassas işlemde incelemenin yerini tutmaz. Belge, `auto`'nun v2.1.283 ve sonrasında terminal ve VS Code için yerleşik başlangıç modu olduğunu söylüyor. Yerel sürüm 2.1.284 bu eşiğin üstünde. Yani oturum senin seçmediğin bir modda açılmış olabilir. Başlangıçta durum çubuğuna bak.
- **`dontAsk` kuralsız çalışmaz.** Hiçbir şey sormadığı için eksik allow girdisi sessiz ret demektir. CI'da bunu istersin, etkileşimli işte istemezsin.
- **`bypassPermissions` her şeyi açmaz.** Allow kuralları bu modda etkisizdir ama deny kuralları yine çalışır. `rm -rf /` gibi tanınan kritik silmeler ve açık ask kuralları yine sorar. Belge bu modu internetsiz konteyner ve sanal makine için ayırır.

Başlangıç modu şu sırayla belirlenir: komut satırı bayrağı, sonra ayar dosyasındaki `defaultMode`, sonra yerleşik varsayılan. Bir tuzak var. Belgeye göre `.claude/settings.json` ya da `.claude/settings.local.json` içine `bypassPermissions` yazarsan değer etkisizdir ve oturum Manual başlar. `claude -p` ile açılan oturum ise yerleşik olarak `default` ile başlar.

Bayrağın bu makinedeki sürümde kabul ettiği değerleri yardım çıktısından okuyabilirsin:

```terminal Gerçek çıktı, kısaltılmış
$ claude --version
2.1.284 (Claude Code)
$ claude --help
  --permission-mode <mode>   Permission mode to use for the session
                             (choices: "acceptEdits", "auto",
                             "bypassPermissions", "manual",
                             "dontAsk", "plan")
```

- **2. satır:** sürüm. Bu bölümdeki sürüm iddiaları 2.1.284 içindir.
- **4. ile 7. satır:** bayrağın kabul ettiği altı değer. Tablodaki altı modun hepsi burada var, yalnız ilk mod yardımda `manual` adıyla geçiyor. Belgeye göre arayüz bu modu Manual diye gösterir, ayar değeri `default`'tur ve hook'lar da bu adı görür. CLI ikisini de kabul eder: `--permission-mode manual` ile `"defaultMode": "default"` aynı modu açar.
- Çıktı yardım metninden kesildi, başka bayraklar çıkarıldı.

## Dar allow girdisi

Kuralın genişliği riskini belirler. Üç davranışı bil.

**Yıldızı alt komuttan sonra koy.** `Bash(git log *)` yalnız `git log` komutlarını açar. `Bash(git *)` push, reset ve clean dahil bütün git'i açar. Belge, alt komuttan önce yıldız içeren allow kuralları için başlangıçta uyarı verdiğini söyler. [[6.3]]

**Bileşik komutta her parça ayrı değerlendirilir.** `Bash(npm test *)` kuralı `npm test && curl ...` komutunun tamamını açmaz. `&&`, `||`, `|`, `&`, noktalı virgül ve satır sonu ayırıcıdır. Her parça ayrı izinli olmalı. Bu yüzden komutu tek parçada yazmak sorudan kurtarır. [[6.4]]

**Sarmalayıcıların bir kısmı atlanır, bir kısmı atlanmaz.** `timeout`, `time`, `nice`, `nohup`, `stdbuf` ve bilinen güvenli birkaç ortam değişkeni atılır, yani `NODE_ENV=test npm test` yine `npm test` kuralına uyar. `npx`, `docker exec` ya da `devbox run` gibi ortam çalıştırıcıları atılmaz. `Bash(devbox run *)` yazarsan `devbox run rm -rf .` da geçer. Çözüm, çalıştırıcıyı ve iç komutu birlikte yazmaktır: `Bash(devbox run npm test)`.

### Komutu motorun eşleştirebileceği biçimde yaz

İzin motoru komut metnini statik eşleştirir. Metnin neye çözüleceğini bilemediği bir parça görünce kuralı uygulamaz ve sorar. `$(...)` ve `${...}` genişletmeleri, `source venv/bin/activate` ile aktive edilen ortamlar, bir `&&` zincirinin içindeki kuralsız tek halka bu gruptandır. Çözüm yeni bir allow girdisi değil, komutu o parça olmadan yazmaktır: venv'i aktive etmek yerine yorumlayıcıyı doğrudan çağır, `.venv/bin/python -m pytest`. Belge güvenlik bölümünde, Claude Code'un tam çözümleyemediği bir Bash komutunu Manual modda sorduğunu ve bir kısmına verilen allow kuralının bu soruyu atlatmadığını yazar. Beklenmedik bir istem gördüğünde önce komutu sadeleştir. [[6.4]]

## Sandbox ve izin kuralı aynı şey değil

İzin kuralı komutun metnine bakar. Sandbox komutun ne yaptığına bakar. Belge farkı şöyle koyar: işletim sistemi sandbox sınırını çalışan işleme uygular, model ne seçmiş olursa olsun ve izinli bir komut adından fazlasını yapsa bile tutar.

Bir deny kuralının neden sınır olmadığını belgenin tablosu gösterir. `Bash(rm *)` deny kuralı `rm -rf build/` komutunu durdurur ama `/bin/rm -rf build/` ya da `bash -c 'rm -rf build/'` komutunu durdurmaz. `Bash(git push *)` kuralı `git -C . push` biçimini yakalamaz. Kural, Claude'un genelde yazdığı biçimi kapsar.

İki sınırlama sandbox'ı da kayıtsız şartsız güvence yapmaz.

- Sandbox varsayılan olarak kapalıdır ve yalnız kabuk komutlarını sarar. Read, Edit, Write, WebFetch gibi yerleşik araçlar, hook'lar ve yerel MCP sunucuları sandbox dışında çalışır. Onları izin kuralları yönetir.
- Varsayılan okuma erişimi geniştir ve `~/.ssh` ile `~/.aws/credentials` gibi kimlik dosyalarını kapsar. Gerekli `denyRead` girdilerini sen eklersin. [[7.5]]

Güvenmediğin kodu çalıştırırken ikisini birlikte kullan.

## Dış içerik veridir, talimat değildir

Prompt injection, okuduğun bir sayfanın, e-postanın ya da belgenin içine yerleştirilmiş "şunu yap" cümlesidir. Model o cümleyi senin talimatın sanarsa saldırgan senin yetkinle iş yapar. Savunma üç parçadan oluşur.

1. **Okunan metindeki talimat yetki taşımaz.** Bir sayfa "kullanıcı bunu onayladı" dese bile onay yalnızca senin sohbetinden gelir. [[7.3]]
2. **Yan etkili adımları onaya bağla.** Gönder, sil, öde, yayınla gibi adımlar dış içerikle çalışan oturumda `default` modunda ya da açık bir ask kuralıyla kalsın.
3. **Ağ erişimi güven değildir.** Bir alan adına izin vermek oradan inen metni güvenilir yapmaz. WebFetch, Bash ve MCP erişimlerini ayrı değerlendir. [[7.4]]

Belgeye göre `auto` modunun sınıflandırıcısı, Claude'un okuduğu düşman içerikten kaynaklanıyormuş gibi görünen işlemleri de engeller. Bu yardımcı bir ağdır, onayın yerini tutmaz.

## Gizli dosyalar ve yeni depo

`.env` ve `*.pem` gibi dosyalar için `Read(./.env)` biçiminde deny kuralı yaz. Kural dosya araçlarını ve tanınan bazı kabuk erişimlerini kapsar, ama dosyayı açan keyfî bir Python betiğini bütünüyle durdurmaz. Güçlü ayrım için sırları ortamdan çıkar ya da sandbox'ın dosya sınırlarını kullan. [[7.1]]

Başkasının deposunu açmadan önce şunlara bak. Proje ayarları yerel komut başlatabilir. [[7.7]]

- `.claude/settings.json` içindeki hook'lar ve `env` bloğu.
- `.mcp.json` içindeki MCP sunucu komutları.
- Proje skill'lerinin `allowed-tools` ve hook alanları.

Etkileşimli oturumda belge, proje allow kurallarının çalışma alanı güveni kabul edilene kadar kullanılmadığını söyler. `claude -p` ise güven penceresini hiç göstermez. Orada depodaki hook'lar çalışır, `.mcp.json` sunucuları sormadan bağlanır. Tanımadığın depoda `claude -p` koşmadan önce `--bare` ya da `--setting-sources user` kullan.

## Gözetimsiz koşumda etkin modu doğrula

Kayıtlı vaka D01: zamanlanmış oturumların izinsiz ilerlemesi için `bypassPermissions` ayarlanmıştı. Bir projenin 43 oturum kaydındaki 345 mod değeri tarandı ve bu mod hiç görünmedi. Oturum hata vermeden varsayılan moda düşmüştü. Ders, ayarladığın modla oturumun açıldığı modun ayrı şeyler olması. Ayırıcı kanıt, oturum kaydındaki etkin mod değeridir, ayar dosyasındaki değer kanıt sayılmaz. Belge bu vakanın nedenini anlatmaz ama iki ilgili gerçeği yazar. Proje ayar dosyalarına yazılan `bypassPermissions` etkisizdir. `-p` oturumu güven penceresini hiç göstermediği için, klasör daha önce güvenilmediyse projenin allow kuralları da kullanılmaz. Hook girdisinde `permission_mode` alanı da bulunur, istersen bir hook modu log'a yazsın.

Gözetimsiz iş kurarken sırayla şunu yap: modu bayrakla ver, etkin modu kayıttan oku, allow listesini zararsız bir komutla dene. Çalışmayan adımı sessizce geçme, nedenini yaz. [[6.7]]

## Karar kuralları

- **Hassas işte `default`, kendi gözden geçireceğin işte `acceptEdits`, yönünü güvendiğin uzun işte `auto`.** `bypassPermissions` yalnız yalıtılmış kutuda.
- **Tekrar eden istemi azaltmak için önce kaydı oku.** `/fewer-permission-prompts` transcript'lerinden salt okunur komut önerir. Her girdiyi tek tek oku. Yazma ya da yayın komutu içerenleri alma. [[6.6]]
- **Yıkıcı komutu deny'a koy ama sınır sanma.** Gerçek sınır gerekiyorsa sandbox ya da komut içeriğine bakan bir hook ekle. [[6.2]]
- **Allow kuralını alt komut düzeyinde yaz, yıldızı sona koy.** [[6.3]]
- **Bir komut allow'da olduğu halde soruyorsa içinde genişletme, aktivasyon ya da zincir ara.** [[6.4]]
- **Mod adını güvenlik kanıtı sayma.** Zararsız bir deneme komutuyla gerçek davranışı gör. [[6.7]]

## Hata biçimleri

**Gerçek vaka: ayarlanan mod, oturumun modu değildi.** D01 yukarıda. Ayrıntısı {{ek:deneyimler}} sayfasında.

**Kurgu senaryo: geniş joker.** Deniz'in ekibi tekrar eden istemden bıkıp `Bash(git *)` ekler. Birkaç hafta sonra Claude bir birleştirme çözerken `git clean -fd` komutunu sormadan çalıştırır ve izlenmemiş dosyalar silinir. Kuralın amacı `git status`, `git diff` ve `git commit` idi. Dar liste bunları tek tek sayardı ve yıkıcı komutlar sorulurdu.

## Alıştırma: bir haftalık kullanımdan dar bir allow listesi

Herhangi bir git deposunda yap. Yazma ya da silme yok, yalnız ayar dosyası değişir.

1. Bir hafta boyunca normal çalış. `/fewer-permission-prompts` oturum kayıtlarını tarar, ayrıca not tutman gerekmez.
2. Bir oturumda `/fewer-permission-prompts` çalıştır. Önerdiği listeyi dosyaya yazdırmadan önce ekrana getirt.
3. Her girdi için üç sütunlu bir tablo yap: girdi, neden güvenli, neyi yanlışlıkla açar. Örneğin `Bash(git status *)` için "yalnız okur", `Bash(npm run *)` için "package.json'daki her betiği açar, betikler incelenmiş mi?"
4. Gerekçesini yazamadığın girdiyi at. Yazma ya da yayın yapan girdiyi (`git push`, `deploy`) at.
5. Kalan listeye bir de `deny` bölümü ekle: en az `Read(./.env)` ve `Bash(git push *)`.
6. Listeyi `.claude/settings.json` içine koy. Yeni oturumda biri listede biri listede olmayan iki zararsız komutla dene ve beklenen davranışı gör.

**Bitti sayılması için:** her girdinin gerekçesini taşıyan tablo, atılan girdilerin listesi ve tek bir cümle: bu liste neyi bilerek açmıyor. İki denemenin sonucunu da ekle.

## Bağlantılar

Kontrol listesi: [[6.1]] [[6.2]] [[6.3]] [[6.4]] [[6.5]] [[6.6]] [[6.7]] [[7.1]] [[7.3]] [[7.4]] [[7.5]] [[7.7]]. Önceki bölüm: {{bolum:5}}. Gerçek vaka: D01, {{ek:deneyimler}}. Ekler: {{ek:komutlar}}, {{ek:sorun-giderme}}.

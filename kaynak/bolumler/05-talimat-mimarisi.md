## Zihinsel model: rica ile garanti

Claude Code'a bir kuralı iki türlü verebilirsin. Ya Claude'a söylersin, ya da Claude Code'a uygulatırsın. Belge bu ikisini ayrı adlarla anar. Birinde **Claude karar verir**: prompt, CLAUDE.md, kural dosyası ve Claude'un kendi seçtiği skill'ler. Ötekinde **Claude Code uygular**: hook, deny kuralı ve yönetilen ayar. İlki çoğu zaman tutar. İkincisi her zaman tutar.

Bu ayrım CLAUDE.md'nin nasıl iletildiğinden gelir. CLAUDE.md sistem prompt'unun parçası değildir. Sistem prompt'undan sonra bir kullanıcı mesajı olarak modele verilir. Belge bunu açıkça yazar: Claude bu dosyaları bağlam olarak görür, zorlanan yapılandırma olarak değil, ve sıkı uyumun garantisi yoktur. Hook ise modelin kararına hiç girmez. Olayı gelince çalışır, Claude ne düşünürse düşünsün.

| Katman | Kim karar verir | Ne zaman yüklenir | Ne için |
|---|---|---|---|
| CLAUDE.md | Claude | Her oturumda | Her konuşmada geçerli bağlam: komutlar, tuzaklar, tercihler |
| `.claude/rules/` | Claude | Eşleşen dosyaya dokununca | Yalnız belli dosyalarda geçerli kural |
| Skill | Claude seçer, sen `/ad` ile zorlayabilirsin | Açıklama her zaman, gövde çağrılınca | Tekrarlanan prosedür |
| Alt ajan | Claude | Çağrılınca, kendi penceresinde | Yalıtılmış iş, sonuç özet döner |
| Hook (`command`, `http`) | Claude Code | Olayı gelince | Her seferinde olması gereken şey |
| Deny kuralı, yönetilen ayar | Claude Code | Her araç çağrısından önce | Hiçbir zaman olmaması gereken şey |
| Sandbox | İşletim sistemi | Her kabuk komutunda | Komut adından fazlasını yapsa bile tutan sınır |

Belgenin hook ile skill karşılaştırmasındaki iki cümle bütün bölümü özetler: skill "bir rica, garanti değil". Korkulukları hook'a koy.

## Karar kuralları

**İstisnası olmayan şey kesin katmana gider.** Belge bunu tek cümleyle söyler: bir şey her seferinde olmak zorundaysa onu hook, deny kuralı ya da yönetilen ayar yap. `.env` okunmayacaksa bu bir CLAUDE.md satırı değil, deny kuralıdır. Commit'ten önce testler koşacaksa bu bir hook'tur. [[7.1]] [[7.6]]

**Geri kalan her şeyi Claude'a bırak.** Belge burada da açık: çoğu zaman Claude'un karar vermesini istersin. Kırk hook'a ulaştıysan çoğu kural değil tercihtir. Kesin katman bakım ister, her hook test ister ve yanlış yazılmış bir hook işi tamamen durdurur. [[8.4]]

**Vurguyla uyum satın alınmaz.** Bir kural çiğneniyorsa başına IMPORTANT eklemek belgenin deyişiyle büyük olasılıkla düzeltmez. Eski modeller vurguya ihtiyaç duyuyordu. Güncel modeller düz yazılmış bir satırı izler, vurgu yığmak kuralı fazla uygulatır. Vurgu eklemeye devam ediyorsan o satır hook'a aittir. [[1.1]]

**CLAUDE.md'yi kısa tut.** Belge dosya başına 200 satırın altını hedefler. Uzun dosya hem bağlam harcar hem uyumu düşürür. Çelişen iki talimattan Claude birini rastgele seçebilir. Uzun prosedür skill'e, belli dosyalara özgü kural `.claude/rules/` altına gider. [[1.2]] [[1.4]]

**Yol kuralının bir bedeli var.** `paths` deseniyle yüklenen kural konuşma geçmişine girer. Sıkıştırmada özetlenip kaybolabilir, ancak eşleşen dosyaya yeniden dokununca geri gelir. Oturum boyunca kesin geçerli olması gerekiyorsa `paths` alanını kaldır ya da kökteki CLAUDE.md'ye taşı.

**Skill'in açıklaması tetiğidir.** Claude işini skill açıklamalarıyla karşılaştırıp hangisinin ilgili olduğuna kendisi karar verir. Açıklama belirsizse ya da başka bir skill'le örtüşüyorsa yanlış skill yüklenir ya da hiç yüklenmez. Mutlaka çalışması gerekiyorsa `/ad` ile kendin çağır. Yan etkili bir skill'i otomatik çağrıya `disable-model-invocation: true` ile kapat. [[9.3]] [[9.4]]

**Her hook kesin değildir.** `command` ve `http` tipindeki hook kesindir. `prompt` ve `agent` tipindeki hook kararı başka bir modele bırakır, belgeye göre bunlar da kesin değildir. Hook'un kendisi çökerse eylemi de durdurmak istiyorsan hata politikasını buna göre seç. [[8.5]]

**Deny kuralı bir güvenlik sınırı değildir.** Bash kuralları komutun metnini eşler, niyetini değil. `Bash(rm *)` kuralı `/bin/rm` ya da `bash -c 'rm ...'` biçimini durdurmaz. Bir dosyaya okuma yasağı `cat .env`'i yakalar ama dosyayı açan bir betiği yakalamaz. Gerçek sınır işletim sistemi düzeyindeki sandbox'tır. O da yalnız kabuk komutlarını sarar. Dosya okuma ve düzenleme araçları, web araçları ve hook'lar sandbox dışında çalışır, onları izin kuralları yönetir. Belge ikisini birlikte kullanmayı önerir. [[6.2]] [[7.5]]

## Bir kuralın yerini bulmak

Belgenin önerdiği tetikler kısa bir karar listesi verir:

| Gözlem | Yeri |
|---|---|
| Claude aynı şeyi iki kez yanlış yaptı | CLAUDE.md |
| Aynı uzun prompt'u tekrar tekrar yazıyorsun | Skill |
| Bir yan iş konuşmayı çıktıyla boğuyor | Alt ajan |
| Bir şeyin sormadan her seferinde olması gerekiyor | Hook |
| Bir şeyin hiçbir zaman olmaması gerekiyor | Deny kuralı, gerekirse sandbox |
| Aynı kurulum ikinci bir depoda da lazım | Plugin |

## Hata biçimleri

**Gerçek vaka: metin kuralı yeni oturuma ulaşmadı.** Dört paralel oturum aynı anda derleme koştu, makinenin yükü 720'ye çıktı. Oturumlara "ağır komutu kilitle sar" diye talimat verildi. Bir oturum kilitsiz bir derleme başlattı ve sonradan durdurmak zorunda kaldı. Metin kuralı o anki oturumlara ulaştı, yenilerine ve başka projelere ulaşmadı. Çalışan çözüm kesin katmandaydı: ağır komutları kilitle koşturan bir sarmalayıcı ve sırasız ağır komutu reddeden bir PreToolUse hook'u. Hook 16 vakalık bir testle sınandı. Ayrıntısı {{ek:deneyimler}} sayfasında D08.

**Gerçek vaka: kesin sandığın katman hiç yüklenmedi.** Proje dışı bir dosyayı import eden CLAUDE.md, headless koşumda içeriği yüklemedi. Çözüm aynı bilgiyi her oturumda bağlama koyan bir SessionStart hook'u oldu. Burada hook kuralı uygulatmadı, yalnız bağlama girmesini garanti etti. Kuralın kendisi yine Claude'un kararındaydı. Ayrıntısı D07.

**Kurgu senaryo: çoğu zaman tutan kural.** Mert'in ekibi CLAUDE.md'ye "commit'ten önce tip kontrolünü çalıştır" yazar. Haftalarca sorun çıkmaz. Bir gün uzun bir oturumun sonunda Claude tip kontrolünü atlayıp commit atar, kırık kod ana dala girer. Belge tam bu satırı örnek verir: çoğu zaman çalışır, her zaman değil. Ekip kuralı bir hook'a taşır. Artık tip kontrolü geçmeyen commit hiç oluşmaz.

## Alıştırma: aynı kuralı üç katmanda dene

Bunu gerçek bir iş deposunda değil, bu iş için açtığın bir deneme deposunda yap.

1. Depoya içinde sahte bir değer olan bir `.env` dosyası koy, ör. `DENEME_ANAHTARI=12345`.
2. **Rica katmanı.** CLAUDE.md'ye "`.env` dosyasını okuma" yaz. Yeni oturumda Claude'dan `.env` içindeki değeri söylemesini iste. Ne olduğunu kaydet.
3. **Kesin katman.** CLAUDE.md satırını sil. `.claude/settings.json` içine `Read(./.env)` için deny kuralı ekle. Yeni oturumda aynı isteği yap. Sonra Claude'dan değeri `cat .env` ile okumasını iste. İkisinin sonucunu kaydet.
4. **Kuralın sınırı.** Claude'dan `.env` dosyasını okuyup değeri yazdıran küçük bir betik yazmasını ve çalıştırmasını iste. Deny kuralı bunu durdurdu mu?
5. Platformun destekliyorsa `/sandbox` ile sandbox'ı aç ve 4. adımı tekrarla.

**Bitti sayılması için:** dört satırlık bir tablo. Her satırda katman, deneme ve sonuç olsun. Altına bir cümle yaz: bu depoda `.env`'i gerçekten koruyan katman hangisi. Sonra deneme deposunu sil.

## Bağlantılar

Kontrol listesi: [[1.1]] [[1.2]] [[1.4]] [[6.2]] [[7.1]] [[7.5]] [[7.6]] [[8.4]] [[8.5]] [[9.3]] [[9.4]]. Önceki bölüm: {{bolum:1}}. Ekler: {{ek:ipuclari}}, {{ek:dosyalar}}.

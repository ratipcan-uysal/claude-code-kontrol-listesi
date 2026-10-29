## Zihinsel model: olay gelir, betik karar verir

{{bolum:5}} rica ile garanti ayrımını kurdu. Hook, garanti tarafının en esnek aracıdır. Claude Code yaşam döngüsünde belirli noktalara geldiğinde senin betiğini, HTTP isteğini ya da küçük bir model çağrısını çalıştırır. Betik olay hakkında JSON girdisi alır. Çıktısıyla işlemi durdurur, bağlama bilgi ekler ya da sessiz kalır. Model araya girmez, çünkü Claude ne düşünürse düşünsün olay geldiği anda hook çalışır ve kararını kendi başına verir.

Hook'u anlamak için üç şeyi bil: ne zaman çalıştığı, neye bakarak seçildiği ve çıkışının neyi etkilediği.

**Ne zaman çalışır?** Olaylar üç tempoda gelir. Oturum başına: `SessionStart`, `SessionEnd`. Tur başına: `UserPromptSubmit`, `Stop`. Araç çağrısı başına: `PreToolUse` (araç çalışmadan önce, durdurabilir) ve `PostToolUse` (araç çalıştıktan sonra, geri alamaz). Bunların yanında `PermissionRequest`, `SubagentStop`, `PreCompact`, `Notification` gibi daha özel olaylar vardır. Tam liste {{ek:komutlar}} ekinde ve belgenin hook referansında durur.

**Neye bakarak seçilir?** `matcher` alanı, olayın ilgili alanına göre hook'u süzer. Araç olaylarında araç adıdır: `Bash`, `Edit|Write`, `mcp__.*`. `SessionStart` için oturumun nasıl başladığıdır: `startup`, `resume`, `clear`, `compact`. Claude Code, yalnız harf, rakam, alt çizgi, tire, virgül ve `|` içeren değeri tam eşleşme listesi sayar. Başka bir karakter girerse JavaScript düzenli ifadesi olur ve değerin herhangi bir yerinde eşleşir. `Edit.*` hem `Edit` hem `NotebookEdit` ile eşleşir, tam eşleşme için `^Edit$` yaz.

Bir de `if` alanı var. İzin kuralı sözdizimiyle yazılır, örneğin `Bash(git *)`. Hook yalnız çağrı bu kalıba uyarsa çalışır, böylece her komutta betik başlatmazsın. Belge iki sınır koyar. Claude Code `if` alanını yalnız araç olaylarında (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`) değerlendirir. Diğer olaylarda `if` olan hook hiç çalışmaz. İkincisi, `if` en iyi çabayla süzer: Claude Code komutun neyi çalıştıracağını çözemezse hook'u yine de çalıştırır. Kesin izin ya da ret için hook'a değil izin sistemine güven.

## Çıkış kodu ve JSON karar

Hook'un sonucunu iki yoldan bildirebilirsin. Birini seç, karıştırma.

| Çıkış | Anlamı |
|---|---|
| 0, çıktı yok | Karar yok. Normal izin akışı sürer. Sessiz kalmak onay vermek değildir |
| 2 | Engelleyebilen olayda işlemi durdurur. Stderr gerekçe olur ve Claude'a gider |
| Başka kod, başlatılamama, bozuk JSON | Engellemeyen hata. İşlem devam eder, yalnız bir bildirim görürsün |

Bu tablonun son satırı bölümün en önemli cümlesidir. Betiğin çökerse, yolu yanlışsa ya da bozuk JSON basarsa Claude Code işlemi yine yapar. Güvenlik kapısı olan bir hook'ta bunu istemezsin. İki çözüm var: kapalı hata yönünü betikte kendin yaz (hata yakalayınca `exit 2`) ya da hook'a `"onFailure": "block"` ekle. İkincisi komut ve HTTP hook'ları için geçerli ve belgede v2.1.295 ve sonrasını gerektirir. Yerel sürüm 2.1.284 olduğundan bu makinede alan etkisiz kalır. Eski sürümde yokmuş gibi davran ve çözümü betiğe yaz.

Exit 2 ne yapar, olaya göre değişir. `PreToolUse` araç çağrısını durdurur. `UserPromptSubmit` istemi Claude'a ulaşmadan reddeder. `Stop` Claude'un durmasını engeller ve konuşmayı sürdürür. `PostToolUse` ise geri alamaz, çünkü araç çalışmıştır, yalnız stderr'i Claude'a gösterir. `SessionStart` stderr'i yalnız sana gösterir. Bir olayı engelleyici saymadan önce belgedeki "Exit code 2 behavior per event" tablosuna bak. [[8.4]]

JSON yoluyla daha ince karar verirsin. Exit 0 ile tek bir JSON nesnesi yazdırırsın. `PreToolUse` için karar `hookSpecificOutput` içinde olur: `permissionDecision` değeri `allow`, `deny`, `ask` ya da `defer`, yanında `permissionDecisionReason`. Birden çok hook farklı karar verirse öncelik `deny`, `defer`, `ask`, `allow` sırasıdır. Stdout'ta JSON dışında tek satır metin (kabuk profilinin bastığı bir karşılama satırı gibi) nesnenin okunmasını bozar.

Hook kararı izin kurallarını delmez. Belgeye göre bir hook `allow` dese bile Claude Code eşleşen deny ve ask kurallarını değerlendirir. Ters yönde exit 2 ile bloklayan hook, izin kuralları değerlendirilmeden çağrıyı durdurur. Bu yüzden "Bash'i tamamen aç, ama şu üç komutu engelle" düzeni çalışır: `Bash` allow'da, engelleyen hook yanında. [[7.6]]

## Hook'un gücü: hangi tip kesin?

Beş hook tipi var: `command`, `http`, `mcp_tool`, `prompt`, `agent`. {{bolum:5}} içinde gördüğün gibi `command` ve `http` kesindir, kod çalışır ve ne yazdıysan onu yapar. `prompt` ve `agent` tipi kararı başka bir modele bırakır. Belge prompt hook'unu, hook girdisini bir Claude modeline verip karar JSON'u alan tek turluk değerlendirme olarak anlatır. Karar bir modelden geldiği için belgenin iyi uygulamalar sayfası bu tipi de kesin saymaz. Garanti gereken yerde `command` kullan. `SessionStart` zaten yalnız `command` ve `mcp_tool` kabul eder.

Aynı olaya eşleşen hook'lar paralel çalışır. Bunun sonucu şu: birinin diğerinin çıktısına dayandığı düzen bazen tutar, bazen tutmaz, bu yüzden sıraya bağlı adımları tek betikte birleştir ve paralel hook'lar aynı dosyaya yazıyorsa onları ayrı dosyalara yazdır. Aynı tanımı birden çok ayar dosyasında yazarsan yalnız bir kez çalışır. [[8.7]]

### async: bekletmeyen, durduramayan

`async: true` hook'u arka plana atar. Claude beklemez ama durdurulamaz da: `decision`, `permissionDecision` ve `continue` alanları async hook'ta etkisizdir. `asyncRewake` hook exit 2 verince Claude'u uyarır ama işlemi engellemez, çünkü işlem çoktan bitmiştir. `claude -p` oturumu bitince Claude Code hâlâ çalışan async hook'u iptal eder. Kural basit: engellemesi gereken hook'u hiç async yapma, bildirim, log ve yavaş biçimlendirme gibi işleri ise rahatça async'e ver. [[8.6]]

## Hook'u sına, sonra bozarak düştüğünü gör

Hook hiçbir şeye bakmasa da sessizce "çalışır". `/hooks` yapılandırmayı gösterir, doğru çalıştığını göstermez. Sınama için olayın JSON girdisini elle ver ve çıkış kodunu oku. Üç vaka yeter: izinli, yasak, bozuk girdi. Sonra hook'u bilerek boz ve testin düştüğünü gör. [[8.4]]

## Hata biçimleri

**Gerçek vaka D08: metin kuralı ulaşmadı, hook ulaştı.** {{bolum:5}} içinde anlatılan vakada çalışan yol, sırasız ağır komutu reddeden bir PreToolUse hook'uydu. Hook 16 vakalık testle sınandı ve sıfır yanlış verdi. Hafif komut istisnası bilerek bozulunca iki yanlış verdi, yani test gerçekten bakıyordu. Tek yuvanın fazla dar çıktığı da kaydedildi. Ayrıntısı {{ek:deneyimler}} içinde.

**Gerçek vaka D07: hook kuralı uygulatmadı, bağlama girmesini garanti etti.** Proje dışı import headless koşumda yüklenmedi ({{bolum:1}}). Aynı içeriği her oturumda bağlama koyan bir SessionStart hook'u çözümü oldu ve model kuralı kelimesi kelimesine aktardı. Hook burada kuralı zorlamadı, sadece Claude'un gördüğü şeyi garanti etti. Doğrulama: dosya okuma araçları kapalı bir headless oturumda "bu kural ne diyor?" diye sormak. [[8.1]]

**Kurgu senaryo: sessizce açık bırakan kapı.** Cem'in ekibi `.claude/hooks/kontrol.js` betiğini bir `PreToolUse` hook'una bağlar. Bir refactor sırasında biri betiği başka klasöre taşır. Hook artık başlamaz, bu engellemeyen bir hatadır, yalnız transkriptte bir uyarı çıkar. İki hafta boyunca kontrol çalışmaz ve kimse fark etmez. Ekip `onFailure: "block"` alanını ekler ve sürümü v2.1.295 üstüne çıkarır, ayrıca testi CI'a bağlar: betik yoksa test düşer.

## Karar kuralları

- **Her seferinde olması gerekiyorsa `command` ya da `http` hook'u yaz.** Garanti `prompt` ve `agent` tipinde yok.
- **Engellemesi gereken hook senkron olsun.** Async yalnız bildirim ve log için.
- **Hata yönünü seç.** Bilgi veren hook hatada devam edebilir. Güvenlik kapısı hatada engellemeli: betikte `exit 2`, destekleyen sürümde `onFailure: "block"`.
- **`if` ile süzmek hızlandırır, güvenlik sağlamaz.** Kesin ret için deny kuralı.
- **Sıraya güvenme.** Bağımlı adımlar tek betikte.
- **Hook sayısı arttıkça sor:** bu bir kural mı, tercih mi? Kırk hook'a ulaştıysan çoğu tercihtir.

## Alıştırma: engelleyen bir PreToolUse hook'u yaz ve üç girdiyle sına

Bunu deneme deposunda yap. Gerçek bir iş deposunda hook'u etkinleştirme.

1. `jq` kurulu olduğundan emin ol (`jq --version`). Deneme deposunda `.claude/hooks/yasak-komut.sh` dosyasını oluştur.

```
#!/bin/sh
# PreToolUse: Bash komutunda yasak kalıp varsa engelle
komut=$(jq -er '.tool_input.command | select(type == "string")') || {
  echo "Geçersiz hook girdisi" >&2
  exit 2
}
if printf '%s' "$komut" | grep -qE 'DROP TABLE|--force'
then
  echo "Politika engelledi: yasak kalıp" >&2
  exit 2
fi
exit 0
```

2. `chmod +x .claude/hooks/yasak-komut.sh` ile çalıştırılabilir yap.
3. Üç girdiyi elle ver ve çıkış kodunu yazdır:
   - İzinli: `printf '%s' '{"tool_input":{"command":"git status"}}' | .claude/hooks/yasak-komut.sh`, ardından `echo $?`. Beklenen: 0.
   - Yasak: aynı komut, ama `git push --force`. Beklenen: 2 ve stderr'de gerekçe.
   - Bozuk: `printf '%s' '{bozuk' | .claude/hooks/yasak-komut.sh`, ardından `echo $?`. Beklenen: 2.
4. Betiği bilerek boz. `exit 2` satırlarından birini `exit 0` yap (önce yasak-kalıp dalını, sonra bozuk-girdi dalını). Üç girdiyi yeniden ver. İlgili satırın artık 0 döndüğünü ve testinin düştüğünü gör. Betiği geri al.
5. Hook'u `.claude/settings.json` içine bağla: `PreToolUse`, `matcher: "Bash"`, tip `command`, yol `${CLAUDE_PROJECT_DIR}/.claude/hooks/yasak-komut.sh`. Yeni oturumda Claude'dan zararsız bir komut ve `echo "--force"` içeren bir komut çalıştırmasını iste. İkincisinin engellendiğini ve Claude'un gerekçeyi okuduğunu gör.

**Bitti sayılması için:** üç satırlık bir tablo (girdi, beklenen kod, gerçek kod), bozulmuş sürümde düşen satırın kaydı ve gerçek oturumdaki engelin ekran görüntüsü ya da transkript alıntısı. Sonra deneme deposunu sil.

## Bağlantılar

Kontrol listesi: [[8.1]] [[8.2]] [[8.3]] [[8.4]] [[8.5]] [[8.6]] [[8.7]] [[7.6]]. Gerçek vakalar: D07, D08, {{ek:deneyimler}}. Önceki bölümler: {{bolum:5}}, {{bolum:6}}, {{bolum:7}}. Ekler: {{ek:komutlar}}, {{ek:sorun-giderme}}.

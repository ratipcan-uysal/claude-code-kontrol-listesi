# Sorun giderme

_Belge kontrolü: 29 Ekim 2026_

Bir belirti çoğu zaman birkaç nedenden biridir. Aşağıdaki tablo her belirti için **ilk ayırıcı kontrolü** verir: nedenleri birbirinden ayıran en ucuz bakış. Aynı denemeyi tekrarlamak yerine yeni kanıt topla.

Hangi başlığın uyduğunu bilmiyorsan oturumda `/doctor` koş. Claude hiç açılmıyorsa kabukta `claude doctor`. Sorunun senin yapılandırmandan gelip gelmediğini ayırmak için `claude --safe-mode` ya da `claude --bare` ile başlat. Kaynak: [resmî sorun giderme](https://code.claude.com/docs/en/troubleshooting).

## Talimat ve ayar

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| CLAUDE.md'deki kural uygulanmıyor | `/memory` listesinde dosya var mı? | Yüklenmiyorsa yol ya da import onayı. Yükleniyorsa kural belirsiz ya da başka kuralla çelişiyor. [1.2](../README.md#1-talimat) [1.5](../README.md#1-talimat) |
| Import edilen dosya bazen görünüyor, bazen görünmüyor | Etkileşimli mi headless mi, worktree'de mi? | Proje dışı import onayı proje yolu başına tutulur. Her oturumda gereken bilgi için SessionStart hook'u. [1.5](../README.md#1-talimat) [8.1](../README.md#8-hook) |
| Ayar değişikliği etki etmiyor | `/status` içinde `Setting sources` | Daha yüksek öncelikli katman aynı anahtarı ezmiş olabilir. Listeler birleşir, ezilmez. [1.8](../README.md#1-talimat) |
| Model ayarı tutmuyor | `env` içinde `ANTHROPIC_MODEL` var mı? | Kabuktaki değişken dosyadaki `model` anahtarını geçer. [1.8](../README.md#1-talimat) |
| Otomatik bellek eski bilgi veriyor | Kaydın tarihi ve kaynağın bugünkü hali | Eski kaydı düzelt ya da sil. [1.7](../README.md#1-talimat) |

## İzin ve hook

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Aynı komut için sürekli izin soruluyor | Komutta `$(...)`, `${...}`, `source` var mı? | Bu parçaları içeren komut allow kuralıyla eşleşmeyip her seferinde sorabilir. Komutu onlarsız yaz, venv'i aktive etmek yerine yorumlayıcıyı doğrudan çağır. [6.4](../README.md#6-izin) |
| Gözetimsiz koşum izin ekranında takıldı | Oturumun gerçek etkin modu | Ayarlanan mod ile açılan mod farklı olabilir. Projenin kendi allow listesine bak. [6.7](../README.md#6-izin) [13.2](../README.md#13-gozetimsiz) |
| Hook hiç çalışmıyor | `/hooks` listesinde var mı, eşleşme deseni doğru mu? | Betiği aynı JSON girdisiyle elle çalıştır. [8.4](../README.md#8-hook) |
| Hook çalışıyor ama engellemiyor | Hook async mi, çıkış kodu 2 mi? | Async hook engelleyemez. Olayın exit 2 davranışını belgede kontrol et. [8.5](../README.md#8-hook) [8.6](../README.md#8-hook) |
| İki hook'un sonucu her seferinde farklı | Aynı olaya eşleşen birden çok hook var mı? | Paralel çalışırlar. Bağımlı adımları tek betikte birleştir. [8.7](../README.md#8-hook) |

## Bağlam ve performans

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Bağlam çabuk doluyor | `/context` dağılımı | Büyük dosyayı parça parça okut, geniş aramayı alt ajana ver. [2.4](../README.md#2-baglam) [2.5](../README.md#2-baglam) |
| Otomatik sıkıştırma art arda tetikleniyor | `/context` içinde `Messages` payı | Odak vererek `/compact`, gerekirse `/clear` ve devir dosyası. [2.6](../README.md#2-baglam) |
| Oturum dondu | `Ctrl+C` tepki veriyor mu? | Vermiyorsa terminali kapat, aynı dizinde `claude --resume`. Konuşma kaybolmaz. |
| Bellek ya da işlemci çok yüksek | Büyük derleme dizinleri, eklentiler | `.gitignore`'a ekle, `claude --safe-mode` ile eklenti ve MCP'yi ayır, yeniden başlatıp `--continue`. |
| `@dosya` ya da arama sonuç vermiyor | `claude doctor` çıktısında Search satırı | Paketli ripgrep çalışmıyor olabilir. Belgedeki ripgrep adımları. |

## Genişletme

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Skill hiç devreye girmiyor | `/skills` listesinde var mı? | Varsa açıklama, isteğin diliyle eşleşmiyor. Açıklamaya tetik kelimelerini ve sınırını yaz. [9.3](../README.md#9-yeniden) [9.8](../README.md#9-yeniden) |
| Yeni skill görünmüyor | Dosya doğru dizinde mi? | `/reload-skills`. |
| MCP aracı listede ama veri gelmiyor | `/mcp` durumu ve küçük bir okuma denemesi | Bağlantı, yetki ve sorgu kapsamını ayrı sına. [9.7](../README.md#9-yeniden) |
| Alt ajan raporu "bitti" diyor ama iş yok | Diff ve dosya | Rapor kanıt değildir. Dosyanın kendisine bak. [12.3](../README.md#12-dogrulama) |

## Doğrulama, koşum ve yayın

| Belirti | İlk ayırıcı kontrol | Sonraki adım |
|---|---|---|
| Testler geçti ama hata sürüyor | Koşulan test sayısı | Filtre hiçbir şeye eşleşmemiş olabilir. Hatayı geri koyup testin düştüğünü gör. [12.1](../README.md#12-dogrulama) [12.2](../README.md#12-dogrulama) |
| Headless betik başarılı diyor ama sonuç boş | JSON'da `is_error` ve `structured_output` | Yalnız `subtype` alanına güvenme. [14.6](../README.md#14-rutin) [14.7](../README.md#14-rutin) |
| Gece koşumu sabah bitmemiş, çıktı boş | Süreç yaşıyor mu, işlemci süresi ne, makine şarjda mı? | Arka plan işi tur bitince ölmüş ya da makine uyumuş olabilir. Bkz. deneyimler D03 ve D05. [13.3](../README.md#13-gozetimsiz) [13.4](../README.md#13-gozetimsiz) |
| Rutin hiç çalışmamış gibi | Zamanlandı mı, başladı mı, çıktı yazdı mı? | Üç aşamayı ayrı kontrol et. Sessizliği başarı sayma. [14.3](../README.md#14-rutin) |
| Commit'te başkasının dosyaları var | `git log --stat` | Aynı checkout'ta başka oturum stage etmiş. Ayrı worktree. [11.1](../README.md#11-paralel) [11.2](../README.md#11-paralel) |
| Önizlemede değişiklik görünmüyor | Sunucu hangi dizinden, hangi porttan çalışıyor? | Başka oturumun sunucusuna bakıyor olabilirsin. [11.3](../README.md#11-paralel) |
| Rewind sonrası bazı dosyalar eski halinde değil | Dosya Bash'le mi değişti? | Checkpoint onu izlemez. Git ile geri al. [15.2](../README.md#15-git) |
| Belgedeki komut yok | `claude --version` | Belge yerel sürümden yeni olabilir. Güncelle ya da `/help` ile kontrol et. [19.6](../README.md#19-bakim) |

## Yardım isterken

"Çalışmıyor" yerine dört şey yaz: beklenen, gözlenen, tekrar koşulu ve son değişiklik. Büyük log'u sohbete yapıştırma, dosyaya yaz ve ilgili kısmı okut.

```text
Beklenen: PreToolUse hook'u rm -rf içeren komutu reddetsin.
Gözlenen: komut sormadan çalıştı.
Tekrar: yeni oturum, proje kökünde, hook .claude/settings.json içinde.
Son değişiklik: hook'a async: true eklendi.
İstek: nedeni ayır, en küçük düzeltmeyi öner, aynı koşulda sına.
```

---

[Kontrol listesi](../README.md) · [Komutlar ve kısayollar](komutlar.md) · [Gerçek deneyimlerden on ders](deneyimler.md) · [Terimler sözlüğü](sozluk.md)

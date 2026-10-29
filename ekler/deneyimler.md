# Gerçek deneyimlerden on ders

_Belge kontrolü: 29 Ekim 2026_

Bu sayfadaki on vaka, bu listenin yazarının kendi makinesinde tuttuğu tarihli ölçüm defterinden alındı. Proje adları, yollar ve kişisel veriler çıkarıldı. Her vaka bir gözlemdir: o makinede, o sürümde, o koşulda görüldü. Genel kural gibi okuma, kendi ortamında aynı belirtiyi gördüğünde ilk bakılacak yer olarak kullan.

Vakaların ortak dersi şu: en pahalı hatalar bir şeyin kırılmasından değil, bir şeyin **hiçbir şeye bakmadan başarılı görünmesinden** çıkıyor.

## D01 · Gözetimsiz oturumda izin modu sessizce değişti

**Gözlenen:** Zamanlanmış oturumların izinsiz ilerlemesi için `bypassPermissions` modu ayarlanmıştı. Bir projenin 43 oturum kaydındaki 345 mod değeri tarandı. Bu mod hiç görünmüyordu. Mod ilk kullanımda bir onay penceresi istiyor, zamanlanmış oturum pencereyi gösteremediği için oturum hata vermeden varsayılan moda düşüyordu.

**Ders:** Ayarladığın mod ile oturumun gerçekte açıldığı mod ayrı şeylerdir. Gözetimsiz koşumu ayakta tutan şey projenin kendi izin listesiydi.

**Ayırıcı kanıt:** Oturum kaydındaki etkin mod değeri. Ayar dosyasındaki değer kanıt değildir.

**Sınır:** 29 Ağustos 2026 gözlemi. Davranış sürüme ve yönetilen politikaya göre değişebilir. İlgili maddeler: [6.7](../README.md#6-izin), [13.2](../README.md#13-gozetimsiz).

## D02 · Hiç test koşmayan filtre yeşil döndü

**Gözlenen:** Test komutuna süitin okunur adı filtre olarak verildi. Eşleşen test olmadı, çıktı "başarılı" dedi. Aynı gün iki kez rapora "test geçiyor" diye girmek üzereydi. Aynı gün iki benzer yeşil daha görüldü: hiçbir dosya bulamadığı için geçen lint ve dar pencere yüzünden körleşen lint.

**Ders:** Durum satırını değil sayıyı oku. Sıfır test koşmak geçmek değildir.

**Ayırıcı kanıt:** Çıktıdaki koşulan test sayısı. Filtreyi tip ya da fonksiyon adıyla verince sayı sıfırdan çıktı.

**Sınır:** Belirli bir test aracının filtre davranışı. Başka araçlarda ilke aynı, sözdizimi farklı. İlgili maddeler: [12.1](../README.md#12-dogrulama), [12.2](../README.md#12-dogrulama).

## D03 · Arka plana atılan iş, tur bitince iz bırakmadan öldü

**Gözlenen:** Zamanlanmış bir görev uzun bir veri çekimini arka planda başlattı ve turu "bekliyorum" diye kapattı. Komut başlamadan önce rastgele bekleme yapıyordu. Oturum kapanınca süreç öldü, görev çıktısı dizinle birlikte silindi. 83 dakika boyunca ağa tek istek gitmedi ve geriye tek satır kanıt kalmadı.

**Ders:** Gözetimsiz oturumda uzun işi arka plana atıp turu kapatma. Log'u oturumdan bağımsız bir yola yaz. Aynı iş ön planda ve kalıcı log'la 12 dakikada bitti.

**Ayırıcı kanıt:** Normal komutun yarım çıktısı log'da kalır. Önce bekleyen komut ise "hiç başlamadı" ile "öldü" arasında fark bırakmaz.

**Sınır:** 1 Eylül 2026, tek bir masaüstü kurulumu. İlgili maddeler: [13.3](../README.md#13-gozetimsiz), [13.4](../README.md#13-gozetimsiz).

## D04 · "Ucuz" kontrol yük altında 120 kat uzadı

**Gözlenen:** Görev dosyası bir test komutunu "yaklaşık 2,5 saniye" diye tarif ediyordu. Bir nöbet koşumunda aynı komut 300 saniyelik ön plan sınırını aştı ve arka plana düştü. Testler sonunda geçti. Makine yükü o dakikada 68'e çıkmıştı, eşzamanlı oturumlar yüzünden.

**Ders:** "Ucuz" bir ölçüm değil varsayımdır. Kontrol arka plana düştüyse turu kapatma, bitmesini bekle ve çıkış satırını oku. Yoksa D03 tekrarlanır ve dışarıdaki nöbetçi makineyi ölü sanıp yanlış alarm verir.

**Ayırıcı kanıt:** `uptime` yük ortalamaları. Bir dakikalık değer on beş dakikalığın birkaç katıysa yük o pencerede fırlamıştır.

**Sınır:** 2 Eylül 2026. İlgili maddeler: [11.4](../README.md#11-paralel), [13.4](../README.md#13-gozetimsiz).

## D05 · Uyku engelleyici, bataryada uykuyu engellemedi

**Gözlenen:** Gece koşumu bir uyku engelleyiciyle sarılmıştı. Makine prizde değildi. 19 saatte süreç 1,2 saniye işlemci zamanı kullandı. Sistem günlüğünde aynı gece 257 uykuya giriş kaydı vardı. Çıktı dosyası 19 saat boyunca boş kaldı. Makine prize takılınca aynı koşum 20 dakikada bitti.

**Ders:** Batarya ve düşük şarj koşumu öldürmez, dondurur. Donma sessizdir. Gece koşumunun ön koşulu makinenin şarjda olmasıdır.

**Ayırıcı kanıt:** Geçen süreye değil işlemci süresine bak. Oran sıfıra yakınsa süreç uyuyor demektir.

**Sınır:** macOS, 5 Eylül 2026. İlgili madde: [13.2](../README.md#13-gozetimsiz).

## D06 · Başka oturumun commit'i benim değişikliklerimi götürdü

**Gözlenen:** Değişiklikler stage edildi, ardından üç dakikalık izole derleme yapıldı. Bu arada aynı repoda çalışan başka bir oturum kendi raporunu commit'ledi. Commit index'in tamamını aldı. Dört dosya başka bir mesajın altına girdi, benim commit'im "değişiklik yok" diye boş döndü.

**Ders:** Git index'i aynı checkout'taki bütün oturumlar arasında ortaktır. Stage ile commit'i tek komutta yap. Arada derleme gerekiyorsa index'i değil geçici bir kopyayı ya da ayrı worktree'yi kullan.

**Ayırıcı kanıt:** `git log --stat` ile dosyaların hangi commit'e girdiğine bak.

**Sınır:** 28 Eylül 2026. İçerik doğruydu, yalnız commit mesajı yanlıştı. Paylaşılan dalda geçmiş yeniden yazılmadı. İlgili maddeler: [11.1](../README.md#11-paralel), [11.2](../README.md#11-paralel).

## D07 · Proje dışı import headless koşumda yüklenmedi

**Gözlenen:** Ortak kurallar ayrı bir dosyaya taşındı ve dört projenin CLAUDE.md'sine `@~/...` import'u eklendi. `claude -p` ile koşulan oturum dosyanın içeriğini görmedi, yalnız import satırını gördü. Proje dışı import onayı proje yolu başına tutuluyordu. Her worktree ayrı kayıt sayılıyordu, headless koşum onay penceresini hiç göstermiyordu. Symlink de çözmedi.

**Ders:** Her oturuma girmesi gereken proje dışı bilgiyi import'a bırakma. SessionStart hook'u aynı içeriği her koşumda bağlama koydu ve model kuralı kelimesi kelimesine aktardı.

**Ayırıcı kanıt:** Dosya okuma araçları kapalı bir headless oturumda "bu kural ne diyor?" diye sor.

**Sınır:** 15 Ekim 2026. İlgili maddeler: [1.5](../README.md#1-talimat), [8.1](../README.md#8-hook).

## D08 · Dört paralel oturum makineyi kilitledi, metin kuralı yetmedi

**Gözlenen:** Dört alt oturum ayrı worktree'lerde aynı anda derleme ve test koştu. Başka projelerin derlemeleri de sürüyordu. Yük ortalaması 720'ye çıktı, sakin makinede 4'tü. Oturumlara "ağır komutu kilitle sar" diye metin talimatı verildi. Bir oturum kilitsiz başlattığı derlemeyi sonradan durdurmak zorunda kaldı.

**Ders:** Metin kuralı yeni oturuma ve başka projeye ulaşmaz. Çalışan yol iki parçalıydı: ağır komutları iki yuvalı kilitle koşturan bir sarmalayıcı ve sırasız ağır komutu reddeden bir PreToolUse hook'u.

**Ayırıcı kanıt:** Hook 16 vakalık bir testle sınandı, sıfır yanlış verdi. Hafif komut istisnası bozulunca iki yanlış verdi, yani test gerçekten bakıyordu.

**Sınır:** 26 Ekim 2026. Tek yuva fazla dar çıktı: uzun bir cihaz testi kilidi 30 dakika tuttu, diğerleri boşta bekledi. İlgili maddeler: [8.4](../README.md#8-hook), [11.4](../README.md#11-paralel), [11.6](../README.md#11-paralel).

## D09 · Geçici dizin toptan silindi, çok günlük iş gitti

**Gözlenen:** Bir yazı serisinin kaynakları, görselleri ve durum dosyası oturumun geçici çalışma dizinindeydi. Dizin ağacı bir akşam toptan silindi. Metinler alt ajan kayıtlarındaki dosya okuma sonuçlarından geri kuruldu. Görsellerin yerel kopyası geri gelmedi.

**Ders:** Birden çok gün sürecek işin kaynağı geçici dizinde tutulmaz. Proje dizinine ya da kalıcı bir yola yaz. Geçici dizin yalnız o turun ara çıktısı içindir.

**Ayırıcı kanıt:** Yeniden yaratılan dizinlerin hepsi aynı dakikanın zaman damgasını taşıyordu.

**Sınır:** 27 Ekim 2026. Silmenin nedeni ölçülmedi. İlgili maddeler: [13.3](../README.md#13-gozetimsiz), [18.2](../README.md#18-bilgi).

## D10 · Eski rapor, canlı sistemin yerine okundu

**Gözlenen:** On gün önceki bir denetim "uygulama yalnız bir ülkede satışta" diyordu. Cümle aynı gün iki kez tekrarlandı, biri kullanıcının yapıştırdığı notta. Sayfaya bakılmadan doğru kabul edildi ve buna göre bir karar önerildi. Yönetim panelinde uygulama 175 ülkede satıştaydı. Aynı oturumda ikinci bir örnek: bir sürüm notundaki "hepsinin görseli var" iddiası yeni sürümde 11 eksik görselle çürüdü.

**Ders:** Mağaza ayarı, sayı, kapsam gibi değişebilen bir durumu eski rapordan alma. Kullanıcının yapıştırdığı not da bir rapordur. Yazmadan ya da öneri yapmadan önce kaynağın kendisine bak.

**Ayırıcı kanıt:** Kaynağın şu anki değeri ve okuma tarihi.

**Sınır:** 28 Ekim 2026. İlgili maddeler: [12.3](../README.md#12-dogrulama), [18.4](../README.md#18-bilgi).

---

[Kontrol listesi](../README.md) · [Komutlar ve kısayollar](komutlar.md) · [Sorun giderme](sorun-giderme.md) · [Dosya konumları](dosyalar.md) · [İpuçları ve püf noktaları](ipuclari.md) · [Terimler sözlüğü](sozluk.md)

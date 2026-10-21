# Claude Code'u iyi kullanmanın kontrol listesi

19 bölüm, 107 madde. Her maddede neden, nasıl, kopyalanabilir örnek ve doğrulama.

- **Web sürümü** (işaretlenebilir, süzgeçli): https://ratipcan-uysal.github.io/claude-code-kontrol-listesi/
- **PDF:** [claude-code-kontrol-listesi.pdf](claude-code-kontrol-listesi.pdf)

_21 Ekim 2026 · Kaynak kontrolü; yerel CLI 2.1.284_

## Nasıl okunur

Bu liste tekrar işi azaltmak, kapsamı belirlemek ve sonucu kanıtla teslim almak için hazırlanmış bir çalışma rehberidir. Her madde her projeye uygun değildir; kullanımına uygun olanları seç.

**Neden** gerekçeyi, **nasıl** uygulama yolunu, **doğrula** beklenen kanıtı gösterir. Başlangıç onlusu ve temel/ileri etiketleri editoryal öneridir; ölçülmüş getiri sıralaması değildir.

**Temel** 25, **ileri** 82 madde vardır. Teknik davranışların yanında resmî kaynak bağlantısı bulunur; bağlantısız maddeler iş akışı önerisidir. Örnekler kendi projenin araçlarına ve yetkisine uyarlanmalıdır.

Kaynaklar 21 Ekim 2026'da kontrol edildi. Yerel CLI 2.1.284 için yalnız sürüm ve yardım çıktısı alındı; listelenen bütün Claude özellikleri canlı çalıştırılmadı. CLI, Desktop, bulut ve sağlayıcı farklarını ilgili belgede kontrol et.

Bir kutuyu işaretlemek kişisel ilerleme kaydıdır; otomatik doğrulama veya güvenlik garantisi değildir. Tarayıcı verisi temizlenebilir; ilerlemeni JSON olarak dışa aktarabilirsin.

## Önce bu on madde

1. **Bitiş ölçütünü baştan yaz** ([3.1](#3-gorev)): Ölçüt yoksa iş parça parça ilerler ve her parçada seni bekler.
2. **Tutarlı oturum ve devir kaydı** ([2.1](#2-baglam)): Birbirinden kopuk işleri aynı bağlama yığmak kararları karıştırabilir; her küçük adımda yeni oturum açmak da tekrar yaratır.
3. **Kısa ve doğrulanmış proje talimatı** ([1.2](#1-talimat)): Derleme komutu ve tuzaklar her oturumda yeniden keşfedilmesin.
4. **Projeye izin listesi** ([6.1](#6-izin)): Projeye ait dar liste tekrarlanan izinleri azaltabilir; test betikleri de kod çalıştırdığı için önce incelenmelidir.
5. **Gizli dosyaları okuma dışı bırak** ([7.1](#7-guvenlik)): Gizli verinin bağlama veya çıktıya girmesini azaltmak gerekir; tek bir araç kuralı tam yalıtım sağlamaz.
6. **Alt ajan modelini ölçerek seç** ([5.1](#5-model)): Daha küçük model her doğrulama işinde yeterli olmayabilir. Aynı temsilî işte kalite, süre ve kullanımı karşılaştır.
7. **"Geçti" yerine sayıyı oku** ([12.1](#12-dogrulama)): Eşleşmeyen bir test filtresi sıfır test koşup başarılı diyebilir.
8. **Kaynak kodu Git’te, commit kapsamı belli** ([15.1](#15-git)): Küçük, anlamlı commit geri almayı kolaylaştırır. Git dışı veriler ve sırlar için ayrıca uygun yedek gerekir.
9. **Düşünme bütçesini işe göre ayarla** ([5.3](#5-model)): Mimari karar ile dosya yeniden adlandırma aynı bütçeyi istemez. "Think hard" gibi ifadeler sıradan metin olarak geçer, hiçbir ayarı değiştirmez. Yalnız `ultrathink` o tur için ek bir talimat ekler, effort ayarı yine aynı kalır.
10. **Eleştiriyi yazandan ayrı bağlama ver** ([9.1](#9-yeniden)): Ayrı bağlam farklı varsayımlarla inceleme yapabilir; bağımsızlık kalite garantisi değildir.

## Bölümler

1. [Talimat katmanları](#1-talimat) (7)
2. [Bağlam yönetimi](#2-baglam) (6)
3. [Görev verme](#3-gorev) (7)
4. [Prompt yazımı: önce ve sonra](#4-prompt) (4)
5. [Model, effort ve maliyet](#5-model) (5)
6. [İzinler](#6-izin) (7)
7. [Güvenlik ve gizlilik](#7-guvenlik) (7)
8. [Hook'lar](#8-hook) (5)
9. [Skill, komut, ajan, MCP](#9-yeniden) (8)
10. [Ekiple kullanım](#10-ekip) (3)
11. [Paralel çalışma](#11-paralel) (6)
12. [Doğrulama](#12-dogrulama) (7)
13. [Gözetimsiz koşum](#13-gozetimsiz) (6)
14. [Rutinler ve zamanlama](#14-rutin) (6)
15. [Git ve yayın](#15-git) (4)
16. [Tasarım ve arayüz](#16-tasarim) (4)
17. [Mobil ve simülatör](#17-mobil) (5)
18. [Bilgi birikimi](#18-bilgi) (4)
19. [Bakım ritmi](#19-bakim) (6)

<a id="1-talimat"></a>
## 1. Talimat katmanları

Yeni oturumun konuşma bağlamı yenidir; talimat dosyaları ve otomatik bellek oturumlar arasında bilgi taşıyabilir. Kalıcı kuralları kısa tut, ayrıntılı prosedürleri ilgili işe taşınacak dosyalara ayır.

- [ ] **1.1 Global CLAUDE.md'ye yalnız varsayılan davranışı değiştiren kuralları yaz.** `Temel`
  - **Neden:** Talimatlar bağlamda yer kaplar. Gereksiz tekrar, ilgili kuralları bulmayı zorlaştırır.
  - **Nasıl:** `~/.claude/CLAUDE.md`. Genel tavsiye değil, davranış yaz.

    ```
    # Davranışı tarif et
    - Yetkilendirilmiş değişiklikleri anlamlı commit’lere böl.
    - Push ve yayını kullanıcının belirttiği hedef ve kapsam içinde yap.
    - Karar sorarken önerini ve gerekçeni ekle.
    ```

  - **Doğrula:** Her kural için sor: silsem davranış değişir mi? Değişmiyorsa sil.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **1.2 Her aktif projede kısa ve doğrulanmış bir CLAUDE.md tut.** `Temel`
  - **Neden:** Derleme komutu ve tuzaklar her oturumda yeniden keşfedilmesin.
  - **Nasıl:** `/init` taslağını gözden geçir; gerçek test ve derleme komutlarını yaz. 100 satır bir ürün sınırı değildir. Uzun prosedürü skill veya kapsamlı kurala ayır.

    ```
    # Proje: fiyat-izleyici
    ## Komutlar
    - Test: npm test -- --run
    - Tek dosya: npm test -- src/parser.test.ts
    ## Tuzaklar
    - data/ altındaki JSON elle düzenlenmez, scripts/topla.mjs üretir.
    - Saat dilimi her yerde Europe/Istanbul.
    ```

  - **Doğrula:** Yeni oturumda dosya okutmadan "test komutu ne?" diye sor. Doğru cevap gelmeli.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **1.3 Makineye özgü bilgiyi `CLAUDE.local.md`'ye yaz ve gitignore'la.** `İleri`
  - **Neden:** Repo başka makinede ya da bulut oturumunda açılınca yanlış yol talimatı kalmaz.
  - **Nasıl:** Proje kökünde `CLAUDE.local.md`: venv yeri, yerel port, cihaz adı.
  - **Doğrula:** `git check-ignore CLAUDE.local.md` eşleşme döndürmeli.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **1.4 Yalnız belli dosyalarda geçerli kuralı `.claude/rules/` altına koy.** `İleri`
  - **Neden:** Kural yalnız eşleşen dosyaya dokunulunca yüklenir, geri kalan zamanda bağlamı doldurmaz.
  - **Nasıl:** Frontmatter'da `paths`. Kullanıcı düzeyi için `~/.claude/rules/`.

    ```
    ---
    paths: ["**/*.swift"]
    ---
    - Görünüm dosyalarında iş mantığı yok, ViewModel'e taşı.
    - Yeni ekran eklenince Previews da eklenir.
    ```

  - **Doğrula:** Eşleşen bir dosyayı okut, ardından `/context` ile kuralın yüklendiğini gör.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **1.5 Dış dosya import’unun gerçekten yüklendiğini doğrula.** `İleri`
  - **Neden:** Proje dışı import onayı ve çalışma modu, hangi bilginin yüklendiğini etkileyebilir.
  - **Nasıl:** Gerekli dosyayı `@path` ile belirt, dış import onayını yönet ve `/memory` listesinden kontrol et. SessionStart yalnız gerekli dinamik bilgiyi eklesin; onay atlatma yolu olarak kullanılmasın.
  - **Doğrula:** Etkileşimli ve headless kullanımını ayrı dene; yüklenmeyen bilgiyi varsayma.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **1.6 Başka bir ajanla paylaşılan repoda kuralları tek dosyada tut.** `İleri`
  - **Neden:** İki dosya ayrı ayrı güncellenince birbirinden kopar.
  - **Nasıl:** Güncel sürüm AGENTS.md’yi doğrudan okuyabilir; aynı dizinde veya üstünde CLAUDE.md/CLAUDE.local.md bulunması varsayılan seçimi değiştirir. Ortak dosyayı uyumlu biçimde paylaşmak için aşağıdaki import kullanılabilir. `/memory` ile yüklenen dosyayı doğrula.

    ```
    # CLAUDE.md
    @AGENTS.md
    ```

  - **Doğrula:** Her iki araçta yüklenen dosya ve kritik kural aynı; benzer cevap tek başına yüklenme kanıtı değildir.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **1.7 Otomatik belleği düzenli olarak gözden geçir.** `İleri`
  - **Neden:** Talimat dosyası ile modelin biriktirdiği notlar farklıdır; eski çıkarım sonraki işi etkileyebilir.
  - **Nasıl:** `/memory` ile kayıtları ve etkin ayarı incele; yanlış veya artık geçerli olmayan bilgiyi düzelt.
  - **Doğrula:** Yeni oturum kritik notu doğru kullanıyor; otomatik belleğe güvenilerek açık iş kaydı atlanmıyor.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)

<a id="2-baglam"></a>
## 2. Bağlam yönetimi

Gereksiz araç çıktısı ve konu değişimleri bağlamı büyütür. Sıkıştırma ayrıntı kaybettirebilir; yeni oturum da bağlamı tekrar kurmayı gerektirir. Geçiş kararını işin sınırına ve açık kanıtlara göre ver.

- [ ] **2.1 Oturumu tutarlı bir iş etrafında tut; geçişte devir dosyası bırak.** `Temel`
  - **Neden:** Birbirinden kopuk işleri aynı bağlama yığmak kararları karıştırabilir; her küçük adımda yeni oturum açmak da tekrar yaratır.
  - **Nasıl:** Oturum sonunda Claude'a proje kökünde bir devir dosyası yazdır, yeni oturum oradan başlasın.

    ```
    Oturumu kapatıyoruz. BEKLEYENLER.md'ye yaz:
    1. Sıradaki adım (komut, dosya, beklenen sonuç)
    2. Açık sorular
    3. Alınan kararlar ve gerekçeleri, denenip olmayanlar
    4. Bitenler (tarihli, kısa)
    ```

  - **Doğrula:** Yeni oturum açık işi, ilgili dosyayı ve son doğrulama sonucunu devirden bulabiliyor.
  - **Dayanak:** [İyi uygulamalar](https://code.claude.com/docs/en/best-practices)
- [ ] **2.2 Bağlamı tahminle değil sayıyla izle.** `Temel`
  - **Neden:** Doluluğu hissedemezsin. Sayı görünce devri zamanında yaparsın.
  - **Nasıl:** `/context` ile anlık dağılım. `/statusline` ile alt satıra doluluk yüzdesi.

    ```
    /statusline model adını ve context_window.used_percentage değerini göster
    ```

  - **Doğrula:** Durum satırında yüzde görünüyor.
  - **Dayanak:** [Durum satırı](https://code.claude.com/docs/en/statusline)
- [ ] **2.3 Konu değişince `/clear` de.** `Temel`
  - **Neden:** Eski konunun ayrıntısı yeni işte gürültüdür, yanlış varsayıma da yol açar.
  - **Nasıl:** Alakasız yeni iş için yeni oturum ya da `/clear`.
  - **Doğrula:** Bir oturumda iki farklı projeye ait iş kalmamalı.
  - **Dayanak:** [Komutlar](https://code.claude.com/docs/en/commands)
- [ ] **2.4 Çok dosya okuyan araştırmayı alt ajana ver.** `İleri`
  - **Neden:** Ham metin alt ajanın bağlamında kalır, ana oturuma yalnız sonuç döner.
  - **Nasıl:** Dönüş biçimini baştan söyle.

    ```
    Bir alt ajanla src/ altındaki bütün ödeme akışını tara.
    Bana yalnız şunları dön: giriş noktaları (dosya:satır),
    harici servis çağrıları, hata yönetimi olmayan yerler.
    ```

  - **Doğrula:** Ana oturumda dosya dökümü yerine kısa rapor görürsün.
  - **Dayanak:** [Alt ajanlar](https://code.claude.com/docs/en/sub-agents)
- [ ] **2.5 Büyük araç çıktısını dosyaya yazdır, bağlama yalnız özetini al.** `İleri`
  - **Neden:** Büyük araç çıktısı gerekli kanıtı görünmez kılabilir.
  - **Nasıl:** Tam çıktıyı göreve özel loga yaz; özeti ve komutun gerçek çıkış kodunu birlikte raporla.

    ```
    mkdir -p work
    npm test > work/test.log 2>&1
    sonuc=$?
    tail -n 30 work/test.log
    exit "$sonuc"
    ```

  - **Doğrula:** Sonda çalışan tail komutunun başarısı testin başarısı sanılmıyor.
  - **Dayanak:** [Headless kullanım](https://code.claude.com/docs/en/headless)
- [ ] **2.6 `/compact` yaparken neyin korunacağını söyle.** `İleri`
  - **Neden:** Talimatsız sıkıştırma neyin önemli olduğunu tahmin eder.
  - **Nasıl:** Komutun arkasına korunacakları yaz.

    ```
    /compact veri modeli kararlarını, açık hataları ve değişen dosya yollarını koru
    ```

  - **Doğrula:** Sıkıştırmadan sonra kritik bir kararı sor, doğru gelmeli.
  - **Dayanak:** [Komutlar](https://code.claude.com/docs/en/commands)

<a id="3-gorev"></a>
## 3. Görev verme

Bir isteğin kalitesi, en çok neyin "bitti" sayılacağının açıklığına bağlı. Bitiş tanımı yoksa model ya erken durur ya da senden "devam" bekler.

- [ ] **3.1 Bitiş ölçütünü baştan yaz.** `Temel`
  - **Neden:** Ölçüt yoksa iş parça parça ilerler ve her parçada seni bekler.
  - **Nasıl:** Bitiş koşulunu ve durma sınırını yaz. `/goal` değerlendirmesi konuşmadaki kanıta bakar; bağımsız dosya veya test denetimi yapmaz. Metne yazılan tur sınırı da model tarafından yorumlanır, süreç düzeyinde katı bütçe değildir.

    ```
    Ödeme doğrulamasını uygula. Kabul: geçerli kart kabul, bozuk kart ret,
    servis hatasında tekrar deneme; ilgili testlerin sayısını ve çıktısını göster.
    /goal bu kabul senaryoları ve ilgili testler geçiyor; ya da 20 turda eksikleri raporlayıp dur
    ```

  - **Doğrula:** İstenen davranış ve test çıktısı görünür; sınırda duran iş tamamlandı diye raporlanmıyor.
  - **Dayanak:** [Hedefler](https://code.claude.com/docs/en/goal)
- [ ] **3.2 Kabul ölçütünü doğrulanabilir yaz.** `Temel`
  - **Neden:** "Çalışsın" denetlenemez, "şu test 12/12 geçsin" denetlenir.
  - **Nasıl:** Sayı, ekran ya da komut çıktısıyla tarif et.

    ```
    Kötü: Arama düzgün çalışsın.
    İyi:  "ist" yazınca 300 ms içinde İstanbul ilk sırada gelir;
          boş sorguda liste temizlenir; search.test.ts 8/8 geçer.
    ```

  - **Doğrula:** Ölçütü başka biri okuyup evet/hayır diyebiliyor mu?
  - **Dayanak:** İş akışı önerisi
- [ ] **3.3 Büyük ve belirsiz işte önce plan iste, küçük işte doğrudan yaptır.** `Temel`
  - **Neden:** Plan, yanlış yönü kod yazılmadan yakalar. Küçük işte plan zaman kaybıdır.
  - **Nasıl:** Plan modu: CLI'da Shift+Tab ile modlar arasında geç ya da tek bir isteğin başına `/plan` yaz. Uygulamada mod seçiciyi kullan.
  - **Doğrula:** Plan aşamasında hedef uygulama dosyaları değişmemiş; izin isteyen bir araç plan modunda diye otomatik güvenli sayılmamış.
  - **Dayanak:** [Komutlar](https://code.claude.com/docs/en/commands)
- [ ] **3.4 Kısıtları ve yapılmayacakları açıkça söyle.** `Temel`
  - **Neden:** Model boşluğu en olası çözümle doldurur. O çözüm çoğu zaman senin istemediğindir.
  - **Nasıl:** İsteğe ayrı bir "Kısıtlar" bloğu ekle.

    ```
    Kısıtlar:
    - Yeni bağımlılık ekleme.
    - Sunucu tarafı yok, veri cihazda kalır.
    - Mevcut renk ve boşluk değerlerini kullan.
    ```

  - **Doğrula:** Çıktıda kısıtı ihlal eden bir öğe var mı?
  - **Dayanak:** İş akışı önerisi
- [ ] **3.5 İstediğin çıktının bir örneğini, mümkünse bir de karşı örneğini ver.** `İleri`
  - **Neden:** Bir örnek, bir paragraf tarifin anlatamadığı tonu ve biçimi taşır.
  - **Nasıl:** "Şuna benzesin / şuna benzemesin" diye iki kısa örnek.

    ```
    Bildirim metni şuna benzesin: "Bugün 3 dakikan var mı? Bir sayfa kaldı."
    Şuna benzemesin: "Hedeflerinize ulaşmak için şimdi harekete geçin!"
    ```

  - **Doğrula:** İlk çıktı örneğe yakın mı?
  - **Dayanak:** İş akışı önerisi
- [ ] **3.6 Claude'dan soru sorarken önerdiği cevabı da yazmasını iste.** `İleri`
  - **Neden:** Boş soru işi sana geri yükler. Önerili soruya "önerinle devam" demek yeter.
  - **Nasıl:** Global CLAUDE.md'ye tek kural.

    ```
    - Sorduğun her soruya önerdiğin cevabı ve gerekçesini ekle.
    - Seçenekleri harflendir, tek mesajda tek karar iste.
    ```

  - **Doğrula:** Gelen sorulara tek kelimeyle cevap verebiliyor musun?
  - **Dayanak:** İş akışı önerisi
- [ ] **3.7 Uzun bir brief'i yapıştırmadan önce eksiklerini buldur.** `İleri`
  - **Neden:** Brief'teki boşluk sonradan "beğenmedim" ve yeniden iş olarak döner.
  - **Nasıl:** Kararı sonucu değiştiren boşlukları ve çelişkileri ayır; geri alınabilir uygulama ayrıntılarını öneriyle tamamla.

    ```
    Bu brief’te sonucu değiştiren belirsizlikleri ve çelişkileri listele.
    Her biri için öneri, gerekçe ve karar sahibini yaz.
    Geri alınabilir teknik ayrıntıları varsayım olarak belirtip ilerle.
    ```

  - **Doğrula:** Ürün davranışı veya dış taahhüt değiştiren kararlar çözülmüş; bağımsız işler gereksiz beklemiyor.
  - **Dayanak:** İş akışı önerisi

<a id="4-prompt"></a>
## 4. Prompt yazımı: önce ve sonra

İyi bir istek uzun olmak zorunda değil. Dört şey taşıması yeter: amaç, "iyi"nin tanımı, bağlam ve çıktının biçimi. Aşağıdaki örnekler aynı isteğin zayıf ve güçlü hâlleri.

- [ ] **4.1 "En iyi" ya da "kaliteli" diyorsan ölçütünü yaz.** `Temel`
  - **Neden:** Tanımsız sıfatı model kendi ortalamasıyla doldurur.
  - **Nasıl:** Sıfatın yerine iki-üç gözlemlenebilir özellik koy.

    ```
    Önce: Bana en iyi onboarding ekranını tasarla.
    Sonra: İlk açılışta 30 saniyede bitecek, en fazla 3 ekranlık,
           izin isteğini ilk değer görüldükten sonra soran bir onboarding.
           Üç farklı yön çiz, her biri tam ekran.
    ```

  - **Doğrula:** Ölçütü okuyan biri çıktıyı puanlayabilir mi?
  - **Dayanak:** İş akışı önerisi
- [ ] **4.2 Okuru ve kullanım yerini söyle.** `Temel`
  - **Neden:** Aynı içerik yöneticiye, geliştiriciye ve müşteriye farklı yazılır.
  - **Nasıl:** "Kim okuyacak, nerede, ne karar verecek" cümlesi.

    ```
    Önce: Bu sürüm için not yaz.
    Sonra: Bu sürüm notunu App Store'daki "Yenilikler" alanı için yaz.
           Okur teknik olmayan kullanıcı. En fazla 4 madde, her biri
           kullanıcının fark edeceği bir değişiklik.
    ```

  - **Doğrula:** Çıktının tonu ve ayrıntı düzeyi okura uyuyor mu?
  - **Dayanak:** İş akışı önerisi
- [ ] **4.3 Uzunluk istiyorsan dolguyu da yasakla.** `İleri`
  - **Neden:** "En az 10 sayfa" tek başına doldurma davetidir.
  - **Nasıl:** Uzunluk hedefinin yanına "madde uydurma" kısıtı.

    ```
    Yeterli açıklama ve somut örnek ver. Hedef uzunluk yaklaşık 10 sayfa;
    kaynak veya gerekçe yetmiyorsa kısa tut ve boşluğu açıkla.
    Sayfa hedefi için tekrar, uydurma veri veya gereksiz bölüm ekleme.
    ```

  - **Doğrula:** Silinse kimsenin aramayacağı bir paragraf var mı?
  - **Dayanak:** İş akışı önerisi
- [ ] **4.4 Çıktının biçimini şablonla ver.** `İleri`
  - **Neden:** Biçim belirsizse her bölüm farklı yapıda gelir, karşılaştırılamaz.
  - **Nasıl:** Her öğe için alan listesi.

    ```
    Her madde şu biçimde:
    - tek cümlelik eylem (fiille başlar)
    - neden önemli (bir cümle)
    - nasıl yapılır (komut, ayar ya da dosya)
    - nasıl doğrularım
    ```

  - **Doğrula:** Bütün öğeler aynı alanları taşıyor mu?
  - **Dayanak:** İş akışı önerisi

<a id="5-model"></a>
## 5. Model, effort ve maliyet

Her işe en güçlü modeli ve en yüksek düşünme bütçesini vermek limiti erken bitirir. Doğru eşleştirme, aynı limitle daha çok iş demek.

- [ ] **5.1 Alt ajan modelini işin zorluğu ve hata maliyetiyle seç.** `Temel`
  - **Neden:** Daha küçük model her doğrulama işinde yeterli olmayabilir. Aynı temsilî işte kalite, süre ve kullanımı karşılaştır.
  - **Nasıl:** Ajan tanımında `model` seç; genel varsayılan için aşağıdaki ayar kullanılabilir. Çağrı ve ajan tanımı bu varsayılanı geçersiz kılabilir; Explore/Plan da aynı varsayımı izlemez.

    ```
    {
      "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet" }
    }
    ```

  - **Doğrula:** Çalışan ajanın gerçek modelini `/tasks` ile gör; sonuç kalitesini ayrı değerlendir.
  - **Dayanak:** [Alt ajanlar](https://code.claude.com/docs/en/sub-agents)
- [ ] **5.2 Model takma adı ile sürüme sabitleme arasında bilinçli seçim yap.** `Temel`
  - **Neden:** Takma ad güncellemeleri izler; tam model kimliği tekrar üretilebilirlik sağlar. Takma adın hedefi sağlayıcıya göre de değişir.
  - **Nasıl:** Gündelik işte hesabının desteklediği takma adı, karşılaştırmalı ölçümde tam kimliği kaydet.

    ```
    { "model": "opus" }
    ```

  - **Doğrula:** `/model` ve oturum bilgisi beklediğin modeli gösteriyor; güncel takma ad en ucuz veya en iyi sonuç garantisi sayılmıyor.
  - **Dayanak:** [Model ve effort](https://code.claude.com/docs/en/model-config)
- [ ] **5.3 Düşünme bütçesini işe göre ayarla.** `Temel`
  - **Neden:** Mimari karar ile dosya yeniden adlandırma aynı bütçeyi istemez. "Think hard" gibi ifadeler sıradan metin olarak geçer, hiçbir ayarı değiştirmez. Yalnız `ultrathink` o tur için ek bir talimat ekler, effort ayarı yine aynı kalır.
  - **Nasıl:** Oturumda `/effort`, başlatırken `--effort` kullan. `max` oturum içindir; kalıcı `effortLevel` için desteklenen seviyeyi seç. Seçenekler modele ve sürüme bağlıdır.

    ```
    /effort high
    /effort status
    claude --effort max
    ```

  - **Doğrula:** `/effort status` ile seçimi gör; aynı kabul senaryosunda kalite ve süreyi karşılaştır.
  - **Dayanak:** [Model ve effort](https://code.claude.com/docs/en/model-config)
- [ ] **5.4 Kullanımı haftada bir kez sayıyla gör.** `İleri`
  - **Neden:** Limit bittiğinde değil, bitmeden önce neyin harcadığını bilmek gerekir.
  - **Nasıl:** `/usage` içinde oturum tüketimini ve varsa plan limitlerini ayrı oku. Tahmini dolar tutarı abonelik faturası değildir; API faturası için Console kayıtlarına bak.
  - **Doğrula:** Notta dönem, cihaz kapsamı ve API/abonelik ayrımı var; yaklaşık yerel analiz tüm hesap kullanımı sayılmıyor.
  - **Dayanak:** [Kullanım ve maliyet](https://code.claude.com/docs/en/costs)
- [ ] **5.5 Advisor'u zor kararlar için kullan.** `İleri`
  - **Neden:** İkinci modelin danışması da kullanım tüketir; API faturalaması ve abonelik limiti ayrı değerlendirilir.
  - **Nasıl:** `/advisor opus` ile aç, `/advisor off` ile kapat. Kullanılabilirlik model, sağlayıcı ve özellik erişimine bağlıdır; Anthropic API altyapısı kullanır, bu yalnız API anahtarı kullanıcıları demek değildir.
  - **Doğrula:** `/advisor` ile bağlı modeli kontrol et.
  - **Dayanak:** [Advisor](https://code.claude.com/docs/en/advisor)

<a id="6-izin"></a>
## 6. İzinler

İzin listesi tekrarlanan yetkili işlemleri kolaylaştırır. Etkin mod, yönetilen politika, hook ve sandbox da sonucu etkiler. Bir allow kuralı komutun her girdide güvenli olduğunu kanıtlamaz.

- [ ] **6.1 Her aktif projede `.claude/settings.json` izin listesi tut.** `Temel`
  - **Neden:** Projeye ait dar liste tekrarlanan izinleri azaltabilir; test betikleri de kod çalıştırdığı için önce incelenmelidir.
  - **Nasıl:** Yalnız incelenmiş test ve derleme komutlarını ekle; yazma veya yayın komutunu işin mevcut yetkisine göre ayrı değerlendir.

    ```
    {
      "permissions": {
        "allow": ["Bash(npm test)", "Bash(npm run build)"]
      }
    }
    ```

  - **Doğrula:** İzin isteme davranışını zararsız bir denemeyle ve etkin modla kontrol et; bekleyen adım varsa nedeni kayıtlı.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **6.2 Yıkıcı komutları deny listesine koy.** `Temel`
  - **Neden:** Normal izin değerlendirmesinde deny kuralları allow’dan önce gelir. Komut kalıpları tüm yıkıcı eşdeğerleri yakalamaz; mod/eklenti ve OS sınırlarını da incele.
  - **Nasıl:** Global ya da proje ayarında `deny` dizisi.

    ```
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)",
      "Bash(git reset --hard:*)"
    ]
    ```

  - **Doğrula:** Gerçek veride yıkıcı komut çalıştırma. Geçici, verisiz bir test ortamında engellenen ve izinli karşı örneği kontrol et.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **6.3 Allow girdisini dar tut.** `İleri`
  - **Neden:** Geniş bir joker, istemediğin alt komuta da izin verir.
  - **Nasıl:** Araç adı yerine alt komut düzeyinde yaz.

    ```
    Geniş: "Bash(git:*)"            # push, reset, clean da dahil
    Dar:   "Bash(git status:*)", "Bash(git diff:*)", "Bash(git commit:*)"
    ```

  - **Doğrula:** Her joker için kapsadığı komutları ve seçenekleri gözden geçir; izinli betiğin içeriği değişince yeniden incele.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **6.4 Komutu izin motorunun eşleştirebileceği biçimde yaz.** `İleri`
  - **Neden:** Kabuk genişletmeleri ve birleşik komutlar ek izin değerlendirmesine girebilir; doğrudan yorumlayıcı yolu davranışı sadeleştirir.
  - **Nasıl:** venv'i aktive etme, yorumlayıcıyı doğrudan çağır.

    ```
    Karmaşık: source .venv/bin/activate && python -m pytest
    Daha kolay denetlenir: .venv/bin/python -m pytest
    ```

  - **Doğrula:** Allow'da olan bir komut yine soruyorsa içinde genişletme ara.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **6.5 Tekrarlanan analizleri betiğe çevir.** `İleri`
  - **Neden:** Sürüm kontrollü betik, tekrar eden anlık koddan daha kolay incelenir. Betiği izin listesine almak içindeki her işlemi güvenli yapmaz.
  - **Nasıl:** Analizi projede `scripts/` altına koy, betiği izin listesine ekle.
  - **Doğrula:** Betik değişiklikleri incelenmiş; çalıştırılan dosya ve sürüm raporda belli.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **6.6 Geçmişten izin listesi önerisi al.** `İleri`
  - **Neden:** Hangi komutun sık sorulduğunu tahmin etmek yerine kayıttan çıkar.
  - **Nasıl:** `/fewer-permission-prompts`.
  - **Doğrula:** Önerilen her girdiyi tek tek gözden geçir, yıkıcı olanı alma.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **6.7 Etkin izin modunu başlangıçta kontrol et.** `İleri`
  - **Neden:** Plan, manuel, otomatik onay ve bypass farklı davranır.
  - **Nasıl:** `/permissions` ve oturumun mod göstergesini oku; geniş bypass yerine görevine uygun izin/sandbox bileşimini seç.
  - **Doğrula:** Zararsız örnekte beklenen izin davranışı görülmüş; mod adı tek başına güvenlik kanıtı değil.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)

<a id="7-guvenlik"></a>
## 7. Güvenlik ve gizlilik

Araç izinleri, dış içerik ve veri paylaşımı farklı riskler taşır. Talimat, izin kuralı ve sandbox farklı katmanlardır; biri diğerinin yerine geçmez.

- [ ] **7.1 Gizli dosyaları okuma dışı bırak.** `Temel`
  - **Neden:** Gizli verinin bağlama veya çıktıya girmesini azaltmak gerekir; tek bir araç kuralı tam yalıtım sağlamaz.
  - **Nasıl:** Read deny kuralları dosya araçlarını ve tanınan bazı kabuk erişimlerini kapsar; keyfî Python/Node alt süreçlerini bütünüyle engellemez. Güçlü ayrım için sırları ortamdan çıkar veya sandbox dosya erişim sınırlarını uygula.

    ```
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/*.pem)",
      "Read(./secrets/**)"
    ]
    ```

  - **Doğrula:** Gerçek sır yerine sahte işaret içeren dosyayla dosya aracı ve alt süreç sınırlarını ayrı test et.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **7.2 Kurumsal veriyi kişisel hesaba ve depoya taşıma.** `Temel`
  - **Neden:** Şirket içi adresler, müşteri verisi ve iç doküman, özel bir depoda bile şirketin dışına çıkmış olur.
  - **Nasıl:** Şirket işini şirketin onayladığı hesapla yap. Paylaşmadan önce iç alan adı ve iç kod deposu adresleri için tarama yaptır.

    ```
    Bu klasörü paylaşmadan önce tara: şirket alan adları, iç git adresleri,
    IP adresleri, e-posta adresleri, token'a benzeyen diziler.
    Bulduklarını dosya:satır olarak listele, hiçbirini silme.
    ```

  - **Doğrula:** Push öncesi tarama boş dönüyor.
  - **Dayanak:** [Güvenlik](https://code.claude.com/docs/en/security)
- [ ] **7.3 Web sayfası, e-posta ve belgedeki talimata uyma refleksini kapat.** `Temel`
  - **Neden:** Okunan içerikteki "şunu yap" cümlesi senin talimatın değildir. Prompt injection böyle çalışır.
  - **Nasıl:** Dış içerikle çalışırken izin modunu sıkı tut, yan etkili adımları (gönder, sil, öde) onaya bağla.
  - **Doğrula:** Dış metindeki talimat yetki sayılmıyor; gönderme, silme veya ödeme yalnız kullanıcının geçerli yetkisi kapsamındaysa uygulanıyor.
  - **Dayanak:** [Güvenlik](https://code.claude.com/docs/en/security)
- [ ] **7.4 Ağ erişimini içerik güveniyle karıştırma.** `İleri`
  - **Neden:** Bir alan adına veya curl komutuna izin vermek indirilen içeriği güvenilir talimata dönüştürmez.
  - **Nasıl:** Gereken adres ve araçla sınırla, indirilen betiği çalıştırmadan incele. WebFetch, Bash ve MCP erişimlerini ayrı değerlendir.
  - **Doğrula:** Dış içerikteki talimat uygulama yetkisi olarak kabul edilmiyor; erişim kapsamı kayıtlı.
  - **Dayanak:** [Güvenlik](https://code.claude.com/docs/en/security)
- [ ] **7.5 Güvenmediğin kodda sandbox'ı aç.** `İleri`
  - **Neden:** İndirilen bir repodaki betik dosya sistemine ve ağa serbestçe erişmesin.
  - **Nasıl:** `/sandbox` ile destek ve etkin sınırları incele. Varsayılan okuma erişimi geniş olabilir; gerekli denyRead sınırlarını, ağ alanlarını ve sandbox dışı istisnaları kontrol et. Yerleşik Read/WebFetch araçları ayrıca izin kurallarına tabidir.

    ```
    { "sandbox": { "enabled": true } }
    ```

  - **Doğrula:** İzinli ve yasaklı geçici dosya yollarında zararsız deneme yap; yalnız enabled=true görmeyi yalıtım kanıtı sayma.
  - **Dayanak:** [Sandbox](https://code.claude.com/docs/en/sandboxing)
- [ ] **7.6 Tehlikeli komutu hook'la içeriğinden yakala.** `İleri`
  - **Neden:** Hook politika kontrolünü araç çağrısından önce çalıştırabilir; basit metin araması tüm komut eşdeğerlerini yakalamaz.
  - **Nasıl:** PreToolUse engellemesi için çıkış kodu 2 kullan. Girdiyi doğrula, hatada engelleme davranışını ve timeout’u test et. Aşağıdaki örnek yalnız öğretici bir kalıp kontrolüdür.

    ```
    #!/bin/sh
    # Öğretici örnek; kapsamlı bir komut güvenlik motoru değildir.
    komut=$(jq -er ' .tool_input.command | select(type == "string") ' ) || {
      echo "Geçersiz hook girdisi" >&2; exit 2;
    }
    case "$komut" in
      *"DROP TABLE"*|*"--force"*) echo "Politika denetimi engelledi" >&2; exit 2;;
    esac
    exit 0
    ```

  - **Doğrula:** Sahte girdide izinli, engelli ve bozuk JSON vakaları test edilmiş; gerçek komutu çalıştırmadan sonuç görülüyor.
  - **Dayanak:** [Hook referansı](https://code.claude.com/docs/en/hooks)
- [ ] **7.7 Yeni depodaki hook ve MCP yapılandırmasını güvenmeden önce incele.** `İleri`
  - **Neden:** Proje ayarları yerel komut veya dış araç başlatabilir.
  - **Nasıl:** Settings, hook betikleri ve MCP sunucu komutlarını oku; paket kaynağını ve istenen yetkileri kontrol et.
  - **Doğrula:** Bilinmeyen komut otomatik çalıştırılmamış; güven kararı incelenen sürüme ait.
  - **Dayanak:** [Ayarlar](https://code.claude.com/docs/en/settings)

<a id="8-hook"></a>
## 8. Hook'lar

Hook belirli olaylarda çalışan bir mekanizmadır; güvenilirliği betiğin kapsamı, izinleri, hata davranışı ve testleriyle sınırlıdır.

- [ ] **8.1 Her oturuma girmesi gereken bilgiyi SessionStart hook'una koy.** `İleri`
  - **Neden:** Talimatı model unutabilir. Hook her oturumda çalışır.
  - **Nasıl:** Betiğin stdout'u oturumun bağlamına girer.

    ```
    "hooks": {
      "SessionStart": [{ "hooks": [{
        "type": "command",
        "command": "head -80 BEKLEYENLER.md 2>/dev/null || true"
      }]}]
    }
    ```

  - **Doğrula:** Okuma araçları kapalı bir `claude -p` ile içerikten soru sor.
  - **Dayanak:** [Hook referansı](https://code.claude.com/docs/en/hooks)
- [ ] **8.2 Biçimlendirmeyi düzenleme sonrası hook'a bağla.** `İleri`
  - **Neden:** Biçimi her seferinde istemek yerine her düzenlemeden sonra kendiliğinden düzelir.
  - **Nasıl:** PostToolUse içinde yalnız değişen, desteklenen dosyayı biçimlendiren bir betik çağır. Betik JSON girdisindeki yolu doğrulasın ve proje dışına çıkmasın; tüm depoyu her düzenlemede taramasın.

    ```
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command",
        "command": "python3 .claude/hooks/format_changed.py" }]
    }]
    # format_changed.py projene göre yazılmalı ve test edilmelidir.
    ```

  - **Doğrula:** Bozuk girintili bir dosya düzenlet, sonuç biçimli gelmeli.
  - **Dayanak:** [Hook referansı](https://code.claude.com/docs/en/hooks)
- [ ] **8.3 Bağlam göstergesini belgelenmiş statusline alanından üret.** `İleri`
  - **Neden:** Transcript iç yapısını token sayacı gibi ayrıştırmak sürüm değişiminde bozulabilir.
  - **Nasıl:** Statusline JSON girdisindeki `context_window.used_percentage` alanını kullan; ilk yanıt öncesi eksik/null değerini işle.
  - **Doğrula:** Sıfır, null ve yüksek doluluk örneklerinde gösterge doğru; bilinmeyen değer yüzde sıfır diye sunulmuyor.
  - **Dayanak:** [Durum satırı](https://code.claude.com/docs/en/statusline)
- [ ] **8.4 Hook'u test et ve bozarak testin düştüğünü gör.** `İleri`
  - **Neden:** Hiçbir şeye bakmayan hook da sessizce "çalışır".
  - **Nasıl:** Hook'a örnek bir JSON girdisi verip çıktısını kontrol eden küçük bir test.

    ```
    printf '%s\n' '{"cwd":"/tmp/ornek-proje"}' | sh .claude/hooks/oturum-basi.sh
    # Test: izinli, engelli ve bozuk JSON girdilerini ayrı doğrula.
    ```

  - **Doğrula:** Hook'u bilerek boz, test düşmeli.
  - **Dayanak:** [Hook referansı](https://code.claude.com/docs/en/hooks)
- [ ] **8.5 Hook hata politikasını görevine göre seç.** `İleri`
  - **Neden:** Bilgi gösteren hook ile güvenlik kapısı aynı hatada-devam kuralını kullanmamalıdır.
  - **Nasıl:** Bilgilendirme hatasını görünür kaydet; politika hook’unda hatayı sessizce başarıya çevirme. `onFailure: "block"` komut/HTTP hook’ları için v2.1.295+ gerektirir; eski sürümde yokmuş gibi davran.
  - **Doğrula:** Betiğin bulunamaması, bozuk JSON, hata çıkışı ve timeout ayrı denenmiş; engel gerektiğinde çağrı ilerlemiyor.
  - **Dayanak:** [Hook referansı](https://code.claude.com/docs/en/hooks)

<a id="9-yeniden"></a>
## 9. Skill, komut, ajan, MCP

Aynı tarifi üçüncü kez yazıyorsan, o tarif bir dosyaya aittir. Skill gerektiğinde yüklenir, ajan kendi bağlamında çalışır, MCP dış sisteme API ile bağlanır.

- [ ] **9.1 Eleştiriyi yazandan ayrı bir bağlama ver.** `Temel`
  - **Neden:** Ayrı bağlam farklı varsayımlarla inceleme yapabilir; bağımsızlık kalite garantisi değildir.
  - **Nasıl:** Statik inceleme için yazma ve Bash aracı olmayan doğrulayıcı ajan kullan. Test çalıştırmak gerekiyorsa ayrı, sınırlı ortam ve izin ver; Bash olan ajan salt okunur sayılmaz.

    ```
    ---
    name: dogrulayici
    description: Tamamlanan değişiklikte kanıtlı doğruluk hatalarını statik olarak inceler.
    tools: Read, Grep, Glob
    model: sonnet
    ---
    İddiaları diff ve kaynakla karşılaştır. Bulgu uydurma.
    Her bulguda dosya, tetikleyici ve etkisini yaz. Test çalıştırmadıysan belirt.
    ```

  - **Doğrula:** Bulgu varsa dosya ve kanıtı var; bulgu yoksa kapsam ve çalıştırılmayan kontroller açık.
  - **Dayanak:** [Alt ajanlar](https://code.claude.com/docs/en/sub-agents)
- [ ] **9.2 Üçüncü kez anlattığın işi skill'e çevir.** `İleri`
  - **Neden:** Tarif her seferinde biraz farklı anlatılır, sonuç da farklı çıkar.
  - **Nasıl:** `~/.claude/skills//SKILL.md`.

    ```
    ---
    name: surum-notu
    description: Son etiketten bu yana değişikliklerden kullanıcıya dönük sürüm notu yazar. "Sürüm notu", "release notes" denince kullan. Teknik changelog için kullanma.
    ---
    1. git log ile son etiketten bu yanaki commit'leri al.
    2. Kullanıcının fark edeceği değişiklikleri seç, en fazla 5.
    3. Her maddeyi kullanıcının diliyle bir cümlede yaz.
    ```

  - **Doğrula:** Açık /surum-notu çağrısı ve doğal dille eşleşen istek ayrı denenmiş; otomatik seçilmeme de kaydedilmiş.
  - **Dayanak:** [Skills](https://code.claude.com/docs/en/skills)
- [ ] **9.3 Skill açıklamasına "kullanma" sınırı koy.** `İleri`
  - **Neden:** Model skill'i açıklamadan seçer. Sınır yoksa komşu işlerde de yüklenir.
  - **Nasıl:** Açıklamaya hem tetikleyici ifadeleri hem de kullanılmayacağı durumu yaz (yukarıdaki örnekteki son cümle).
  - **Doğrula:** Benzer ama farklı bir istekte skill yüklenmemeli.
  - **Dayanak:** [Skills](https://code.claude.com/docs/en/skills)
- [ ] **9.4 Yan etkili skill'i kendiliğinden çalışmaya kapat.** `İleri`
  - **Neden:** Deploy ya da mesaj gönderen bir skill yanlış eşleşmede çalışmasın.
  - **Nasıl:** Frontmatter’da `disable-model-invocation: true` otomatik çağrıyı kapatır; araç izinleri veya kullanıcı yetkisi yerine geçmez. Etkin skill override ayarını da kontrol et.

    ```
    disable-model-invocation: true
    ```

  - **Doğrula:** İlgili cümleyi yaz, skill kendiliğinden çalışmamalı.
  - **Dayanak:** [Skills](https://code.claude.com/docs/en/skills)
- [ ] **9.5 Bir uygulamaya bağlanırken önce o uygulamanın MCP'sini dene.** `İleri`
  - **Neden:** API tabanlı araç hızlı ve kesin. Ekranda tıklayarak sürmek yavaş ve kırılgan.
  - **Nasıl:** Sıra: uygulamanın MCP'si, sonra tarayıcı, en son bilgisayar kontrolü.
  - **Doğrula:** Aynı iş için kaç araç çağrısı gittiğine bak.
  - **Dayanak:** [MCP](https://code.claude.com/docs/en/mcp)
- [ ] **9.6 Kendi setini plugin olarak paketle.** `İleri`
  - **Neden:** Başka makineye ya da ekip arkadaşına tek komutla taşınır.
  - **Nasıl:** `.claude-plugin/plugin.json` ve skill dizinleri.
  - **Doğrula:** Temiz bir makinede kurulumdan sonra skill listede görünmeli.
  - **Dayanak:** [Plugins](https://code.claude.com/docs/en/plugins)
- [ ] **9.7 MCP bağlantısına yalnız gereken kapsamı ver.** `İleri`
  - **Neden:** Bağlantının çalışması doğru hesap ve en az yetki anlamına gelmez.
  - **Nasıl:** `/mcp` ile sunucu ve hesap durumunu incele; okuma/yazma yetkisini ayır, gereksiz bağlantıyı kaldır.
  - **Doğrula:** Zararsız okuma testi doğru hedefte; yazma ayrıca kullanıcının yetki kapsamıyla eşleşiyor.
  - **Dayanak:** [MCP](https://code.claude.com/docs/en/mcp)
- [ ] **9.8 Skill’i olumlu ve olumsuz örneklerle değerlendir.** `İleri`
  - **Neden:** Tek başarılı çağrı yanlış eşleşmeleri ve eksik çıktıları yakalamaz.
  - **Nasıl:** Tetiklenmesi gereken, gerekmeyen ve hata durumunu içeren küçük vaka seti tut; beklenen sonucu baştan yaz.
  - **Doğrula:** Gerekli çağrıda doğru çıktı, komşu istekte gereksiz çağrı yok; başarısız vaka saklanmış.
  - **Dayanak:** [Skills](https://code.claude.com/docs/en/skills)

<a id="10-ekip"></a>
## 10. Ekiple kullanım

Bir kişinin iyi düzeni, ekip için de düzen olabilir. Ama ortak dosyaya giren her şey herkesin oturumunu etkiler.

- [ ] **10.1 Ortak ayarları `.claude/settings.json`'da, kişisel olanları `settings.local.json`'da tut.** `İleri`
  - **Neden:** Ekibin izin listesi ve hook'ları git ile paylaşılır, kişisel tercihin başkasına geçmez.
  - **Nasıl:** `settings.json` commit'lenir, `settings.local.json` git dışında kalır. Öncelik sırası yukarıdan aşağı: yönetilen ayarlar, komut satırı, `settings.local.json`, `settings.json`, kullanıcı ayarları.
  - **Doğrula:** Yeni ekip üyesi dosyaları ve etkin politikayı doğruluyor; yönetilen ayar veya kişisel mod farkı aynı izin garantisi sayılmıyor.
  - **Dayanak:** [Ayarlar](https://code.claude.com/docs/en/settings)
- [ ] **10.2 Proje CLAUDE.md'sini kod gibi gözden geçir.** `İleri`
  - **Neden:** Bir kural bütün ekibin oturumunu değiştirir.
  - **Nasıl:** CLAUDE.md değişikliği de pull request'ten geçsin.
  - **Doğrula:** Son ay eklenen kuralların gerekçesi commit mesajında yazıyor mu?
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **10.3 Ekipte tekrar eden işi ortak skill ya da plugin yap.** `İleri`
  - **Neden:** Herkes aynı işi kendi tarifinle yaptırınca sonuçlar tutarsız olur.
  - **Nasıl:** Repoda `.claude/skills/` ya da ekip plugin'i.
  - **Doğrula:** İki kişinin aynı skill ile ürettiği çıktı aynı biçimde.
  - **Dayanak:** [Skills](https://code.claude.com/docs/en/skills)

<a id="11-paralel"></a>
## 11. Paralel çalışma

Aynı anda çok oturum çalıştırmak güçlü bir kaldıraç. Ama her paylaşılan kaynak bir çakışma noktası ve makine yükü her şeyi yavaşlatır.

- [ ] **11.1 Aynı dosyalara iki yazar sokma. Her yazar ayrı worktree'de.** `İleri`
  - **Neden:** İki oturum aynı dosyayı düzenlerse biri diğerinin işini ezer.
  - **Nasıl:** Worktree ile başlat.

    ```
    claude --worktree odeme-ekrani
    ```

  - **Doğrula:** `git worktree list`'te her yazar için ayrı satır.
  - **Dayanak:** [İş akışları](https://code.claude.com/docs/en/common-workflows)
- [ ] **11.2 Git index’ini ortak yazarlardan ayır ve commit kapsamını incele.** `İleri`
  - **Neden:** Aynı checkout index’i ortaktır; ayrı worktree index’leri ayrıdır. İki komutu && ile birleştirmek atomik kilit sağlamaz.
  - **Nasıl:** Ayrı worktree kullan, yalnız kendi değişikliklerini stage et ve commit öncesi staged diff’i incele.

    ```
    git status --short
    git add -- src/odeme.ts
    git diff --cached -- src/odeme.ts
    git commit -m "Ödeme: kart doğrulama"
    # Önceden stage edilmiş başka dosya varsa önce kapsamı ayır.
    ```

  - **Doğrula:** Commit diff’inde başka işin değişikliği yok.
  - **Dayanak:** [Git worktree](https://git-scm.com/docs/git-worktree)
- [ ] **11.3 Port ve tarayıcı oturumunu projeye özel yap.** `İleri`
  - **Neden:** Aynı porttaki iki sunucu birbirini düşürür, yanlış sayfa test edilir.
  - **Nasıl:** Her projeye sabit ve farklı bir port.
  - **Doğrula:** Açılan sayfa gerçekten bu projenin sayfası.
  - **Dayanak:** İş akışı önerisi
- [ ] **11.4 Ağır oturum sayısını makine yüküne göre sınırla.** `İleri`
  - **Neden:** Kaynak baskısı yavaşlama ve kararsız testlerle birlikte görülebilir; tek yük ölçümü nedeni kanıtlamaz.
  - **Nasıl:** CPU, bellek baskısı, disk ve aktif işleri birlikte izle; bağımsız ağır işi kaynaklara göre sırala.
  - **Doğrula:** Bekleme süresi ve başarısızlıklar ölçülmüş; sabit bir load-average eşiği her makineye uygulanmıyor.
  - **Dayanak:** İş akışı önerisi
- [ ] **11.5 Uzun gözetimsiz işi bulut oturumuna gönder.** `İleri`
  - **Neden:** Makineyi yormaz, uyku onu öldürmez.
  - **Nasıl:** Uygulamada bulut hedefli oturum. Yerel cihaz isteyen iş yerelde kalır.
  - **Doğrula:** Bilgisayar kapalıyken iş ilerlemiş olmalı.
  - **Dayanak:** İş akışı önerisi
- [ ] **11.6 Çok ajanlı iş akışını yalnız gerçekten paralel işe kullan.** `İleri`
  - **Neden:** Onlarca ajan çok token harcar. Sıralı iş paralelden kazanmaz.
  - **Nasıl:** Bağımsız parçalar için, örneğin on dosyanın ayrı ayrı incelenmesi.
  - **Doğrula:** İş akışı sonrası kullanım farkına `/usage`'dan bak.
  - **Dayanak:** [Alt ajanlar](https://code.claude.com/docs/en/sub-agents)

<a id="12-dogrulama"></a>
## 12. Doğrulama

"Geçti" demek bir iddia, kanıt değil. En tehlikeli yeşil, hiçbir şeye bakmadığı için yeşil olandır.

- [ ] **12.1 Sonuçta durumu değil sayıyı oku.** `Temel`
  - **Neden:** Eşleşmeyen bir test filtresi sıfır test koşup başarılı diyebilir.
  - **Nasıl:** Raporda test sayısını iste.

    ```
    Yeşil görünen ama boş:  Test run with 0 tests ... SUCCEEDED
    Gerçek:               Executed 42 tests, with 0 failures
    ```

  - **Doğrula:** Her "geçti"nin yanında bir sayı.
  - **Dayanak:** İş akışı önerisi
- [ ] **12.2 Yeni kontrolü hatayı geri koyarak doğrula.** `Temel`
  - **Neden:** Kontrol gerçekten bakıyorsa bozuk kodda düşmeli.
  - **Nasıl:** İzole fixture veya geçici branch’te kusuru geri getir; testin düştüğünü ve düzeltilmiş eşinin geçtiğini göster. Kullanıcının çalışma dosyasını koru.

    ```
    Yazdığın testin gerçekten çalıştığını kanıtla: fiyat hesabındaki
    indirimi geçici olarak kaldır, testi koş, düştüğünü göster, sonra geri al.
    ```

  - **Doğrula:** Bozuk sürümde kırmızı.
  - **Dayanak:** İş akışı önerisi
- [ ] **12.3 Alt ajanın raporunu kanıtla karşılaştır.** `Temel`
  - **Neden:** Ajan raporu bir iddiadır.
  - **Nasıl:** Diff'e, dosyaya, çıktıya bak. Ondan sonra "bitti" de.
  - **Doğrula:** Rapordaki bir iddiayı rastgele seç ve doğrula.
  - **Dayanak:** İş akışı önerisi
- [ ] **12.4 İş sonunda üç satır istet: kaçırılan, en zayıf iddia, gerekçesiz karar.** `İleri`
  - **Neden:** Övgü değil kırma denemesi, sorunun kendisini sana getirir.
  - **Nasıl:** CLAUDE.md'ye tek kural ya da bir slash komutu.

    ```
    İş bitince sormadan üç satır yaz:
    1. Neyi kaçırmış olabilirim (bakmadığım dosya, koşmadığım yol)
    2. Hangi iddiam en zayıf
    3. Hangi kararım gerekçesiz
    ```

  - **Doğrula:** Üç satırın her biri somut bir dosya ya da karar adı içeriyor mu?
  - **Dayanak:** İş akışı önerisi
- [ ] **12.5 Görsel değişikliği önce/sonra ekran görüntüsüyle gör.** `İleri`
  - **Neden:** "Ne değişti" sorusu metinle cevaplanmaz.
  - **Nasıl:** İki ekran görüntüsü yan yana.
  - **Doğrula:** Farkı ilk bakışta görebiliyor musun?
  - **Dayanak:** İş akışı önerisi
- [ ] **12.6 Önemli değişikliği teslimden önce kod incelemesinden geçir.** `İleri`
  - **Neden:** Yazan bağlam kendi hatasını kaçırır.
  - **Nasıl:** `/code-review` ile hedef diff’i incele. `--fix` değişiklik yapar, `--comment` dışarı yorum gönderir; bunları amaç ve yetki olmadan ekleme.
  - **Doğrula:** Bulgu ve kanıtları veya kapsamı belirtilmiş “bulgu yok” sonucu var; test yapılmadıysa ayrı yazıyor.
  - **Dayanak:** [Komutlar](https://code.claude.com/docs/en/commands)
- [ ] **12.7 Teslim aşamasını kanıtıyla adlandır.** `İleri`
  - **Neden:** Yerel test, push ve herkese açık yayın farklı sonuçlardır.
  - **Nasıl:** PASS, FAIL, NOT_RUN ve BLOCKED durumlarını ilgili komut, tarih ve sürümle kaydet; dış hedefi tekrar oku.
  - **Doğrula:** Build geçti diye cihaz testi, upload oldu diye canlı yayın geçti denmiyor.
  - **Dayanak:** İş akışı önerisi

<a id="13-gozetimsiz"></a>
## 13. Gözetimsiz koşum

"Ben yatıyorum, sabaha bitir" dediğin iş, sabah çalışan bir sonuç bırakmalı. Gece boyu izin ekranında beklemek ya da sessizce ölmek en pahalı başarısızlık.

- [ ] **13.1 Gözetimsiz koşum için talimat setini önceden yaz.** `İleri`
  - **Neden:** "Sormadan ilerle" demek, hangi durumda ne yapılacağını söylemez.
  - **Nasıl:** İşe özel yetki, kapsam, bütçe ve engel davranışını belirt; her proje için sınırsız global yetki yazma.

    ```
    ## Bu görevde ben yokken
    - Yetkili kapsam içindeki geri alınabilir kararları ver, varsayımı yaz.
    - Eksik yetki veya sonucu değiştiren karar varsa ilgili adımı engelli işaretle.
    - Bağımsız işleri tamamla; başarısız testi gizleme.
    - Sonuç: yapılan, yapılmayan, kanıt, kalan karar ve kaynak temizliği.
    ```

  - **Doğrula:** Bir koşumu dene, sabah rapor eksiksiz mi?
  - **Dayanak:** İş akışı önerisi
- [ ] **13.2 Ayrılmadan önce izin, disk, yük ve uyku koşullarını doğrula.** `İleri`
  - **Neden:** Bu dördünden biri geceyi boşa çıkarır.
  - **Nasıl:** İzinleri etkin ayardan, kaynakları işletim sistemi araçlarından kontrol et. macOS örneği aşağıda; diğer sistemlerde eşdeğerini kullan.

    ```
    df -h .
    uptime
    pmset -g
    # Claude oturumunda /permissions ile etkin izinleri incele.
    ```

  - **Doğrula:** Dört kontrolün sonuçları ve sınırları yazılmış; ilk 20 ayar satırını okumak bütün izin denetimi sayılmıyor.
  - **Dayanak:** İş akışı önerisi
- [ ] **13.3 Uzun işi kaldığı yerden devam edecek biçimde kur.** `İleri`
  - **Neden:** Uyku ya da çökme işi baştan başlatmasın.
  - **Nasıl:** Ara çıktıyı diske yaz, her adım öncesi "bu adım bitti mi" kontrolü.
  - **Doğrula:** İşi yarıda öldür, yeniden başlat, tamamlanan adımlar atlanmalı.
  - **Dayanak:** İş akışı önerisi
- [ ] **13.4 Zamanlanmış oturumda uzun işi arka plana atıp turu kapatma.** `İleri`
  - **Neden:** Arka plan süreci oturumla birlikte ölebilir ve geriye log bile kalmayabilir.
  - **Nasıl:** Turu açık tut, log'u oturumdan bağımsız bir yola yaz.
  - **Doğrula:** Sabah log'un son satırı işin bitişini gösteriyor mu?
  - **Dayanak:** [Masaüstü](https://code.claude.com/docs/en/desktop)
- [ ] **13.5 İş bitince açık kaynakları kapat.** `İleri`
  - **Neden:** Açık kalan simülatör, sunucu ya da tarayıcı belleği ve diski tüketir.
  - **Nasıl:** Koşum sonunda kendi açtığın süreçleri kapat, başka oturumunkine dokunma.
  - **Doğrula:** Sabah yalnız beklediğin süreçler açık.
  - **Dayanak:** İş akışı önerisi
- [ ] **13.6 Geçici derleme ve bağımlılıkları görev sonunda hedefli temizle.** `İleri`
  - **Neden:** Göreve özel ürün ve cache diskte birikir; isim benzerliği sahiplik kanıtı değildir.
  - **Nasıl:** Başta kesin yolları kaydet. Kullanım bitince logları ve teslim dosyalarını koruyup yalnız göreve ait yeniden üretilebilir artıkları kaldır.
  - **Doğrula:** Silinen yol yok; kaynak, release arşivi, sonuç ve paylaşılan cache korunmuş.
  - **Dayanak:** İş akışı önerisi

<a id="14-rutin"></a>
## 14. Rutinler ve zamanlama

Tekrarlanan işi elle tetiklemek unutulur. Ama bilgisayar kapanınca ölen bir rutin de güvenilir değildir.

- [ ] **14.1 Zamanlamanın nerede çalıştığını açıkça seç.** `İleri`
  - **Neden:** Bulut görevleri bilgisayarından bağımsızdır; yerel Desktop işi cihaz ve uygulama koşullarına bağlıdır.
  - **Nasıl:** Bulut görevleri için `/schedule` ve desteklenen claude.ai hesabını kontrol et. Araştırma önizlemesinin koşulları değişebilir; Desktop ve oturum içi döngüyü aynı mekanizma sanma.
  - **Doğrula:** Doğru ortamda bir deneme koşumu, sonraki çalışma zamanı ve sonuç bağlantısı görülmüş.
  - **Dayanak:** [Bulut zamanlama](https://code.claude.com/docs/en/routines)
- [ ] **14.2 Headless rutinde çıktıyı ve tur sayısını sınırla.** `İleri`
  - **Neden:** Sınırsız koşum takılı kalınca saatlerce harcar.
  - **Nasıl:** JSON çıktı, tur sınırı, kendi log yolu.

    ```
    mkdir -p work/runs
    claude -p "$(cat gorev.md)" --output-format json --max-turns 30 \
      > work/runs/sonuc.json 2> work/runs/hata.log
    sonuc=$?
    printf '%s\n' "$sonuc" > work/runs/exit-code.txt
    exit "$sonuc"
    ```

  - **Doğrula:** JSON parse ediliyor, hata/başarı alanı ve süreç çıkış kodu birlikte kaydediliyor; limit dolması başarı değil.
  - **Dayanak:** [Headless kullanım](https://code.claude.com/docs/en/headless)
- [ ] **14.3 Rutinin sessiz ölümünü ayrı bir nöbetle yakala.** `İleri`
  - **Neden:** Hiç koşmayan rutin hata da vermez.
  - **Nasıl:** Son başarılı koşumun zamanını kontrol eden ikinci küçük bir rutin.
  - **Doğrula:** Bir rutini bilerek durdur, nöbet uyarmalı.
  - **Dayanak:** İş akışı önerisi
- [ ] **14.4 Dış servis kotasına uy ve yeniden denemeyi sınırla.** `İleri`
  - **Neden:** Eşzamanlı istekler kotayı tüketebilir; zamanları rastgele dağıtmak erişim engelini aşma yöntemi değildir.
  - **Nasıl:** Servis koşullarına ve Retry-After yanıtına uy; sınırlı geri çekilme ve jitter uygula.
  - **Doğrula:** 429/503 denemesinde bekleme ve azami deneme sayısı doğru; engelde görev durumu açık.
  - **Dayanak:** İş akışı önerisi
- [ ] **14.5 Oturum içi /loop ile kalıcı zamanlamayı ayır.** `İleri`
  - **Neden:** /loop çalışan oturumun yaşam döngüsüne bağlıdır; cihazdan bağımsız bulut görevi değildir.
  - **Nasıl:** `/loop 5m` gibi sabit aralıklı döngünün görev kaydını ve durdurma biçimini kontrol et; bilgisayardan bağımsız işte bulut zamanlamasını seç.

    ```
    /loop 5m Yayının tamamlanıp tamamlanmadığını kontrol et;
    anlamlı değişiklikte bildir, tamamlanınca döngüyü iptal et.
    ```

  - **Doğrula:** Bir deneme tetiklenmiş, iptal sonrası yeni koşum yok; oturum kapalıyken çalışma varsayılmıyor.
  - **Dayanak:** [Oturum içi zamanlama](https://code.claude.com/docs/en/scheduled-tasks)
- [ ] **14.6 Headless başarısını süreç ve sonuç alanından birlikte doğrula.** `İleri`
  - **Neden:** Geçerli JSON üretmek işin tamamlandığını göstermez.
  - **Nasıl:** Çıkış kodu, `is_error`, sonuç türü ve kabul ölçütünü değerlendir; yarım işi tekrar koşarken yan etkileri çoğaltma.
  - **Doğrula:** İzin reddi ve tur sınırı vakaları hata/eksik olarak görünür; başarılı eşinde kabul ölçütü sağlanır.
  - **Dayanak:** [Headless kullanım](https://code.claude.com/docs/en/headless)

<a id="15-git"></a>
## 15. Git ve yayın

Git, Claude ile çalışırken en güvenilir geri alma düğmesi. Sık commit, Claude'a cesur değişiklik yaptırmanın güvencesi.

- [ ] **15.1 Kaynak kodunu Git’te tut ve commit kapsamını tanımla.** `Temel`
  - **Neden:** Küçük, anlamlı commit geri almayı kolaylaştırır. Git dışı veriler ve sırlar için ayrıca uygun yedek gerekir.
  - **Nasıl:** `git init`, sonra CLAUDE.md'ye commit kuralı.

    ```
    - Sormadan commit at, mantıklı parçalara böl.
    - Push ve deploy yalnız açıkça istendiğinde.
    ```

  - **Doğrula:** `git log --oneline`'da her satır tek bir değişikliği anlatıyor.
  - **Dayanak:** [Git worktree](https://git-scm.com/docs/git-worktree)
- [ ] **15.2 Checkpoint'in sınırını bil.** `Temel`
  - **Neden:** `/rewind` yalnız dosya araçlarıyla yapılan düzenlemeleri geri alır. Bash'le silinen ya da taşınanı almaz.
  - **Nasıl:** Bash'le toplu değişiklikten önce commit.
  - **Doğrula:** Commit öncesi diff incelenmiş; Bash, dış servis ve veritabanı etkileri için ayrı geri alma yolu var.
  - **Dayanak:** [Checkpoint](https://code.claude.com/docs/en/checkpointing)
- [ ] **15.3 Push ve deploy yetkisini hedefe ve kapsama bağla.** `İleri`
  - **Neden:** Uzak depo ve yayın hedefi yerel değişiklikten farklı bir teslim aşamasıdır.
  - **Nasıl:** Kullanıcının mevcut yayın talimatını koru; belirsiz hedef veya yeni dış taahhütte karar iste. Geniş, kalıcı push/deploy iznini varsayılan yapma.
  - **Doğrula:** Doğru hesap, repo, dal ve görünürlük doğrulanmış; yayından sonra canlı sonuç okunmuş.
  - **Dayanak:** [İzinler](https://code.claude.com/docs/en/permissions)
- [ ] **15.4 Commit atfını talimatla değil ayarla yönet.** `İleri`
  - **Neden:** Talimat unutulabilir, ayar her commit'te uygulanır.
  - **Nasıl:** `attribution` ayarı (`includeCoAuthoredBy` eskidi). Boş metin o atfı gizler, `false` hepsini gizler (v2.1.281 ve sonrası).

    ```
    { "attribution": { "commit": "", "pr": "" } }
    ```

  - **Doğrula:** Ayardan sonraki ilk commit'te atıf satırı beklediğin gibi.
  - **Dayanak:** [Ayar referansı](https://code.claude.com/docs/en/settings-reference)

<a id="16-tasarim"></a>
## 16. Tasarım ve arayüz

Tasarımda en pahalı döngü "beğenmedim, tekrar dene". Onu kısaltan şey araştırma, birden çok yön ve görsel karşılaştırma.

- [ ] **16.1 Tasarımdan önce gerçek örneklerden ilham topla.** `İleri`
  - **Neden:** İlhamsız ilk taslak şablona yakın çıkar.
  - **Nasıl:** Kaynaklı bir ilham raporu iste.

    ```
    Alışkanlık uygulamalarından 8 örnek bul, ana ekranlarını karşılaştır.
    Her biri için: neyi iyi yapıyor, bizim uygulamaya ne alınabilir, kaynak.
    ```

  - **Doğrula:** Her öneri bir gerçek örneğe dayanıyor mu?
  - **Dayanak:** İş akışı önerisi
- [ ] **16.2 İki-üç farklı yönü tam ekran çizdir.** `İleri`
  - **Neden:** Anlatılan tasarım kafada farklı canlanır, alt alanlar unutulur.
  - **Nasıl:** Her yönü alt alanlar dahil tam ekran iste.
  - **Doğrula:** Seçimini görsele bakarak yapabiliyor musun?
  - **Dayanak:** İş akışı önerisi
- [ ] **16.3 Beğenmediğinde aynı yönü değil, farklı bir yönü iste.** `İleri`
  - **Neden:** Rötuş aynı fikrin varyasyonunu üretir.
  - **Nasıl:** Neyin çalışmadığını söyle ve yön değişikliği iste.

    ```
    Bu yönden çık. Kart dizisi yerine tek bir odak alanı dene,
    renk değil boşluk ve tipografiyle hiyerarşi kur.
    ```

  - **Doğrula:** Yeni öneri ilkinden yapısal olarak farklı mı?
  - **Dayanak:** İş akışı önerisi
- [ ] **16.4 Tasarım dilini bir kez yaz, her turda yeniden anlatma.** `İleri`
  - **Neden:** Renk, tipografi ve boşluk kuralları her seferinde sohbetle aktarılınca kayar.
  - **Nasıl:** Projede tasarım ilkeleri dosyası ya da tasarım skill'i.
  - **Doğrula:** Yeni oturumda tasarım dili sorulunca dosyadan cevap gelmeli.
  - **Dayanak:** İş akışı önerisi

<a id="17-mobil"></a>
## 17. Mobil ve simülatör

iOS ya da Android uygulaması geliştiriyorsan simülatör en çok kullanılan araç olur. Paylaşılan cihaz, elle tıklama ve açık kalan simülatör en sık zaman kaybı.

- [ ] **17.1 Paralel testlerde cihaz sahipliğini ve UDID’yi kaydet.** `İleri`
  - **Neden:** Paylaşılan simülatörde başka oturumun uygulaması öne gelir, senin uygulaman bozuk sanılır.
  - **Nasıl:** Önce mevcut cihaz ve runtime listesini oku; gerekli ise göreve özel cihaz oluştur, dönen UDID’yi kaydet.

    ```
    xcrun simctl list devices available
    xcrun simctl list devicetypes
    xcrun simctl list runtimes
    # create için bu listelerdeki geçerli tip ve runtime kimliğini kullan.
    ```

  - **Doğrula:** Testin cihazı, runtime’ı ve uygulama build’i kayıtlı; başka görevin cihazı değiştirilmemiş.
  - **Dayanak:** İş akışı önerisi
- [ ] **17.2 Tekrarlanan arayüz akışını otomatik teste çevir.** `İleri`
  - **Neden:** Elle tıklayarak doğrulama her seferinde aynı maliyeti öder.
  - **Nasıl:** Maestro, XCUITest ya da Espresso akışı, tek komutla koşan.

    ```
    appId: com.ornek.fiyat
    ---
    - launchApp
    - tapOn: "Ürün ekle"
    - inputText: "Kahve"
    - assertVisible: "Kahve"
    ```

  - **Doğrula:** Akış bozuk bir ekranda kırmızı dönmeli.
  - **Dayanak:** İş akışı önerisi
- [ ] **17.3 Türkçe metin girişini kullanılan araçta gerçekten dene.** `İleri`
  - **Neden:** Bazı otomasyon giriş yöntemleri Unicode veya klavye davranışını eksik taklit edebilir.
  - **Nasıl:** Desteklenen giriş yolunu seç; İstanbul, ışık ve çığ gibi metinleri ekranda ve kaydedilen veride karşılaştır. ASCII yardımcı fixture gerçek dil testinin yerine geçmesin.
  - **Doğrula:** Girilen, gösterilen ve kaydedilen metin eşit; denenemeyen giriş yolu NOT_RUN.
  - **Dayanak:** İş akışı önerisi
- [ ] **17.4 Farklı ekran boyutlarında kontrol et.** `İleri`
  - **Neden:** Küçük ekranda taşan metin büyük ekranda görünmez.
  - **Nasıl:** En küçük ve en büyük desteklenen cihazda ekran görüntüsü.
  - **Doğrula:** İki görüntüde de taşma yok.
  - **Dayanak:** İş akışı önerisi
- [ ] **17.5 Göreve ait geçici simülatörü kanıtları koruyup sil.** `İleri`
  - **Neden:** Shutdown cihazın veri alanını kaldırmaz; erase de cihaz kaydını silmez.
  - **Nasıl:** Önce log ve ekran görüntülerini dışarı al, aktif kullanıcı olmadığını doğrula. Yalnız bu görevde oluşturduğun kesin UDID’yi kapat ve sil.

    ```
    xcrun simctl shutdown <GOREVE_AIT_UDID>
    xcrun simctl delete <GOREVE_AIT_UDID>
    xcrun simctl list devices --json
    ```

  - **Doğrula:** UDID cihaz listesinden kalkmış; önceden var olan veya sahibi belirsiz cihaz korunmuş.
  - **Dayanak:** İş akışı önerisi

<a id="18-bilgi"></a>
## 18. Bilgi birikimi

Öğrenilen ders yazılmazsa bir sonraki oturumda yeniden öğrenilir. Yanlış yere yazılırsa da kaybolur.

- [ ] **18.1 Dersi doğru katmana yaz.** `İleri`
  - **Neden:** Makine gerçeği bir proje dosyasında kalırsa diğer projelere görünmez.
  - **Nasıl:** "Bu cümle nerede doğru olmaktan çıkıyor" diye sor.

    ```
    Makine ve araç gerçeği   -> ~/.claude/CLAUDE.md
    Koda ait gerçek          -> proje CLAUDE.md
    Repo + bu makine         -> CLAUDE.local.md
    Tarihli ölçüm, kanıt     -> ayrı kanıt dosyası
    ```

  - **Doğrula:** Her yeni kural doğru dosyada mı?
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **18.2 "Sonra" ve "unutma" denen her şeyi hemen dosyaya yazdır.** `İleri`
  - **Neden:** Oturum içi hafıza devirde kaybolur.
  - **Nasıl:** Proje kökünde bekleyenler dosyası, CLAUDE.md'de buna dair tek kural.
  - **Doğrula:** "Neler kaldı" sorusu dosyadan cevaplanıyor.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **18.3 Aynı düzeltme üçüncü kez geldiyse kural yap.** `İleri`
  - **Neden:** Üçüncü tekrar artık tesadüf değil.
  - **Nasıl:** Düzeltmeyi say, üçte kurala çevir.
  - **Doğrula:** Son ayın düzeltmelerinden kaçı kurala dönüştü?
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **18.4 Kuralı kısa, kanıtını ayrı tut.** `İleri`
  - **Neden:** Kısa kural bağlamda taşınır, uzun kanıt yalnız gerektiğinde açılır.
  - **Nasıl:** Kuralın sonunda kanıt dosyasına bir atıf.
  - **Doğrula:** Her global kuralın bir kanıt atfı var mı?
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)

<a id="19-bakim"></a>
## 19. Bakım ritmi

Ayarlar, kurallar ve izin listeleri zamanla eskir. Küçük ve düzenli bakım, büyük temizlikten ucuzdur.

- [ ] **19.1 Haftalık: kullanımı ve bekleyenleri gözden geçir.** `İleri`
  - **Neden:** Limiti ve yarım işleri hafta bitmeden görürsün.
  - **Nasıl:** `/usage` ve aktif projelerin bekleyenler dosyası.
  - **Doğrula:** Haftalık not: en çok harcayan proje, en eski bekleyen madde.
  - **Dayanak:** [Kullanım ve maliyet](https://code.claude.com/docs/en/costs)
- [ ] **19.2 Eski worktree ve disk kullanımını sahiplik bilgisiyle gözden geçir.** `İleri`
  - **Neden:** Disk doluluğu derleme ve testleri aksatabilir; tek bir yüzde bütün projeler için yeterli sınır değildir.
  - **Nasıl:** Aktif süreç, yerel değişiklik ve kurtarma ihtiyacını kontrol et. `prune` yalnız eski yönetim kayıtlarını temizler; kullanılan checkout’u kaldırmaz.

    ```
    git worktree list
    git worktree prune --dry-run
    df -h .
    ```

  - **Doğrula:** Kaldırılan kesin yol ve korunmuş kanıt belli; boş alan işin beklenen derleme ihtiyacına yeterli.
  - **Dayanak:** [Git worktree](https://git-scm.com/docs/git-worktree)
- [ ] **19.3 Aylık: CLAUDE.md'leri buda.** `İleri`
  - **Neden:** Kurallar birikir, bazıları artık hiç tetiklenmez.
  - **Nasıl:** Geçerliliğini kaybeden kuralı düzelt; seyrek ama kritik olanı sırf geçen ay tetiklenmedi diye silme.
  - **Doğrula:** Çelişen veya eski kurallar düzeltilmiş; dosyanın küçük olması tek başına başarı ölçütü değil.
  - **Dayanak:** [Talimat ve bellek](https://code.claude.com/docs/en/memory)
- [ ] **19.4 Aylık: izin listelerini ve hook testlerini gözden geçir.** `İleri`
  - **Neden:** Yeni komutlar eklenir, Claude Code güncellemesi hook girdisini değiştirebilir.
  - **Nasıl:** `/fewer-permission-prompts`, ardından hook testleri.
  - **Doğrula:** Gözetimsiz koşumlarda izin bekleyen adım yok, testler yeşil.
  - **Dayanak:** [Hook referansı](https://code.claude.com/docs/en/hooks)
- [ ] **19.5 Çeyrekte bir: kendi kullanım analizini çıkar.** `İleri`
  - **Neden:** Alışkanlığın değişip değişmediğini sayı söyler.
  - **Nasıl:** Claude'dan oturum kayıtlarını taramasını iste.

    ```
    ~/.claude/projects altındaki oturum kayıtlarını tara. Çıkar:
    mesaj sayısı, en sık kısa mesajlar ("devam" gibi), bağlam dolma sayısı,
    alt ajan çağrılarının model dağılımı. Önceki çeyrekle karşılaştır.
    ```

  - **Doğrula:** Sonuçları önceki çeyrekle karşılaştır.
  - **Dayanak:** [Kullanım ve maliyet](https://code.claude.com/docs/en/costs)
- [ ] **19.6 Sürüm, platform ve sağlayıcı farkını kaydet.** `İleri`
  - **Neden:** Belgede olan özellik eski CLI’da, başka sağlayıcıda veya masaüstü arayüzünde aynı olmayabilir.
  - **Nasıl:** `claude --version`, `claude --help` ve ilgili komut menüsünü kontrol et; sürüm yükseltmesini kurulum yöntemine göre yap.
  - **Doğrula:** Rapor ortamı ve erişilemeyen özelliği belirtir; belge kontrolü canlı çalışma testi sayılmaz.
  - **Dayanak:** [Genel bakış](https://code.claude.com/docs/en/overview)

## Kaynak ve doğrulama

[Kaynaklar](KAYNAKLAR.md) · [Doğrulama](DOGRULAMA.md) · [Değişiklikler](GUNCELLEMELER.md)


## Güncelleme

İçerik tek dosyada: `kaynak/veri.py`. Değiştirdikten sonra:

```sh
python3 kaynak/yap.py
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer \
  --print-to-pdf=claude-code-kontrol-listesi.pdf "file://$PWD/kaynak/pdf.html"
```

## Lisans

[CC BY 4.0](LICENSE): kaynak göstererek paylaşabilir ve uyarlayabilirsin.

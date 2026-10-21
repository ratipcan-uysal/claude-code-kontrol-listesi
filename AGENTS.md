# Bu depoda çalışma

- İçerik kaynağı `kaynak/veri.py`; üretici `kaynak/yap.py`, tarayıcı davranışı `kaynak/app.js`.
- Üretilmiş README/index dosyasını tek başına düzenleme. `python3 kaynak/yap.py` çalıştır; PDF’yi de güncelle.
- Mevcut bölüm sırasını ve madde sırasını koru. Yeni madde bölüm sonuna eklenir; işaret kimlikleri ve `cc-kontrol-v2` anahtarı kullanıcı verisidir.
- Teknik iddiayı resmî kaynakla ve sürüm/platform sınırıyla ilişkilendir. Editoryal tercih ölçülmüş sonuç veya ürün şartı değildir.
- Yapısal testleri çalıştır. Etkilenen sayfa işlevlerini gerçek tarayıcıda, PDF’yi render ederek kontrol et.
- Yerel başarı, GitHub push, Pages build ve anonim canlı erişimi ayrı doğrula. NOT_RUN durumunu koru.
- Kişisel oturum notlarını `docs/memory/` altında tut; bu dizin public Git içeriğine dahil edilmez.

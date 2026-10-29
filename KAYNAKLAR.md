# Kaynaklar ve kapsam

Kontrol tarihi: 21 Ekim 2026. Yeni altı madde (1.8, 2.7, 5.6, 8.6, 8.7, 14.7) ve ekler 29 Ekim 2026'da ayrıca kontrol edildi. Bu liste bağımsız bir rehberdir; Anthropic tarafından hazırlanmış veya onaylanmış bir ürün belgesi değildir.

Teknik davranışlar ilgili resmî belgeyle ilişkilidir. Kaynak bağlantısı ürün davranışını destekler; madde içindeki proje tercihini veya performans önerisini ölçülmüş sonuç yapmaz. Bağlantısız maddeler editoryal iş akışı önerisidir.

Yerel Claude Code 2.1.284 için sürüm ve yardım çıktısı kontrol edildi. Güncel belgeler daha yeni sürümleri de kapsıyor. Özellikle hook `onFailure` ayarı 2.1.295+ gerektirir; yerel sürümde çalıştığı iddia edilmiyor.

| Kaynak | İlgili maddeler |
|---|---|
| [Talimat ve bellek](https://code.claude.com/docs/en/memory) | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 10.2, 18.1, 18.2, 18.3, 18.4, 19.3 |
| [İyi uygulamalar](https://code.claude.com/docs/en/best-practices) | 2.1 |
| [Durum satırı](https://code.claude.com/docs/en/statusline) | 2.2, 8.3 |
| [Komutlar](https://code.claude.com/docs/en/commands) | 2.3, 2.6, 3.3, 12.6 |
| [Alt ajanlar](https://code.claude.com/docs/en/sub-agents) | 2.4, 5.1, 9.1, 11.6 |
| [Headless kullanım](https://code.claude.com/docs/en/headless) | 2.5, 5.6, 14.2, 14.6, 14.7 |
| [Hedefler](https://code.claude.com/docs/en/goal) | 3.1 |
| [Model ve effort](https://code.claude.com/docs/en/model-config) | 5.2, 5.3, 5.6 |
| [Kullanım ve maliyet](https://code.claude.com/docs/en/costs) | 5.4, 19.1, 19.5 |
| [Advisor](https://code.claude.com/docs/en/advisor) | 5.5 |
| [İzinler](https://code.claude.com/docs/en/permissions) | 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 7.1, 15.3 |
| [Güvenlik](https://code.claude.com/docs/en/security) | 7.2, 7.3, 7.4 |
| [Sandbox](https://code.claude.com/docs/en/sandboxing) | 7.5 |
| [Hook referansı](https://code.claude.com/docs/en/hooks) | 7.6, 8.1, 8.2, 8.4, 8.5, 8.6, 8.7, 19.4 |
| [Ayarlar](https://code.claude.com/docs/en/settings) | 1.8, 7.7, 10.1 |
| [Skills](https://code.claude.com/docs/en/skills) | 9.2, 9.3, 9.4, 9.8, 10.3 |
| [Plugins](https://code.claude.com/docs/en/plugins) | 9.6 |
| [MCP](https://code.claude.com/docs/en/mcp) | 9.5, 9.7 |
| [İş akışları](https://code.claude.com/docs/en/common-workflows) | 11.1 |
| [Git worktree](https://git-scm.com/docs/git-worktree) | 11.2, 15.1, 19.2 |
| [Masaüstü](https://code.claude.com/docs/en/desktop) | 13.4 |
| [Bulut zamanlama](https://code.claude.com/docs/en/routines) | 14.1 |
| [Oturum içi zamanlama](https://code.claude.com/docs/en/scheduled-tasks) | 14.5 |
| [Checkpoint](https://code.claude.com/docs/en/checkpointing) | 2.7, 15.2 |
| [Ayar referansı](https://code.claude.com/docs/en/settings-reference) | 15.4 |
| [Genel bakış](https://code.claude.com/docs/en/overview) | 19.6 |
| [Oturumlar](https://code.claude.com/docs/en/sessions) | 2.7 |

26 kaynağın erişimi ve içerik özeti [kaynak kaydında](dogrulama/kaynaklar.json) tutulur. Sayfaların tam metni depoya kopyalanmaz. Erişim kontrolü, listelenen özelliğin canlı kullanım testi değildir.

## Ekler

Komutlar ve sorun giderme ekleri [komutlar](https://code.claude.com/docs/en/commands), [CLI referansı](https://code.claude.com/docs/en/cli-reference), [etkileşimli mod](https://code.claude.com/docs/en/interactive-mode) ve [sorun giderme](https://code.claude.com/docs/en/troubleshooting) sayfalarına dayanır. Belgeler yerel CLI 2.1.284'ten yeni: bazı komutlar o sürümde görünmeyebilir, `--max-turns` yerel `--help` çıktısında listelenmedi. Belgede bulunmayan iki iddia eklere yazılmadı: aynı olaydaki hook'lar için sıra garantisi ve `#` ile belleğe yazma kısayolu. Dosya konumları ve ipuçları ekleri [ayarlar](https://code.claude.com/docs/en/settings), [ayar referansı](https://code.claude.com/docs/en/settings-reference), [.claude dizini](https://code.claude.com/docs/en/claude-directory), [bellek](https://code.claude.com/docs/en/memory), [MCP](https://code.claude.com/docs/en/mcp), [hook'lar](https://code.claude.com/docs/en/hooks), [alt ajanlar](https://code.claude.com/docs/en/sub-agents) ve [iyi uygulamalar](https://code.claude.com/docs/en/best-practices) sayfalarına dayanır. "Talimatları buda, eksik kalanı geri ekle" döngüsü belgede yok, iş akışı önerisi olarak işaretlendi. `/doctor prompt-audit` için sürüm şartı 2.1.283 alındı, belgenin başka bir tablosu aynı ad için 2.1.221 yazıyor. Deneyimler eki yazarın tarihli ölçüm defterinden anonimleştirildi. Her vaka tek makinede yapılmış bir gözlemdir.

## Eski ölçümler

Önceki sürümdeki kişisel oturum sayıları ve bunlardan türetilen getiri sıralaması, bu denetimde ham kayıtlarla tekrar doğrulanamadı. Bu nedenle güncel sayfa ve PDF’de kanıt olarak kullanılmıyor. Eski sürüm Git geçmişinde korunur.

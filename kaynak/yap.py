"""veri.py’den web, baskı HTML’i ve README üretir. Kullanım: python3 kaynak/yap.py"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import BOLUMLER, ILK10, SAYILAR, SURUM, KAYNAKLAR
from ekler import EKLER, EK_TARIH
from rehber import REHBER, REHBER_TARIH, REHBER_GIRIS, SEVIYELER

esc = html.escape
N = sum(len(m) for *_, m in BOLUMLER)
NT = sum(1 for *_, m in BOLUMLER for x in m if x["s"] == "temel")
idx = {k: i for i, (k, *_) in enumerate(BOLUMLER, 1)}
SEV = {"temel": "Temel", "ileri": "İleri"}
BASLIK = "Claude Code'u iyi kullanmanın kontrol listesi"
OKUMA = [
 "Bu liste tekrar işi azaltmak, kapsamı belirlemek ve sonucu kanıtla teslim almak için hazırlanmış bir çalışma rehberidir. Her madde her projeye uygun değildir; kullanımına uygun olanları seç.",
 "<b>Neden</b> gerekçeyi, <b>nasıl</b> uygulama yolunu, <b>doğrula</b> beklenen kanıtı gösterir. Başlangıç onlusu ve temel/ileri etiketleri editoryal öneridir; ölçülmüş getiri sıralaması değildir.",
 f"<b>Temel</b> {NT}, <b>ileri</b> {N-NT} madde vardır. Teknik davranışların yanında resmî kaynak bağlantısı bulunur; bağlantısız maddeler iş akışı önerisidir. Örnekler kendi projenin araçlarına ve yetkisine uyarlanmalıdır.",
 "Kaynaklar 21 Ekim 2026'da kontrol edildi, yeni altı madde ve ekler 29 Ekim 2026'da. Yerel CLI 2.1.284 için yalnız sürüm ve yardım çıktısı alındı; listelenen bütün Claude özellikleri canlı çalıştırılmadı. CLI, Desktop, bulut ve sağlayıcı farklarını ilgili belgede kontrol et.",
 "Bir kutuyu işaretlemek kişisel ilerleme kaydıdır; otomatik doğrulama veya güvenlik garantisi değildir. Tarayıcı verisi temizlenebilir; ilerlemeni JSON olarak dışa aktarabilirsin.",
]
SAYI_GIRIS = "Eski sürümün kişisel kullanım sayıları bu denetimde ham kayıtlarla yeniden doğrulanmadığından sıralama kanıtı olarak kullanılmıyor."

def kaynak_html(m):
    if not m['r']:
        return 'İş akışı önerisi'
    return 'Belge: ' + ' · '.join(f'<a href="{KAYNAKLAR[k]["url"]}">{KAYNAKLAR[k]["ad"]}</a>' for k in m['r'])

def validate(bolumler=BOLUMLER):
    seen=set()
    for k, _, _, maddeler in bolumler:
        if k in seen: raise ValueError('Tekrarlanan bölüm kimliği: '+k)
        seen.add(k)
        for m in maddeler:
            if any(not isinstance(m.get(f),str) or not m[f].strip() for f in ['e','n','y','d']):
                raise ValueError('Eksik madde alanı')
            if m['s'] not in SEV: raise ValueError('Bilinmeyen seviye')
            if any(r not in KAYNAKLAR for r in m['r']): raise ValueError('Bilinmeyen kaynak')
    for k,j,_ in ILK10:
        match=next((x for x in bolumler if x[0]==k),None)
        if not match or not 1<=j<=len(match[3]): raise ValueError('Geçersiz başlangıç bağlantısı')
    validate_ekler(EKLER, bolumler)
    if bolumler is BOLUMLER: validate_rehber()

# ---------- EKLER ----------
# Ek metinleri Markdown alt kümesiyle yazılır: ##/###, paragraf, "- " liste, | tablo |, ``` kod.
# [[3.1]] maddeye bağlantı olur; numara bölüm ve madde sırasından çözülür.
REF = re.compile(r"\[\[(\d+)\.(\d+)\]\]")

def validate_ekler(ekler, bolumler=BOLUMLER):
    seen = set()
    for ek in ekler:
        if ek["ad"] in seen: raise ValueError("Tekrarlanan ek: " + ek["ad"])
        seen.add(ek["ad"])
        for i, j in REF.findall(ek["md"]):
            i, j = int(i), int(j)
            if not (1 <= i <= len(bolumler) and 1 <= j <= len(bolumler[i-1][3])):
                raise ValueError(f"Geçersiz madde bağlantısı: {i}.{j} ({ek['ad']})")

def ref_md(md):
    return REF.sub(lambda m: f"[{m[1]}.{m[2]}](../README.md#{m[1]}-{BOLUMLER[int(m[1])-1][0]})", md)

def ref_html(md, onek="../index.html"):
    return REF.sub(lambda m: f"[{m[1]}.{m[2]}]({onek}#m-{BOLUMLER[int(m[1])-1][0]}-{m[2]}-k)", md)

def satir_ici(t):
    t = esc(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)

def baslik_id(t):
    t = t.lower().translate(str.maketrans("çğıöşüâî", "cgiosuai"))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def md_html(md, onek_id=""):
    o, par, liste, tablo, kod = [], [], [], [], None
    def bosalt():
        if par: o.append("<p>" + satir_ici(" ".join(par)) + "</p>"); par.clear()
        if liste: o.append("<ul>" + "".join(f"<li>{satir_ici(x)}</li>" for x in liste) + "</ul>"); liste.clear()
        if tablo:
            hucre = lambda s: [c.strip() for c in s.strip().strip("|").split("|")]
            bas, *govde = [r for r in tablo if not re.fullmatch(r"\|[\s:|-]+\|", r.strip())]
            o.append('<div class="tablo"><table><thead><tr>' + "".join(f"<th>{satir_ici(c)}</th>" for c in hucre(bas)) + "</tr></thead><tbody>"
                     + "".join("<tr>" + "".join(f'<td data-e="{esc(re.sub(r"[`*]", "", h))}">{satir_ici(c)}</td>' for h, c in zip(hucre(bas), hucre(r))) + "</tr>" for r in govde) + "</tbody></table></div>")
            tablo.clear()
    for l in md.strip("\n").split("\n"):
        if kod is not None:
            if l.startswith("```"): o.append(f"<pre>{esc(chr(10).join(kod))}</pre>"); kod = None
            else: kod.append(l)
        elif l.startswith("```"): bosalt(); kod = []
        elif l.startswith("#"):
            bosalt(); n = len(l) - len(l.lstrip("#")); t = l[n:].strip()
            o.append(f'<h{n} id="{onek_id}{baslik_id(t)}">{satir_ici(t)}</h{n}>')
        elif l.startswith("|"):
            if par or liste: bosalt()
            tablo.append(l)
        elif l.startswith("- "):
            if par or tablo: bosalt()
            liste.append(l[2:])
        elif not l.strip(): bosalt()
        else: par.append(l.strip())
    bosalt()
    return "\n".join(o)


def ilk10_satirlari():
    for k, j, kisa in ILK10:
        i = idx[k]; m = BOLUMLER[i-1][3][j-1]
        yield i, j, kisa, m

# ---------- PDF ----------
PCSS = """
@page{size:A4;margin:16mm 16mm 18mm 16mm}
:root{--ink:#18202b;--soft:#5a6270;--line:#e2e5ea;--acc:#1d4f91;--accbg:#e8eff9;--ile:#6a4a9c;--ilebg:#f1ebf8;--kod:#f4f6f9}
body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:var(--ink);font-size:9.6pt;line-height:1.42;margin:0;background:#fff}
code{font-family:Menlo,monospace;font-size:8.2pt;background:var(--kod);padding:0 .8mm;border-radius:1mm}
pre{font-family:Menlo,monospace;font-size:7.8pt;line-height:1.38;background:var(--kod);border-left:2px solid #c9d3e2;padding:2mm 3mm;margin:1.2mm 0 0;white-space:pre-wrap;break-inside:avoid}
.kapak{height:255mm;display:flex;flex-direction:column;justify-content:space-between;break-after:page}
.kapak h1{font-size:30pt;line-height:1.08;margin:28mm 0 5mm;letter-spacing:-.6px;max-width:160mm}
.kapak .alt{font-size:12pt;color:var(--soft);max-width:150mm}
.kapak .kutu{border-top:2px solid var(--ink);padding-top:4mm;font-size:9.5pt;color:var(--soft)}
h2{font-size:15pt;margin:0 0 2mm;letter-spacing:-.2px}
.no{color:var(--acc);font-weight:700;margin-right:2mm}
.giris{color:var(--soft);margin:0 0 3.5mm;max-width:168mm}
.okuma p{margin:0 0 2.4mm;max-width:168mm}
.sayilar{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:3mm}
.sayilar div{border:1px solid var(--line);border-radius:2.5mm;padding:3mm 3.5mm}
.sayilar b{display:block;font-size:12.5pt;margin-bottom:.8mm}.sayilar span{color:var(--soft);font-size:9pt}
.ilk10{break-before:page}
.ilk10 ol{margin:3mm 0 0;padding:0;list-style:none;counter-reset:s}
.ilk10 li{counter-increment:s;display:grid;grid-template-columns:11mm 1fr;padding:2.6mm 0;border-top:1px solid var(--line)}
.ilk10 li::before{content:counter(s);font-size:16pt;font-weight:700;color:var(--acc);line-height:1}
.ilk10 .k{font-weight:700;font-size:10.5pt}.ilk10 .r{color:var(--soft);font-size:8.6pt;margin-left:1.5mm}
.ilk10 .n{color:var(--soft);margin-top:.6mm}
.bolum{margin-top:9mm}.bolum.ilk{break-before:page;margin-top:0}
.grup{break-inside:avoid}
.madde{border-top:1px solid var(--line);padding:2.6mm 0 2.4mm;break-inside:avoid;display:grid;grid-template-columns:6mm 1fr;gap:0 2.5mm}
.kutucuk{width:3.6mm;height:3.6mm;border:1.3px solid #8a909a;border-radius:.8mm;margin-top:.7mm}
.bas{font-weight:700;font-size:10.2pt}
.satir{display:grid;grid-template-columns:20mm 1fr;margin-top:.8mm}
.satir>span:first-child{color:var(--soft);font-size:8.4pt;text-transform:uppercase;letter-spacing:.3px;padding-top:.3mm}
.et{display:inline-block;font-size:7.3pt;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:.3mm 1.6mm;border-radius:1mm;margin-left:1.5mm;vertical-align:1px}
.temel{color:var(--acc);background:var(--accbg)}.ileri{color:var(--ile);background:var(--ilebg)}
table{border-collapse:collapse;width:100%;margin-top:3mm;font-size:9.4pt}
th,td{text-align:left;padding:1.6mm 2mm;border-bottom:1px solid var(--line)}
th{font-size:8.2pt;color:var(--soft);text-transform:uppercase;letter-spacing:.3px}
td.n{text-align:right;font-variant-numeric:tabular-nums}
.bos{width:9mm;height:4.5mm;border:1px solid #b5b9c0;border-radius:.8mm;display:inline-block}
"""

def madde_pdf(i, j, m):
    ornek = f'<pre>{esc(m["o"])}</pre>' if m["o"] else ""
    return (f'<div class="madde"><div class="kutucuk"></div><div><div class="bas">{i}.{j} {m["e"]}<span class="et {m["s"]}">{SEV[m["s"]]}</span></div>'
            f'<div class="satir"><span>Neden</span><span>{m["n"]}</span></div>'
            f'<div class="satir"><span>Nasıl</span><span>{m["y"]}{ornek}</span></div>'
            f'<div class="satir"><span>Doğrula</span><span>{m["d"]}</span></div><div class="kaynak">{kaynak_html(m)}</div></div></div>')

def pdf():
    o = [f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Claude Code kontrol listesi</title><style>{PCSS}</style></head><body>']
    o.append(f'<section class="kapak"><div><h1>{BASLIK}</h1><p class="alt">{len(BOLUMLER)} bölüm, {N} madde. Başlangıç için on madde, her maddede neden, nasıl, kopyalanabilir örnek ve doğrulama.</p></div>'
             f'<div class="kutu">{SURUM}<br>Claude Code belgelerine dayanan teknik notlar ve editoryal iş akışı önerileri.</div></section>')
    o.append('<section class="okuma"><h2>Nasıl okunur</h2>' + "".join(f"<p>{p}</p>" for p in OKUMA))
    o.append('</section>')
    o.append('<section class="ilk10"><h2>Önce bu on madde</h2><p class="giris">Bütün listeyi okumaya vaktin yoksa buradan başla. Bunlar başlangıç önerileri; işine uymayanı atlayabilirsin.</p><ol>')
    for i, j, kisa, m in ilk10_satirlari():
        o.append(f'<li><div><span class="k">{kisa}</span><span class="r">madde {i}.{j}</span><div class="n">{m["n"]}</div></div></li>')
    o.append("</ol></section>")
    for i, (k, b, giris, mad) in enumerate(BOLUMLER, 1):
        o.append(f'<section class="bolum{" ilk" if i == 1 else ""}"><div class="grup"><h2><span class="no">{i}</span>{b}</h2><p class="giris">{giris}</p>')
        for j, m in enumerate(mad, 1):
            o.append(("</div>" if j == 2 else "") + madde_pdf(i, j, m))
        if len(mad) == 1: o.append("</div>")
        o.append("</section>")
    for b in REHBER:
        o.append(f'<section class="bolum ilk ek"><h2>Rehber {b["no"]} · {b["baslik"]}</h2><p class="giris">{SEVIYELER[b["seviye"]]} · {esc(b["ozet"])}</p>'
                 + md_html(ref_html(re.sub(r"\]\((\d\d-)", "](" + SAYFA + r"rehber/\1", ic_bag(b["md"], "html").replace('](../ekler/', '](' + SAYFA + 'ekler/')), SAYFA), b["ad"] + "-") + "</section>")
    for e in EKLER:
        o.append(f'<section class="bolum ilk ek"><h2>Ek · {e["baslik"]}</h2><p class="giris">{e["ozet"]} Belge kontrolü: {EK_TARIH}.</p>'
                 + md_html(ref_html(e["md"], SAYFA), e["ad"] + "-") + "</section>")
    o.append('<section class="bolum ilk"><h2>Kendi puan kartın</h2><p class="giris">Her bölüm için kaç maddenin yapıldığını, kaçının sırada olduğunu yaz. Üç ay sonra yeniden doldur.</p><table><tr><th>#</th><th>Bölüm</th><th>Madde</th><th>Yapıldı</th><th>Sırada</th><th>Gerek yok</th></tr>')
    for i, (k, b, _, mad) in enumerate(BOLUMLER, 1):
        o.append(f'<tr><td>{i}</td><td>{b}</td><td class="n">{len(mad)}</td><td><span class="bos"></span></td><td><span class="bos"></span></td><td><span class="bos"></span></td></tr>')
    o.append(f'<tr><td></td><td><b>Toplam</b></td><td class="n"><b>{N}</b></td><td></td><td></td><td></td></tr></table>'
             f'<p class="giris" style="margin-top:8mm">{SURUM}. Özellikler hızlı değişiyor; bir komut ya da ayar adı çalışmıyorsa code.claude.com/docs adresindeki güncel belgeye bak.</p></section></body></html>')
    return "\n".join(o)

# ---------- WEB ----------
WCSS = """
/* Düzen: tek sütun okuma alanı, üstte yapışkan ilerleme ve süzgeç çubuğu, geniş ekranda solda bölüm dizini */
:root{
 --bg:#f6f7f9;--yuzey:#ffffff;--fg:#17202c;--soft:#5b6472;--line:#e1e5eb;--kod:#eef1f5;
 --acc:#1d4f91;--accbg:#e6eef9;--ile:#6a4a9c;--ilebg:#f0eaf8;--ok:#1f7a4d;
 --f-baslik:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;
 --f-govde:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif;
 --f-kod:"IBM Plex Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11161d;--yuzey:#171e27;--fg:#e6eaf0;--soft:#9aa4b2;--line:#273140;--kod:#1d2631;--acc:#8fb4ec;--accbg:#1c2a40;--ile:#c3a8ec;--ilebg:#2a2238;--ok:#6fcf9b;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11161d;--yuzey:#171e27;--fg:#e6eaf0;--soft:#9aa4b2;--line:#273140;--kod:#1d2631;--acc:#8fb4ec;--accbg:#1c2a40;--ile:#c3a8ec;--ilebg:#2a2238;--ok:#6fcf9b;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--f-govde);font-size:15px;line-height:1.55;margin:0}
.sar{max-width:1120px;margin:0 auto;padding-inline:16px;padding-block:28px 64px;display:grid;grid-template-columns:1fr;gap:32px}
@media (min-width:980px){.sar{grid-template-columns:230px minmax(0,1fr)}}
nav.dizin{display:none}
@media (min-width:980px){nav.dizin{display:block;position:sticky;top:calc(env(safe-area-inset-top,0px) + 96px);align-self:start;max-height:calc(100vh - 120px);overflow:auto;font-size:13px}}
nav.dizin a{display:flex;justify-content:space-between;gap:8px;color:var(--soft);text-decoration:none;padding:4px 8px;border-radius:6px}
nav.dizin a:hover,nav.dizin a:focus-visible{background:var(--accbg);color:var(--fg);outline:none}
nav.dizin small{font-variant-numeric:tabular-nums}
main{min-width:0}
header.ust h1{font-family:var(--f-baslik);font-size:clamp(28px,5vw,44px);line-height:1.08;letter-spacing:-.02em;margin:0 0 10px;text-wrap:balance}
header.ust p{color:var(--soft);max-width:65ch;margin:0 0 6px}
.surum{font-family:var(--f-kod);font-size:12px;color:var(--soft)}
.cubuk{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 0;margin:20px 0 8px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}
.ilerleme{flex:1 1 220px;min-width:0}
.ilerleme .etiket{font-size:13px;color:var(--soft);font-variant-numeric:tabular-nums}
.ilerleme .yol{height:6px;background:var(--line);border-radius:3px;margin-top:5px;overflow:hidden}
.ilerleme .dolu{height:100%;width:0;background:var(--ok);transition:width .25s}
.suzgec{display:flex;flex-wrap:wrap;gap:6px}
.suzgec button{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--yuzey);color:var(--fg);padding:5px 11px;border-radius:999px;cursor:pointer}
.suzgec button[aria-pressed="true"]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.suzgec button:focus-visible,.kopya:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
h2{font-family:var(--f-baslik);font-size:24px;letter-spacing:-.01em;margin:44px 0 6px;text-wrap:balance;scroll-margin-top:90px}
h2 .no{color:var(--acc);margin-right:10px;font-variant-numeric:tabular-nums}
.giris{color:var(--soft);max-width:68ch;margin:0 0 10px}
details.okuma{background:var(--yuzey);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin-top:8px}
details.okuma summary{cursor:pointer;font-weight:600}
details.okuma p{max-width:68ch}
.sayilar{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:10px}
.sayilar div{border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:var(--bg)}
.sayilar b{display:block;font-family:var(--f-baslik);font-size:18px}
.sayilar span{color:var(--soft);font-size:13px}
.ilk10{list-style:none;padding:0;margin:8px 0 0;counter-reset:s;display:grid;gap:8px}
.ilk10 li{counter-increment:s;display:grid;grid-template-columns:40px minmax(0,1fr);gap:4px;background:var(--yuzey);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.ilk10 li::before{content:counter(s);font-family:var(--f-baslik);font-size:24px;font-weight:700;color:var(--acc);line-height:1}
.ilk10 a{color:var(--fg);font-weight:600;text-decoration:none}.ilk10 a:hover{text-decoration:underline}
.ilk10 .n{color:var(--soft);font-size:14px}
.madde{display:grid;grid-template-columns:28px minmax(0,1fr);gap:4px 10px;padding:16px 0;border-top:1px solid var(--line)}
.madde[hidden]{display:none}
.madde input{width:20px;height:20px;margin:3px 0 0;accent-color:var(--ok);cursor:pointer}
.madde.yapildi .bas{color:var(--soft);text-decoration:line-through;text-decoration-color:var(--line)}
.bas{font-weight:600;font-size:16px;cursor:pointer}
.no2{font-variant-numeric:tabular-nums;color:var(--soft);font-weight:500;margin-right:6px}
.et{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:1px 7px;border-radius:4px;margin-left:8px;vertical-align:2px}
.temel{color:var(--acc);background:var(--accbg)}.ileri{color:var(--ile);background:var(--ilebg)}
dl{display:grid;grid-template-columns:76px minmax(0,1fr);gap:4px 10px;margin:8px 0 0;font-size:14.5px}
dt{color:var(--soft);font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;padding-top:3px}
dd{margin:0;min-width:0}
code{font-family:var(--f-kod);font-size:.88em;background:var(--kod);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
.ornek{position:relative;margin-top:8px}
.ornek pre{font-family:var(--f-kod);font-size:13px;line-height:1.5;background:var(--kod);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:0;overflow-x:auto;white-space:pre}
.kopya{position:absolute;top:6px;right:6px;font:inherit;font-size:12px;background:var(--yuzey);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:2px 9px;cursor:pointer}
.bos-durum{color:var(--soft);padding:12px 0}
footer{color:var(--soft);font-size:13px;margin-top:48px;border-top:1px solid var(--line);padding-top:14px}
@media (prefers-reduced-motion:reduce){.ilerleme .dolu{transition:none}}
"""

WCSS += """
a{color:var(--acc)}
.madde,section.bolum{scroll-margin-top:var(--kaydirma,170px)}
.kaynak{font-size:12px;color:var(--soft);margin:8px 0 0}
.araclar{margin:14px 0}.araclar label{font-weight:600;font-size:13px;display:block}
#ara{width:100%;font:inherit;color:var(--fg);background:var(--yuzey);border:1px solid var(--line);border-radius:8px;padding:10px;margin:5px 0}
.islemler{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px}
.islemler button,.islemler a{font:inherit;font-size:12px;padding:7px 9px;background:var(--yuzey);color:var(--fg);border:1px solid var(--line);border-radius:6px;cursor:pointer;text-decoration:none}
button:focus-visible,input:focus-visible,a:focus-visible{outline:2px solid var(--acc);outline-offset:3px}
#arama-sonuc,#bildirim{font-size:13px;color:var(--soft)}
.ornek pre{padding-top:40px;white-space:pre-wrap;overflow-wrap:anywhere}
[hidden]{display:none!important}
@media(max-width:480px){dl{grid-template-columns:1fr;gap:3px}dt{margin-top:7px}.sar{padding-inline:12px}.madde{gap:4px 6px}.cubuk{position:static}.et{margin-left:4px}nav.dizin{position:static}}
@media print{.cubuk,.araclar,.dizin,.kopya,.ilk10,details.okuma{display:none!important}.sar{display:block;padding:0}body{background:white;color:#17202c}.madde{break-inside:avoid}.ornek pre{padding:10px}a{color:#1d4f91}}
"""
PCSS += """
a{color:#1d4f91;text-decoration:none}.kaynak{font-size:7.5pt;color:#5a6270;margin-top:1mm}
pre{overflow-wrap:anywhere}
.ek h2{margin-top:5mm}.ek h3{font-size:10.5pt;margin:4mm 0 1mm}.ek p{margin:0 0 2mm;max-width:172mm}
.ek table{font-size:8.6pt;margin:1mm 0 4mm}.ek td,.ek th{vertical-align:top}.ek tr{break-inside:avoid}.ek ul{margin:0 0 2mm;padding-left:5mm}
"""
SAYFA = "https://ratipcan-uysal.github.io/claude-code-kontrol-listesi/"

WJS = open(os.path.join(os.path.dirname(__file__), 'app.js'), encoding='utf-8').read()

ECSS = """
main.ek{max-width:900px;margin:0 auto;padding:28px 16px 64px}
.ek .ust-bag{font-size:14px;display:flex;flex-wrap:wrap;gap:6px 14px;margin-bottom:18px}
.ek h1{font-family:var(--f-baslik);font-size:clamp(28px,5vw,40px);line-height:1.1;letter-spacing:-.02em;margin:0 0 8px;text-wrap:balance}
.ek h2{scroll-margin-top:16px}.ek h3{font-size:17px;margin:26px 0 4px}
.ek p,.ek li{max-width:72ch}
.ek pre{font-family:var(--f-kod);font-size:13px;line-height:1.5;background:var(--kod);border:1px solid var(--line);border-radius:8px;padding:12px 14px;white-space:pre-wrap;overflow-wrap:anywhere}
.tablo{overflow-x:auto;margin:10px 0 18px;border:1px solid var(--line);border-radius:8px}
.tablo table{border-collapse:collapse;width:100%;font-size:14px;background:var(--yuzey)}
.tablo th,.tablo td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
.tablo th{font-size:12px;color:var(--soft);text-transform:uppercase;letter-spacing:.04em}
.tablo td:first-child code{overflow-wrap:normal;white-space:nowrap}
@media(max-width:600px){.tablo{border:0;overflow:visible}.tablo table{background:none}.tablo thead{display:none}.tablo tr{display:block;background:var(--yuzey);border:1px solid var(--line);border-radius:8px;margin-bottom:8px;padding:4px 0}.tablo td{display:block;border:0;padding:4px 12px}.tablo td::before{content:attr(data-e);display:block;font-size:11px;color:var(--soft);text-transform:uppercase;letter-spacing:.04em}.tablo td code,.tablo td:first-child code{white-space:normal;overflow-wrap:anywhere}}
ul.ekler{display:grid;gap:8px;padding:0;list-style:none;margin:8px 0 0}
ul.ekler li{background:var(--yuzey);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
ul.ekler a{font-weight:600}
ul.ekler span{display:block;color:var(--soft);font-size:14px}
"""

def sayfa(baslik, ozet, nav, govde, footer):
    return ('<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="{esc(ozet)}">\n<title>{baslik} · Claude Code kontrol listesi</title>\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">\n'
            f'<style>{WCSS}{ECSS}</style>\n<script>try{{var t=localStorage.getItem("cc-kontrol-tema");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>\n</head>\n<body>\n<main class="ek">'
            f'<nav class="ust-bag" aria-label="Gezinme">{nav}</nav>{govde}\n<footer>{footer}</footer></main>\n</body>\n</html>\n')

def ek_html(ek):
    bag = "".join(f'<a href="{e["ad"]}.html">{e["baslik"]}</a>' for e in EKLER if e is not ek)
    return sayfa(ek["baslik"], ek["ozet"], f'<a href="../index.html">← Kontrol listesi</a><a href="../rehber/index.html">Rehber</a>{bag}',
                 f'<h1>{ek["baslik"]}</h1><p class="surum">Belge kontrolü: {EK_TARIH}</p>\n{md_html(ref_html(ek["md"]))}',
                 f'<a href="../index.html#ekler">Bütün ekler</a> · <a href="https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/blob/main/ekler/{ek["ad"]}.md">Markdown sürümü</a>')

def ek_md(ek):
    diger = " · ".join(f'[{e["baslik"]}]({e["ad"]}.md)' for e in EKLER if e is not ek)
    return f'# {ek["baslik"]}\n\n_Belge kontrolü: {EK_TARIH}_\n\n{ref_md(ek["md"]).strip()}\n\n---\n\n[Kontrol listesi](../README.md) · [Rehber](../rehber/README.md) · {diger}\n'

# ---------- REHBER ----------
# Bölüm metninde {{ek:komutlar}} eke, {{bolum:5}} başka bölüme bağlanır.
IC = re.compile(r"\{\{(ek|bolum):([a-z0-9-]+)\}\}")

def validate_rehber(rehber=REHBER):
    nolar = {str(b["no"]) for b in rehber}
    for b in rehber:
        if re.search(r"[Bb]ölüm \{\{bolum:", b["md"]):
            raise ValueError(f"Bölüm bağlantısı zaten 'Bölüm n' yazar, önüne 'bölüm' ekleme ({b['ad']})")
        for tur, ad in IC.findall(b["md"]):
            if (tur == "ek" and ad not in {e["ad"] for e in EKLER}) or (tur == "bolum" and ad not in nolar):
                raise ValueError(f"Geçersiz rehber bağlantısı: {tur}:{ad} ({b['ad']})")
    validate_ekler(rehber)

def ic_bag(md, uzanti):
    def bag(m):
        if m[1] == "ek":
            e = next(e for e in EKLER if e["ad"] == m[2])
            return f"[{e['baslik']}](../ekler/{e['ad']}.{uzanti})"
        b = next(b for b in REHBER if str(b["no"]) == m[2])
        return f"[Bölüm {b['no']}: {b['baslik']}]({b['ad']}.{uzanti})"
    return IC.sub(bag, md)

def komsu(b):
    i = REHBER.index(b)
    return (REHBER[i-1] if i > 0 else None), (REHBER[i+1] if i < len(REHBER)-1 else None)

def bolum_html(b):
    once, sonra = komsu(b)
    alt = " · ".join(x for x in [
        f'<a href="{once["ad"]}.html">← Bölüm {once["no"]}: {once["baslik"]}</a>' if once else "",
        f'<a href="{sonra["ad"]}.html">Bölüm {sonra["no"]}: {sonra["baslik"]} →</a>' if sonra else "",
        f'<a href="https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/blob/main/rehber/{b["ad"]}.md">Markdown sürümü</a>'] if x)
    return sayfa(b["baslik"], b["ozet"], '<a href="../index.html">← Kontrol listesi</a><a href="index.html">Rehber içindekiler</a><a href="../index.html#ekler">Ekler</a>',
                 f'<p class="surum">{SEVIYELER[b["seviye"]]} · Bölüm {b["no"]}</p><h1>{b["baslik"]}</h1><p class="giris">{esc(b["ozet"])}</p><p class="surum">Belge kontrolü: {REHBER_TARIH}</p>\n'
                 + md_html(ref_html(ic_bag(b["md"], "html"))), alt)

def bolum_md(b):
    once, sonra = komsu(b)
    alt = " · ".join(x for x in [f'[← Bölüm {once["no"]}]({once["ad"]}.md)' if once else "", "[İçindekiler](README.md)",
                                 f'[Bölüm {sonra["no"]} →]({sonra["ad"]}.md)' if sonra else ""] if x)
    return (f'# {b["no"]}. {b["baslik"]}\n\n_{SEVIYELER[b["seviye"]]} · Belge kontrolü: {REHBER_TARIH}_\n\n{b["ozet"]}\n\n'
            f'{ref_md(ic_bag(b["md"], "md")).strip()}\n\n---\n\n{alt}\n')

def rehber_listesi():
    for s, ad in SEVIYELER.items():
        bs = [b for b in REHBER if b["seviye"] == s]
        if bs: yield ad, bs

def rehber_index():
    govde = f'<h1>Claude Code rehberi</h1><p class="surum">Belge kontrolü: {REHBER_TARIH}</p>\n' + md_html(ref_html(ic_bag(REHBER_GIRIS, "html")))
    for ad, bs in rehber_listesi():
        govde += f'<h2>{ad}</h2><ul class="ekler">' + "".join(f'<li><a href="{b["ad"]}.html">{b["no"]}. {b["baslik"]}</a><span>{esc(b["ozet"])}</span></li>' for b in bs) + "</ul>"
    return sayfa("Claude Code rehberi", "Claude Code'u uzman düzeyinde kullanmak için alıştırmalı rehber.",
                 '<a href="../index.html">← Kontrol listesi</a><a href="../index.html#ekler">Ekler</a>', govde,
                 '<a href="https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/blob/main/rehber/README.md">Markdown sürümü</a>')

def rehber_readme():
    o = [f"# Claude Code rehberi\n\n_Belge kontrolü: {REHBER_TARIH}_\n", ref_md(ic_bag(REHBER_GIRIS, "md")).strip(), ""]
    for ad, bs in rehber_listesi():
        o += [f"## {ad}", ""] + [f"- [{b['no']}. {b['baslik']}]({b['ad']}.md): {b['ozet']}" for b in bs] + [""]
    o += ["---", "", "[Kontrol listesi](../README.md)", ""]
    return "\n".join(o)

def madde_web(i, j, m):
    mid = f"m-{BOLUMLER[i-1][0]}-{j}"
    ornek = (f'<dt>Örnek</dt><dd><div class="ornek"><button type="button" class="kopya">Kopyala</button><pre>{esc(m["o"])}</pre></div></dd>' if m["o"] else "")
    return (f'<div class="madde" data-s="{m["s"]}" id="{mid}-k"><input type="checkbox" id="{mid}" aria-labelledby="{mid}-b">'
            f'<div><label class="bas" id="{mid}-b" for="{mid}"><span class="no2">{i}.{j}</span>{m["e"]}<span class="et {m["s"]}">{SEV[m["s"]]}</span></label>'
            f'<dl><dt>Neden</dt><dd>{m["n"]}</dd><dt>Nasıl</dt><dd>{m["y"]}</dd>{ornek}<dt>Doğrula</dt><dd>{m["d"]}</dd></dl><p class="kaynak">{kaynak_html(m)}</p></div></div>')

def web():
    o = ['<title>Claude Code kontrol listesi</title>',
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">',
         f'<style>{WCSS}{ECSS}</style>', '<div class="sar"><nav class="dizin" aria-label="Bölümler"><a href="#ilk10"><span>Önce bu on madde</span></a>']
    for i, (k, b, _, mad) in enumerate(BOLUMLER, 1):
        o.append(f'<a href="#b-{k}"><span>{i}. {b}</span><small>0/{len(mad)}</small></a>')
    o.append(f'<a href="rehber/index.html"><span>Rehber</span><small>{len(REHBER)}</small></a><a href="#ekler"><span>Ekler</span><small>{len(EKLER)}</small></a></nav><main>')
    o.append(f'<header class="ust"><h1>{BASLIK}</h1><p>{len(BOLUMLER)} bölüm, {N} madde. Her maddede neden, nasıl, kopyalanabilir örnek ve doğrulama. İşaretler bu tarayıcıda saklanır; JSON olarak yedekleyebilirsin.</p><div class="surum">{SURUM}</div></header>')
    o.append('<div class="cubuk"><div class="ilerleme"><div class="etiket" id="sayac" role="status" aria-live="polite">0 madde işaretlendi</div><div class="yol"><div class="dolu" id="dolu"></div></div></div>'
             '<div class="suzgec" role="group" aria-label="Süzgeç"><button type="button" data-suz="hepsi" aria-pressed="true">Tümü</button>'
             f'<button type="button" data-suz="temel" aria-pressed="false">Temel ({NT})</button><button type="button" data-suz="ileri" aria-pressed="false">İleri ({N-NT})</button>'
             '<button type="button" data-suz="acik" aria-pressed="false">Yapılmamış</button></div></div>')
    o.append('<div class="araclar"><label for="ara">Listede ara</label><input id="ara" type="search" placeholder="Örn. izin, MCP, bellek" autocomplete="off"><span id="arama-sonuc" role="status"></span>'
             '<div class="islemler"><button id="tema" type="button">Tema: sistem</button><button id="disa" type="button">İlerlemeyi dışa aktar</button><button id="ice" type="button">İçe aktar</button>'
             '<button id="sifirla" type="button">İşaretleri temizle</button><a href="claude-code-kontrol-listesi.pdf">PDF indir</a><a href="https://github.com/ratipcan-uysal/claude-code-kontrol-listesi">GitHub</a></div>'
             '<input type="file" id="dosya" accept="application/json,.json" hidden><p id="bildirim" role="status" aria-live="polite"></p></div>')
    o.append('<details class="okuma"><summary>Nasıl okunur ve kaynak kapsamı</summary>' + "".join(f"<p>{p}</p>" for p in OKUMA)
             + '</details>')
    o.append('<h2 id="ilk10">Önce bu on madde</h2><p class="giris">Bütün listeyi okumaya vaktin yoksa buradan başla. Bunlar başlangıç önerileri; işine uymayanı atlayabilirsin.</p><ol class="ilk10">')
    for i, j, kisa, m in ilk10_satirlari():
        o.append(f'<li><div><a href="#m-{BOLUMLER[i-1][0]}-{j}-k">{kisa}</a> <span class="no2">· {i}.{j}</span><div class="n">{m["n"]}</div></div></li>')
    o.append("</ol>")
    for i, (k, b, giris, mad) in enumerate(BOLUMLER, 1):
        o.append(f'<section class="bolum" id="b-{k}"><h2><span class="no">{i}</span>{b}</h2><p class="giris">{giris}</p>')
        o.extend(madde_web(i, j, m) for j, m in enumerate(mad, 1))
        o.append('<p class="bos-durum" hidden>Bu süzgeçte bu bölümde gösterilecek madde yok.</p></section>')
    o.append('<section id="rehber"><h2>Rehber</h2><p class="giris">Kontrol listesi neyin yapılacağını söyler. Rehber nedenini ve nasıl öğrenileceğini anlatır: üç seviye, her bölümde bir alıştırma.</p>'
             '<ul class="ekler"><li><a href="rehber/index.html">Claude Code rehberi</a><span>Zihinsel modeller, karar kuralları, gerçek vakalar ve alıştırmalar.</span></li></ul></section>')
    o.append('<section id="ekler"><h2>Ekler</h2><p class="giris">Maddeleri günlük işe taşıyan başvuru sayfaları. Her ek ilgili maddelere bağlanır.</p><ul class="ekler">'
             + "".join(f'<li><a href="ekler/{e["ad"]}.html">{e["baslik"]}</a><span>{e["ozet"]}</span></li>' for e in EKLER) + '</ul></section>')
    o.append(f'<footer>{SURUM}. <a href="https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/blob/main/KAYNAKLAR.md">Kaynaklar</a> · <a href="https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/blob/main/DOGRULAMA.md">Doğrulama kapsamı</a> · <a href="https://github.com/ratipcan-uysal/claude-code-kontrol-listesi/blob/main/GUNCELLEMELER.md">Değişiklikler</a></footer></main></div>')
    o.append(f"<script>{WJS}</script>")
    return "\n".join(o)

def metin(h):
    t = re.sub(r"(?s)<style.*?</style>|<script.*?</script>|<title>.*?</title>|<pre>.*?</pre>", "", h)
    t = re.sub(r"</(p|h1|h2|div|li|td|th|dd|dt|label)>", "\n\n", t); t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\n\s*\n+", "\n\n", html.unescape(t)).strip()

def md_satir(t):
    kodlar = []
    def sakla(m):
        kodlar.append("`" + html.unescape(m.group(1)) + "`")
        return f"\0{len(kodlar)-1}\0"
    t = re.sub(r"<code>(.*?)</code>", sakla, t)
    t = re.sub(r"</?b>", "**", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return re.sub(r"\0(\d+)\0", lambda m: kodlar[int(m.group(1))], t)

def readme():
    o = [f"# {BASLIK}", "", f"{len(BOLUMLER)} bölüm, {N} madde. Her maddede neden, nasıl, kopyalanabilir örnek ve doğrulama.", "",
         "- **Web sürümü** (işaretlenebilir, süzgeçli): https://ratipcan-uysal.github.io/claude-code-kontrol-listesi/",
         "- **PDF:** [claude-code-kontrol-listesi.pdf](claude-code-kontrol-listesi.pdf)", "", f"_{SURUM}_", "", "## Nasıl okunur", ""]
    o += [md_satir(p) + "\n" for p in OKUMA]
    o += ["## Önce bu on madde", ""]
    for n, (i, j, kisa, m) in enumerate(ilk10_satirlari(), 1):
        o.append(f"{n}. **{kisa}** ([{i}.{j}](#{i}-{BOLUMLER[i-1][0]})): {md_satir(m['n'])}")
    o += ["", "## Bölümler", ""]
    o += [f"{i}. [{b}](#{i}-{k}) ({len(m)})" for i, (k, b, _, m) in enumerate(BOLUMLER, 1)]
    o += ["", "## Rehber", "", "[Claude Code rehberi](rehber/README.md): zihinsel modeller, karar kuralları ve alıştırmalarla üç seviyeli öğrenme yolu."]
    o += ["", "## Ekler", ""] + [f"- [{e['baslik']}](ekler/{e['ad']}.md): {e['ozet']}" for e in EKLER]
    for i, (k, b, giris, mad) in enumerate(BOLUMLER, 1):
        o += ["", f'<a id="{i}-{k}"></a>', f"## {i}. {b}", "", md_satir(giris), ""]
        for j, m in enumerate(mad, 1):
            o.append(f"- [ ] **{i}.{j} {md_satir(m['e'])}** `{SEV[m['s']]}`")
            o.append(f"  - **Neden:** {md_satir(m['n'])}")
            o.append(f"  - **Nasıl:** {md_satir(m['y'])}")
            if m["o"]:
                o += ["", "    ```", *["    " + l for l in m["o"].split("\n")], "    ```", ""]
            o.append(f"  - **Doğrula:** {md_satir(m['d'])}")
            o.append('  - **Dayanak:** ' + (' · '.join(f"[{KAYNAKLAR[r]['ad']}]({KAYNAKLAR[r]['url']})" for r in m['r']) or 'İş akışı önerisi'))
    o += ["", "## Kaynak ve doğrulama", "", "[Kaynaklar](KAYNAKLAR.md) · [Doğrulama](DOGRULAMA.md) · [Değişiklikler](GUNCELLEMELER.md)", ""]
    o += ["", "## Güncelleme", "", "İçerik tek dosyada: `kaynak/veri.py`. Değiştirdikten sonra:", "", "```sh",
          "python3 kaynak/yap.py",
          "\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\" --headless=new --no-pdf-header-footer \\",
          "  --print-to-pdf=claude-code-kontrol-listesi.pdf \"file://$PWD/kaynak/pdf.html\"", "```", "",
          "## Lisans", "", "[CC BY 4.0](LICENSE): kaynak göstererek paylaşabilir ve uyarlayabilirsin.", ""]
    return "\n".join(o)

def bagimsiz(w):
    return ('<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="Claude Code için {N} maddelik kontrol listesi: neden, nasıl, örnek ve doğrulama.">\n'
            + w.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")

if __name__ == "__main__":
    validate()
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open(os.path.join(kok, "kaynak", "pdf.html"), "w", encoding="utf-8").write(pdf())
    open(os.path.join(kok, "index.html"), "w", encoding="utf-8").write(bagimsiz(web()))
    open(os.path.join(kok, "README.md"), "w", encoding="utf-8").write(readme())
    os.makedirs(os.path.join(kok, "ekler"), exist_ok=True)
    for e in EKLER:
        open(os.path.join(kok, "ekler", e["ad"] + ".html"), "w", encoding="utf-8").write(ek_html(e))
        open(os.path.join(kok, "ekler", e["ad"] + ".md"), "w", encoding="utf-8").write(ek_md(e))
    os.makedirs(os.path.join(kok, "rehber"), exist_ok=True)
    for b in REHBER:
        open(os.path.join(kok, "rehber", b["ad"] + ".html"), "w", encoding="utf-8").write(bolum_html(b))
        open(os.path.join(kok, "rehber", b["ad"] + ".md"), "w", encoding="utf-8").write(bolum_md(b))
    open(os.path.join(kok, "rehber", "index.html"), "w", encoding="utf-8").write(rehber_index())
    open(os.path.join(kok, "rehber", "README.md"), "w", encoding="utf-8").write(rehber_readme())
    print(len(BOLUMLER), "bölüm", N, "madde", NT, "temel")

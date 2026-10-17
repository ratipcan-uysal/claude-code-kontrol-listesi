"""veri.py'den iki çıktı üretir: baskı HTML'i (PDF için) ve web artifact HTML'i.
Kullanım: python3 v2_yap.py <pdf.html> <web.html> <metin.md>"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import BOLUMLER, ILK10, SAYILAR, SURUM

esc = html.escape
N = sum(len(m) for *_, m in BOLUMLER)
NT = sum(1 for *_, m in BOLUMLER for x in m if x["s"] == "temel")
idx = {k: i for i, (k, *_) in enumerate(BOLUMLER, 1)}
SEV = {"temel": "Temel", "ileri": "İleri"}
BASLIK = "Claude Code'u iyi kullanmanın kontrol listesi"
OKUMA = [
 "\"İyi kullanmak\" burada hız ya da çok özellik kullanmak demek değil. Ölçüt üç tane: aynı işi daha az mesajla bitirmek, aynı limitle daha çok iş çıkarmak ve sonucu kanıtla teslim almak. Bilgisayar başında değilken de ayakta kalan bir düzen bu üçünün toplamı.",
 "Her bölüm kısa bir gerekçeyle başlıyor, maddeler getirisi yüksekten düşüğe sıralı. <b>Neden</b> satırı önemini, <b>nasıl</b> satırı komutu ya da ayarı söyler. Örneği olan maddelerde kopyalanabilir bir parça var. <b>Doğrula</b> satırı işin gerçekten olduğunu neye bakarak anlayacağını gösterir. Doğrulanamayan madde yapılmış sayılmaz.",
 f"<b>Temel</b> etiketli {NT} madde her kullanıcı için, ilk haftada yapılabilir. <b>İleri</b> etiketli {N-NT} madde otomasyon, gözetimsiz koşum, ekip ve çok oturumla çalışanlar için.",
 "Belge Claude Code'u (CLI ve masaüstü uygulaması) kapsıyor. API ile uygulama geliştirme ve ücretli araç önerisi kapsam dışında. Özellik adları 16 Ekim 2026'da code.claude.com belgeleriyle doğrulandı. Bir komut ya da ayar çalışmıyorsa sürümünü <code>claude --version</code> ile kontrol et ve güncel belgeye bak.",
]
SAYI_GIRIS = "Listenin önceliklerini belirleyen veri: tek bir kullanıcının beş aylık oturum kayıtları. Senin dağılımın farklı olabilir. Bu sayılar sıralamanın gerekçesi, senin için hedef değil."

def ilk10_satirlari():
    for k, j, kisa in ILK10:
        i = idx[k]; m = dict(BOLUMLER)[k] if False else BOLUMLER[i-1][3][j-1]
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
            f'<div class="satir"><span>Doğrula</span><span>{m["d"]}</span></div></div></div>')

def pdf():
    o = [f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Claude Code kontrol listesi</title><style>{PCSS}</style></head><body>']
    o.append(f'<section class="kapak"><div><h1>{BASLIK}</h1><p class="alt">{len(BOLUMLER)} bölüm, {N} madde. İlk sayfada en önemli on madde, her maddede neden, nasıl, kopyalanabilir örnek ve doğrulama.</p></div>'
             f'<div class="kutu">{SURUM}<br>Beş aylık gerçek kullanım verisinden ve Claude Code belgelerinden (code.claude.com) derlendi.</div></section>')
    o.append('<section class="okuma"><h2>Nasıl okunur</h2>' + "".join(f"<p>{p}</p>" for p in OKUMA))
    o.append(f'<h2 style="margin-top:6mm">Gerçek bir kullanımdan sayılar</h2><p class="giris">{SAYI_GIRIS}</p><div class="sayilar">'
             + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in SAYILAR) + "</div></section>")
    o.append('<section class="ilk10"><h2>Önce bu on madde</h2><p class="giris">Bütün listeyi okumaya vaktin yoksa buradan başla. En çok getirisi olanlar, çoğu birkaç dakikalık iş.</p><ol>')
    for i, j, kisa, m in ilk10_satirlari():
        o.append(f'<li><div><span class="k">{kisa}</span><span class="r">madde {i}.{j}</span><div class="n">{m["n"]}</div></div></li>')
    o.append("</ol></section>")
    for i, (k, b, giris, mad) in enumerate(BOLUMLER, 1):
        o.append(f'<section class="bolum{" ilk" if i == 1 else ""}"><div class="grup"><h2><span class="no">{i}</span>{b}</h2><p class="giris">{giris}</p>')
        for j, m in enumerate(mad, 1):
            o.append(("</div>" if j == 2 else "") + madde_pdf(i, j, m))
        if len(mad) == 1: o.append("</div>")
        o.append("</section>")
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

WJS = r"""
(function(){
 var ANAHTAR='cc-kontrol-v2';
 var kutular=[].slice.call(document.querySelectorAll('.madde input[type=checkbox]'));
 var durum={};
 try{durum=JSON.parse(localStorage.getItem(ANAHTAR)||'{}')||{}}catch(e){durum={}}
 function kaydet(){try{localStorage.setItem(ANAHTAR,JSON.stringify(durum))}catch(e){}}
 var suz='hepsi';
 function guncelle(){
  var top=kutular.length,ok=0;
  kutular.forEach(function(k){
   var m=k.closest('.madde');var y=!!durum[k.id];k.checked=y;m.classList.toggle('yapildi',y);if(y)ok++;
   var s=m.getAttribute('data-s');
   m.hidden=!(suz==='hepsi'||(suz==='acik'&&!y)||suz===s);
  });
  document.getElementById('sayac').textContent=ok+' / '+top+' madde işaretlendi';
  document.getElementById('dolu').style.width=(top?ok*100/top:0)+'%';
  document.querySelectorAll('section.bolum').forEach(function(b){
   var g=b.querySelectorAll('.madde:not([hidden])').length;
   b.querySelector('.bos-durum').hidden=g>0;
   var t=b.querySelectorAll('.madde').length,y=b.querySelectorAll('.madde.yapildi').length;
   var a=document.querySelector('nav.dizin a[href="#'+b.id+'"] small');if(a)a.textContent=y+'/'+t;
  });
 }
 kutular.forEach(function(k){k.addEventListener('change',function(){if(k.checked)durum[k.id]=1;else delete durum[k.id];kaydet();guncelle();});});
 document.querySelectorAll('.suzgec button').forEach(function(b){b.addEventListener('click',function(){
  suz=b.getAttribute('data-suz');document.querySelectorAll('.suzgec button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});guncelle();});});
 document.getElementById('sifirla').addEventListener('click',function(){
  var b=this;if(b.getAttribute('data-onay')!=='1'){b.setAttribute('data-onay','1');b.textContent='Emin misin? Tekrar tıkla';setTimeout(function(){b.removeAttribute('data-onay');b.textContent='İşaretleri temizle'},3000);return;}
  durum={};kaydet();b.removeAttribute('data-onay');b.textContent='İşaretleri temizle';guncelle();});
 document.querySelectorAll('.kopya').forEach(function(b){b.addEventListener('click',function(){
  var pre=b.parentNode.querySelector('pre');var t=pre.textContent;
  function sec(){var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Seçildi, kopyala';}
  try{navigator.clipboard.writeText(t).then(function(){b.textContent='Kopyalandı';setTimeout(function(){b.textContent='Kopyala'},1500)},sec)}catch(e){sec()}
 });});
 guncelle();
})();
"""

def madde_web(i, j, m):
    mid = f"m-{BOLUMLER[i-1][0]}-{j}"
    ornek = (f'<dt>Örnek</dt><dd><div class="ornek"><button type="button" class="kopya">Kopyala</button><pre>{esc(m["o"])}</pre></div></dd>' if m["o"] else "")
    return (f'<div class="madde" data-s="{m["s"]}" id="{mid}-k"><input type="checkbox" id="{mid}" aria-labelledby="{mid}-b">'
            f'<div><label class="bas" id="{mid}-b" for="{mid}"><span class="no2">{i}.{j}</span>{m["e"]}<span class="et {m["s"]}">{SEV[m["s"]]}</span></label>'
            f'<dl><dt>Neden</dt><dd>{m["n"]}</dd><dt>Nasıl</dt><dd>{m["y"]}</dd>{ornek}<dt>Doğrula</dt><dd>{m["d"]}</dd></dl></div></div>')

def web():
    o = ['<title>Claude Code kontrol listesi</title>',
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">',
         f'<style>{WCSS}</style>', '<div class="sar"><nav class="dizin" aria-label="Bölümler"><a href="#ilk10"><span>Önce bu on madde</span></a>']
    for i, (k, b, _, mad) in enumerate(BOLUMLER, 1):
        o.append(f'<a href="#b-{k}"><span>{i}. {b}</span><small>0/{len(mad)}</small></a>')
    o.append('</nav><main>')
    o.append(f'<header class="ust"><h1>{BASLIK}</h1><p>{len(BOLUMLER)} bölüm, {N} madde. Her maddede neden, nasıl, kopyalanabilir örnek ve doğrulama. İşaretlerin yalnız bu tarayıcıda saklanır.</p><div class="surum">{SURUM}</div></header>')
    o.append('<div class="cubuk"><div class="ilerleme"><div class="etiket" id="sayac">0 madde işaretlendi</div><div class="yol"><div class="dolu" id="dolu"></div></div></div>'
             '<div class="suzgec" role="group" aria-label="Süzgeç"><button type="button" data-suz="hepsi" aria-pressed="true">Tümü</button>'
             f'<button type="button" data-suz="temel" aria-pressed="false">Temel ({NT})</button><button type="button" data-suz="ileri" aria-pressed="false">İleri ({N-NT})</button>'
             '<button type="button" data-suz="acik" aria-pressed="false">Yapılmamış</button><button type="button" id="sifirla">İşaretleri temizle</button></div></div>')
    o.append('<details class="okuma"><summary>Nasıl okunur ve sıralama nereden geliyor</summary>' + "".join(f"<p>{p}</p>" for p in OKUMA)
             + f'<p>{SAYI_GIRIS}</p><div class="sayilar">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in SAYILAR) + "</div></details>")
    o.append('<h2 id="ilk10">Önce bu on madde</h2><p class="giris">Bütün listeyi okumaya vaktin yoksa buradan başla. En çok getirisi olanlar, çoğu birkaç dakikalık iş.</p><ol class="ilk10">')
    for i, j, kisa, m in ilk10_satirlari():
        o.append(f'<li><div><a href="#m-{BOLUMLER[i-1][0]}-{j}-k">{kisa}</a> <span class="no2">· {i}.{j}</span><div class="n">{m["n"]}</div></div></li>')
    o.append("</ol>")
    for i, (k, b, giris, mad) in enumerate(BOLUMLER, 1):
        o.append(f'<section class="bolum" id="b-{k}"><h2><span class="no">{i}</span>{b}</h2><p class="giris">{giris}</p>')
        o.extend(madde_web(i, j, m) for j, m in enumerate(mad, 1))
        o.append('<p class="bos-durum" hidden>Bu süzgeçte bu bölümde gösterilecek madde yok.</p></section>')
    o.append(f'<footer>{SURUM}. Özellik adları 16 Ekim 2026\'da code.claude.com belgeleriyle doğrulandı. Bir komut ya da ayar çalışmıyorsa güncel belgeye bak: <a href="https://code.claude.com/docs" style="color:var(--acc)">code.claude.com/docs</a></footer></main></div>')
    o.append(f"<script>{WJS}</script>")
    return "\n".join(o)

def metin(h):
    t = re.sub(r"(?s)<style.*?</style>|<script.*?</script>|<title>.*?</title>|<pre>.*?</pre>", "", h)
    t = re.sub(r"</(p|h1|h2|div|li|td|th|dd|dt|label)>", "\n\n", t); t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\n\s*\n+", "\n\n", html.unescape(t)).strip()

def md_satir(t):
    t = re.sub(r"<code>(.*?)</code>", lambda m: "`" + html.unescape(m.group(1)) + "`", t)
    t = re.sub(r"</?b>", "**", t)
    return html.unescape(re.sub(r"<[^>]+>", "", t))

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
    for i, (k, b, giris, mad) in enumerate(BOLUMLER, 1):
        o += ["", f'<a id="{i}-{k}"></a>', f"## {i}. {b}", "", md_satir(giris), ""]
        for j, m in enumerate(mad, 1):
            o.append(f"- [ ] **{i}.{j} {md_satir(m['e'])}** `{SEV[m['s']]}`")
            o.append(f"  - **Neden:** {md_satir(m['n'])}")
            o.append(f"  - **Nasıl:** {md_satir(m['y'])}")
            if m["o"]:
                o += ["", "    ```", *["    " + l for l in m["o"].split("\n")], "    ```", ""]
            o.append(f"  - **Doğrula:** {md_satir(m['d'])}")
    o += ["", "## Gerçek bir kullanımdan sayılar", "", SAYI_GIRIS, ""]
    o += [f"- **{a}:** {b}" for a, b in SAYILAR]
    o += ["", "## Güncelleme", "", "İçerik tek dosyada: `kaynak/veri.py`. Değiştirdikten sonra:", "", "```sh",
          "python3 kaynak/yap.py",
          "\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\" --headless=new --no-pdf-header-footer \\",
          "  --print-to-pdf=claude-code-kontrol-listesi.pdf \"file://$PWD/kaynak/pdf.html\"", "```", "",
          "## Lisans", "", "[CC BY 4.0](LICENSE): kaynak göstererek paylaşabilir ve uyarlayabilirsin.", ""]
    return "\n".join(o)

def bagimsiz(w):
    return ('<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="description" content="Claude Code\'u iyi kullanmak için 97 maddelik kontrol listesi: neden, nasıl, örnek ve doğrulama.">\n'
            + w.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")

if __name__ == "__main__":
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open(os.path.join(kok, "kaynak", "pdf.html"), "w", encoding="utf-8").write(pdf())
    open(os.path.join(kok, "index.html"), "w", encoding="utf-8").write(bagimsiz(web()))
    open(os.path.join(kok, "README.md"), "w", encoding="utf-8").write(readme())
    print(len(BOLUMLER), "bölüm", N, "madde", NT, "temel")

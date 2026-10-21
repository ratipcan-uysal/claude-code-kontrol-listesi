(function () {
'use strict';
const KEY='cc-kontrol-v2', THEME='cc-kontrol-tema';
const $=id=>document.getElementById(id), boxes=[...document.querySelectorAll('.madde input[type=checkbox]')];
const ids=new Set(boxes.map(x=>x.id));
let state={}, filter='hepsi', storageOK=true;
const isObject=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
function notify(text){$('bildirim').textContent=text;}
function sanitize(x){
  if(!isObject(x))throw Error('İşaretler bir nesne olmalı.');
  const out={};
  for(const [id,value] of Object.entries(x)){
    if(!ids.has(id)||![0,1,true,false].includes(value))throw Error('Bilinmeyen madde veya geçersiz değer.');
    if(value)out[id]=1;
  }
  return out;
}
try{state=sanitize(JSON.parse(localStorage.getItem(KEY)||'{}'));}catch(e){notify('Kayıt okunamadı; yeni işaretlemeden önce varsa JSON yedeğini içe aktar.');}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));storageOK=true;notify('');}catch(e){storageOK=false;notify('Tarayıcı kaydı kullanılamıyor. Bu oturumu JSON olarak dışa aktar.');}}
function norm(t){return t.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ı/g,'i');}
const texts=new Map(boxes.map(x=>[x.id,norm(x.closest('.madde').textContent+' '+x.closest('section').querySelector('h2').textContent)]));
function update(){
 const query=norm($('ara').value.trim());let ok=0,visible=0;
 boxes.forEach(k=>{const m=k.closest('.madde'),done=state[k.id]===1;k.checked=done;m.classList.toggle('yapildi',done);if(done)ok++;
  m.hidden=!((filter==='hepsi'||filter==='acik'&&!done||filter===m.dataset.s)&&texts.get(k.id).includes(query));if(!m.hidden)visible++;
 });
 $('sayac').textContent=ok+' / '+boxes.length+' madde işaretlendi';$('dolu').style.width=(ok*100/boxes.length)+'%';
 $('arama-sonuc').textContent=visible+' madde gösteriliyor';
 document.querySelector('.ilk10').hidden=query!=='';
 $('ilk10').hidden=query!=='';
 $('ilk10').nextElementSibling.hidden=query!=='';
 document.querySelectorAll('section.bolum').forEach(s=>{const shown=s.querySelectorAll('.madde:not([hidden])').length;s.hidden=query!==''&&shown===0;s.querySelector('.bos-durum').hidden=shown>0;
 const n=document.querySelector('nav.dizin a[href="#'+s.id+'"] small');if(n)n.textContent=s.querySelectorAll('.madde.yapildi').length+'/'+s.querySelectorAll('.madde').length;
 });
 document.querySelectorAll('[data-suz]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.suz===filter?'true':'false'));
}
boxes.forEach(k=>k.addEventListener('change',()=>{if(k.checked)state[k.id]=1;else delete state[k.id];save();update();}));
document.querySelectorAll('[data-suz]').forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.suz;update();}));
$('ara').addEventListener('input',update);
let resetTimer;
$('sifirla').addEventListener('click',()=>{
 const b=$('sifirla');if(b.dataset.onay!=='1'){b.dataset.onay='1';b.textContent='Emin misin? Tekrar tıkla';clearTimeout(resetTimer);resetTimer=setTimeout(()=>{delete b.dataset.onay;b.textContent='İşaretleri temizle';},3000);return;}
 state={};save();delete b.dataset.onay;b.textContent='İşaretleri temizle';clearTimeout(resetTimer);update();if(storageOK)notify('İşaretler temizlendi.');
});
$('disa').addEventListener('click',()=>{
 const payload={schema:'claude-code-kontrol-listesi',version:1,exportedAt:new Date().toISOString(),checked:state};
 const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='claude-kontrol-ilerleme.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('İlerleme yedeği indirildi.');
});
$('ice').addEventListener('click',()=>$('dosya').click());
$('dosya').addEventListener('change',async()=>{
 const file=$('dosya').files[0];if(!file)return;
 try{
  if(file.size>100000)throw Error('Dosya çok büyük.');
  const data=JSON.parse(await file.text());
  if(!isObject(data)||data.schema!=='claude-code-kontrol-listesi'||data.version!==1)throw Error('Bu listeye ait desteklenen bir yedek değil.');
  const candidate=sanitize(data.checked);
  if(Object.keys(state).length&&!confirm('Mevcut işaretler bu yedekle değiştirilecek. Devam edilsin mi?')){notify('İçe aktarma iptal edildi.');return;}
  state=candidate;save();update();if(storageOK)notify('İlerleme yedeği yüklendi.');
 }catch(e){notify('İçe aktarılamadı: '+e.message+' Mevcut işaretler korundu.');}finally{$('dosya').value='';}
});
let theme='sistem';try{const x=localStorage.getItem(THEME);if(['light','dark'].includes(x))theme=x;}catch(e){}
function paint(){if(theme==='sistem')document.documentElement.removeAttribute('data-theme');else document.documentElement.dataset.theme=theme;$('tema').textContent='Tema: '+({light:'açık',dark:'koyu',sistem:'sistem'}[theme]);}
$('tema').addEventListener('click',()=>{theme=({sistem:'light',light:'dark',dark:'sistem'})[theme];paint();try{localStorage.setItem(THEME,theme);}catch(e){}});paint();
document.querySelectorAll('.kopya').forEach(b=>b.addEventListener('click',async()=>{
 const pre=b.parentNode.querySelector('pre');try{await navigator.clipboard.writeText(pre.textContent);b.textContent='Kopyalandı';}
 catch(e){const r=document.createRange();r.selectNodeContents(pre);const selection=getSelection();selection.removeAllRanges();selection.addRange(r);b.textContent='Seçildi, kopyala';}
 setTimeout(()=>b.textContent='Kopyala',1800);
}));
function reveal(){
 let id;try{id=decodeURIComponent(location.hash.slice(1));}catch(e){return;}
 const target=document.getElementById(id);if(!target)return;
 if(id==='ilk10'||target.closest('.madde')||target.matches('section.bolum')){filter='hepsi';$('ara').value='';update();requestAnimationFrame(()=>target.scrollIntoView());}
}
window.addEventListener('hashchange',reveal);
function margins(){document.documentElement.style.setProperty('--kaydirma',(document.querySelector('.cubuk').offsetHeight+24)+'px');}
window.addEventListener('resize',margins);margins();update();reveal();
})();

const {chromium}=require('playwright');
const fs=require('fs'), path=require('path'), assert=require('assert');
(async()=>{const browser=await chromium.launch({...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),headless:true});const results=[],errors=[];const base=process.env.TEST_URL||'http://127.0.0.1:8770';const out=path.resolve(__dirname,'../dogrulama');
const check=(name,ok)=>{results.push({name,status:ok?'PASS':'FAIL'});assert(ok,name);};
try{
 const context=await browser.newContext({viewport:{width:1440,height:1000},permissions:['clipboard-read','clipboard-write']});const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(base);await p.evaluate(()=>localStorage.clear());await p.reload();
 check('118 madde',await p.locator('.madde').count()===118);
 await p.locator('#m-talimat-1').check();await p.reload();check('İşaret kalıcılığı',await p.locator('#m-talimat-1').isChecked());
 await p.locator('#sifirla').click();check('Temizleme ilk tık filtreyi bozmuyor',await p.locator('.madde:visible').count()===118);
 await p.locator('#sifirla').click();check('Temizleme ikinci tık',!(await p.locator('#m-talimat-1').isChecked())&&await p.locator('.madde:visible').count()===118);
 await p.locator('[data-suz="temel"]').click();check('Temel filtre 25',await p.locator('.madde:visible').count()===25);
 await p.locator('[data-suz="ileri"]').click();check('İleri filtre 93',await p.locator('.madde:visible').count()===93);
 await p.locator('[data-suz="hepsi"]').click();await p.locator('#m-talimat-1').check();await p.locator('[data-suz="acik"]').click();check('Yapılmamış filtre 117',await p.locator('.madde:visible').count()===117);
 await p.locator('[data-suz="hepsi"]').click();await p.locator('#ara').fill('OTOMATIK');check('Türkçe arama',await p.locator('#m-talimat-7-k').isVisible());
 await p.locator('#ara').fill('zzzz-bulunmaz');check('Boş sonuç',await p.locator('.madde:visible').count()===0);
 await p.evaluate(()=>location.hash='#m-model-3-k');await p.waitForTimeout(100);check('Hash gizli hedefi açar',await p.locator('#m-model-3-k').isVisible()&&await p.locator('#ara').inputValue()==='');
 await p.locator('#ara').fill('Hook');await p.evaluate(()=>location.hash='#ilk10');await p.waitForTimeout(100);check('Başlangıç bağlantısı aramayı kaldırır',await p.locator('.ilk10').isVisible()&&await p.locator('#ara').inputValue()==='');
 await p.goto(base+'/#m-talimat-2-k');check('İlk açılış derin bağlantı',await p.locator('#m-talimat-2-k').isVisible());
 const copy=p.locator('#m-talimat-2-k .kopya');await copy.click();check('Kopyalama',await p.evaluate(()=>navigator.clipboard.readText())===await p.locator('#m-talimat-2-k pre').textContent());
 const download= p.waitForEvent('download');await p.locator('#disa').click();const dl=await download;const filepath=await dl.path();const payload=JSON.parse(fs.readFileSync(filepath,'utf8'));check('Dışa aktarılan JSON',payload.checked['m-talimat-1']===1&&payload.schema==='claude-code-kontrol-listesi');
 const importData=async data=>{await p.locator('#dosya').setInputFiles({name:'test.json',mimeType:'application/json',buffer:Buffer.from(typeof data==='string'?data:JSON.stringify(data))});await p.waitForTimeout(100);};
 p.once('dialog',d=>d.dismiss());await importData({...payload,checked:{'m-talimat-2':1}});check('İçe aktarma iptal korur',await p.locator('#m-talimat-1').isChecked());
 p.once('dialog',d=>d.accept());await importData({...payload,checked:{'m-talimat-2':1}});check('İçe aktarma onayı',await p.locator('#m-talimat-2').isChecked()&&!(await p.locator('#m-talimat-1').isChecked()));
 for(const [name,data] of [['null',null],['bozuk JSON','{'],['yabancı kimlik',{...payload,checked:{'m-foreign':1}}],['geçersiz değer',{...payload,checked:{'m-talimat-1':'yes'}}],['büyük dosya','x'.repeat(100001)]]){await importData(data);check('Hatalı içe aktarım korunur: '+name,await p.locator('#m-talimat-2').isChecked()&&(await p.locator('#bildirim').textContent()).includes('Mevcut işaretler korundu'));}
 await p.evaluate(()=>{localStorage.setItem('cc-kontrol-v2','[]');location.hash='';});await p.reload();check('Bozuk yerel kayıt dayanıklılığı',await p.locator('.madde:visible').count()===118);await p.locator('#m-talimat-1').check();check('Bozuk kayıt sonrası işaret',await p.locator('#m-talimat-1').isChecked());
 await p.locator('#tema').click();check('Açık tema',await p.locator('html').getAttribute('data-theme')==='light');await p.evaluate(()=>window.scrollTo(0,0));await p.screenshot({path:path.join(out,'desktop-light.png')});
 await p.locator('#tema').click();await p.reload();check('Koyu tema kalıcılığı',await p.locator('html').getAttribute('data-theme')==='dark');await p.screenshot({path:path.join(out,'desktop-dark.png')});
 await p.locator('#ara').focus();await p.keyboard.press('Tab');check('Klavye sırası',await p.evaluate(()=>document.activeElement.id)==='tema');
 await p.locator('#tema').click();await p.locator('#tema').click();
 for(const width of [390,320]){await p.setViewportSize({width,height:844});await p.evaluate(()=>window.scrollTo(0,0));check('Yatay taşma '+width,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:path.join(out,'mobile-'+width+'.png')});}
 await p.locator('#ara').fill('Hook hata politikasını');await p.locator('#m-hook-5-k').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'mobile-detail.png')});
 const denied=await browser.newContext();await denied.addInitScript(()=>{Storage.prototype.setItem=function(){throw Error('blocked')};});const q=await denied.newPage();await q.goto(base);await q.locator('#m-talimat-1').check();check('Depolama engeli görünür', (await q.locator('#bildirim').textContent()).includes('kaydı kullanılamıyor'));await denied.close();
 const ekler=fs.readdirSync(path.resolve(__dirname,'../ekler')).filter(f=>f.endsWith('.html'));check('Ek sayfaları var',ekler.length>0&&await p.locator('#ekler ul.ekler li').count()===ekler.length);
 await p.setViewportSize({width:1440,height:1000});await p.goto(base+'/ekler/deneyimler.html');await p.locator('main.ek a[href*="index.html#m-"]').first().click();await p.waitForLoadState();await p.waitForTimeout(150);check('Ekten maddeye bağlantı',await p.evaluate(()=>{const t=document.querySelector(location.hash);return !!t&&!t.hidden&&t.getBoundingClientRect().top<innerHeight;}));
 for(const f of ekler){await p.goto(base+'/ekler/'+f);for(const width of [1440,320]){await p.setViewportSize({width,height:900});check('Ek yatay taşma '+f+' '+width,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}await p.screenshot({path:path.join(out,'ek-'+f.replace('.html','')+'-320.png'),fullPage:false});}
 const bolumler=fs.readdirSync(path.resolve(__dirname,'../rehber')).filter(f=>f.endsWith('.html'));
 for(const f of bolumler){await p.goto(base+'/rehber/'+f);for(const width of [1440,320]){await p.setViewportSize({width,height:900});check('Rehber yatay taşma '+f+' '+width,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}await p.screenshot({path:path.join(out,'rehber-'+f.replace('.html','')+'-320.png')});}
 check('JS konsol hatası yok',errors.length===0);
 if(!process.env.TEST_URL){const pdf=await context.newPage();await pdf.goto('http://127.0.0.1:8770/kaynak/pdf.html');await pdf.pdf({path:path.resolve(__dirname,'../claude-code-kontrol-listesi.pdf'),printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font-size:8px;color:#596273"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'});}
}finally{fs.writeFileSync(path.join(out,process.env.TEST_URL?'browser-live.json':'browser-local.json'),JSON.stringify({browser:browser.version(),base,results,errors},null,2));await browser.close();}
console.log(JSON.stringify({checks:results.length,passed:results.filter(r=>r.status==='PASS').length}));
})().catch(e=>{console.error(e);process.exit(1)});

import copy, unittest, re
from pathlib import Path
from html.parser import HTMLParser
import yap
class Tests(unittest.TestCase):
 def test_current_content(self):
  yap.validate();self.assertEqual(yap.N,125);self.assertEqual(yap.NT,25)
 def test_missing_verification_fails(self):
  b=copy.deepcopy(yap.BOLUMLER);b[0][3][0]['d']=''
  with self.assertRaisesRegex(ValueError,'Eksik'):yap.validate(b)
  b[0][3][0]['d']='Kanıt';yap.validate(b)
 def test_duplicate_id_fails(self):
  b=copy.deepcopy(yap.BOLUMLER);b.append(b[0])
  with self.assertRaisesRegex(ValueError,'Tekrarlanan'):yap.validate(b)
 def test_unknown_source_fails(self):
  b=copy.deepcopy(yap.BOLUMLER);b[0][3][0]['r']=['missing']
  with self.assertRaisesRegex(ValueError,'Bilinmeyen kaynak'):yap.validate(b)
 def test_original_ids_preserved(self):
  original=[6,6,7,4,5,6,6,5,6,3,6,6,5,4,4,4,5,4,5]
  html=yap.web()
  for (k,*_),n in zip(yap.BOLUMLER,original):
   for j in range(1,n+1):self.assertIn(f'id="m-{k}-{j}"',html)
 def test_generated_files_current(self):
  root=Path(__file__).resolve().parent.parent
  self.assertEqual((root/'index.html').read_text(),yap.bagimsiz(yap.web()))
  self.assertEqual((root/'README.md').read_text(),yap.readme())
 def test_html_ids_and_anchors(self):
  class Parser(HTMLParser):
   def __init__(self):super().__init__();self.ids=[];self.links=[]
   def handle_starttag(self,tag,attrs):
    a=dict(attrs)
    if 'id' in a:self.ids.append(a['id'])
    if a.get('href','').startswith('#'):self.links.append(a['href'][1:])
  p=Parser();p.feed(yap.web());self.assertEqual(len(p.ids),len(set(p.ids)))
  self.assertTrue(set(p.links)<=set(p.ids))
 def test_ekler_current_and_linked(self):
  root=Path(__file__).resolve().parent.parent
  for e in yap.EKLER:
   self.assertEqual((root/'ekler'/(e['ad']+'.html')).read_text(),yap.ek_html(e))
   self.assertEqual((root/'ekler'/(e['ad']+'.md')).read_text(),yap.ek_md(e))
   self.assertNotIn('[[',yap.ek_html(e)+yap.ek_md(e))
   self.assertIn(f'href="ekler/{e["ad"]}.html"',yap.web())
  ids=set(re.findall(r'id="([^"]+)"',yap.web()))
  for e in yap.EKLER:
   for hedef in re.findall(r'href="\.\./index\.html#([^"]+)"',yap.ek_html(e)):self.assertIn(hedef,ids)
 def test_rehber_current_and_linked(self):
  root=Path(__file__).resolve().parent.parent
  for b in yap.REHBER:
   self.assertEqual((root/'rehber'/(b['ad']+'.html')).read_text(),yap.bolum_html(b))
   self.assertEqual((root/'rehber'/(b['ad']+'.md')).read_text(),yap.bolum_md(b))
   self.assertNotRegex(yap.bolum_html(b)+yap.bolum_md(b),r'\[\[|\{\{')
   self.assertIn(f'href="{b["ad"]}.html"',yap.rehber_index())
  self.assertEqual((root/'rehber'/'index.html').read_text(),yap.rehber_index())
  self.assertIn('href="rehber/index.html"',yap.web())
 def test_bad_rehber_link_fails(self):
  import copy
  r=copy.deepcopy(yap.REHBER);r[0]['md']+='{{ek:yok}}'
  with self.assertRaisesRegex(ValueError,'Geçersiz rehber bağlantısı'):yap.validate_rehber(r)
  r[0]['md']=r[0]['md'].replace('{{ek:yok}}','bölüm {{bolum:1}}')
  with self.assertRaisesRegex(ValueError,'önüne'):yap.validate_rehber(r)
  r[0]['md']=r[0]['md'].replace('bölüm {{bolum:1}}','{{bolum:99}}')
  with self.assertRaisesRegex(ValueError,'Geçersiz rehber bağlantısı'):yap.validate_rehber(r)
 def test_bad_ek_reference_fails(self):
  ek=[{'ad':'x','md':'Bak: [[3.99]]'}]
  with self.assertRaisesRegex(ValueError,'Geçersiz madde bağlantısı'):yap.validate_ekler(ek)
  yap.validate_ekler([{'ad':'x','md':'Bak: [[3.1]]'}])
 def test_md_html_table_and_code(self):
  h=yap.md_html('| A | B |\n|---|---|\n| `x` | y |\n\n```\n<a>\n```')
  self.assertIn('<th>A</th>',h);self.assertIn('<td data-e="B">y</td>',h);self.assertIn('<pre>&lt;a&gt;</pre>',h)
 def test_md_satir_keeps_angle_brackets_in_code(self):
  self.assertEqual(yap.md_satir('Yol: <code>~/.claude/skills/&lt;ad&gt;/SKILL.md</code>'),'Yol: `~/.claude/skills/<ad>/SKILL.md`')
 def test_pdf_contains_each_item(self):
  pdf=yap.pdf()
  for i,(_,_,_,ms) in enumerate(yap.BOLUMLER,1):
   for j,m in enumerate(ms,1):self.assertIn(f'{i}.{j} {m["e"]}',pdf)
if __name__=='__main__':unittest.main()

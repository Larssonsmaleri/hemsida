"""Bygger public/index.html från src/sida.html.

Kör från förrådets rot:  python3 src/build.py src/sida.html public

src/sida.html är utkastet (samma fil som visas som förhandsvisning i Claude).
Skriptet gör det till en fristående sida: riktiga tel- och mejllänkar, Netlify-formulär,
metataggar för Google och egna typsnittsfiler i stället för Google Fonts.
"""
import sys,re,json,os
src,outdir=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf8').read()
s=re.sub(r'<title>.*?</title>\n','',s,count=1)
s=re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n','',s)
s=re.sub(r'<meta name="description"[^>]*>\n','',s)
i=s.index('<header class="nav">')
head_part,body=s[:i],s[i:]
def rep(a,b,must=True):
    global body
    if must: assert a in body, a[:60]
    body=body.replace(a,b)
rep('        <span class="wall-note">Plats för er film eller bild från ett jobb</span>\n','',False)
rep('<span class="tel">0730-57 98 55</span>','<a class="tel" href="tel:+46730579855" style="text-decoration:none">0730-57 98 55</a>')
rep('<span class="v tel">0730-57 98 55</span>','<a class="v tel" href="tel:+46730579855" style="text-decoration:none">0730-57 98 55</a>')
rep('href="tel:0730579855"','href="tel:+46730579855"')
rep('<span class="v">kevin@larssonsmaleriservice.se</span>','<a class="v" href="mailto:kevin@larssonsmaleriservice.se" style="text-decoration:none">kevin@larssonsmaleriservice.se</a>')
rep('<form class="offer" id="offer" novalidate>','<form class="offer" id="offer" name="offert" method="POST" action="https://formsubmit.co/kevin@larssonsmaleriservice.se" novalidate>\n        <input type="hidden" name="_subject" value="Ny offertförfrågan från hemsidan">\n        <input type="hidden" name="_template" value="table">\n        <input type="hidden" name="_captcha" value="false">\n        <p hidden><label>Lämna tomt: <input name="_honey"></label></p>')
for fid,nm in [('f-svc','tjanst'),('f-namn','namn'),('f-tel','telefon'),('f-mejl','epost'),('f-ort','adress'),('f-msg','beskrivning')]:
    rep(f'id="{fid}"',f'id="{fid}" name="{nm}"')
rep('<p class="ok" id="ok" hidden>Det här är ett förslag på ny hemsida. Formuläret kopplas till er mejl när sidan går live.</p>','<p class="ok" id="ok" hidden>Tack! Vi har fått din förfrågan och ringer upp dig.</p>\n        <p class="fine" id="fail" hidden>Det gick inte att skicka just nu. Ring oss på 0730-57 98 55 så hjälper vi dig direkt.</p>')
old=body[body.index("  $('offer').addEventListener('submit'"):body.index("  if('IntersectionObserver' in window")]
new="""  $('offer').addEventListener('submit',async e=>{
    e.preventDefault();
    const f=e.target, ok=$('f-namn').value.trim()&&$('f-tel').value.trim();
    $('err').hidden=!!ok;$('ok').hidden=true;$('fail').hidden=true;
    if(!ok)return;
    const btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='Skickar…';
    try{
      const r=await fetch('https://formsubmit.co/ajax/kevin@larssonsmaleriservice.se',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(f)))});
      const j=await r.json().catch(()=>({}));
      if(!r.ok||String(j.success)!=='true')throw new Error(r.status);
      f.reset();$('ok').hidden=false;
    }catch(_){$('fail').hidden=false}
    btn.disabled=false;btn.textContent='Skicka förfrågan';
  });
"""
body=body.replace(old,new)
# --- self-host fonts (no calls to Google; faster and GDPR-clean) ---
import shutil
FN='/tmp/claude-0/-home-claude/3555c828-70f5-503d-bb45-a2157e1a7fa9/scratchpad/fonttest/node_modules/@fontsource'
faces=[("Instrument Serif","instrument-serif",400,"normal"),("Instrument Serif","instrument-serif",400,"italic"),("Covered By Your Grace","covered-by-your-grace",400,"normal"),
("Inter","inter",400,"normal"),("Inter","inter",500,"normal"),("Inter","inter",600,"normal"),("Raleway","raleway",300,"normal"),("Raleway","raleway",600,"normal")]
os.makedirs(os.path.join(outdir,'fonts'),exist_ok=True)
ff=[]
for fam,pkg,w,st in faces:
    f=f"{pkg}-latin-{w}-{st}.woff2"
    if os.path.exists(os.path.join(FN,pkg,'files',f)): shutil.copy(os.path.join(FN,pkg,'files',f),os.path.join(outdir,'fonts',f))  # annars används filen som redan ligger i public/fonts
    ff.append(f'@font-face{{font-family:"{fam}";font-style:{st};font-weight:{w};font-display:swap;src:url(fonts/{f}) format("woff2")}}')
head_part=re.sub(r'<link rel="preconnect"[^>]*>\n','',head_part)
head_part,nn=re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n','<style>'+''.join(ff)+'</style>\n',head_part); assert nn==1
ld={"@context":"https://schema.org","@type":"HousePainter","name":"Larssons Måleriservice & Entreprenad AB","url":"https://www.larssonsmaleriservice.se/","telephone":"+46730579855","email":"kevin@larssonsmaleriservice.se",
"address":{"@type":"PostalAddress","streetAddress":"Tollareslingan 50","postalCode":"132 49","addressLocality":"Saltsjö-Boo","addressCountry":"SE"},
"areaServed":["Stockholm","Stockholms län","Nacka","Värmdö"],"sameAs":["https://www.instagram.com/larssonsmaleriservice/"],
"description":"Målare i Stockholm. Invändig och utvändig målning, tapetsering, spackling, snickerier, badrum och kontor. Gratis hembesök och ROT-avdrag."}
fav="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23EE7203'/%3E%3Ctext x='32' y='40' font-family='Arial' font-size='19' font-weight='700' fill='%23fff' text-anchor='middle'%3ELM%26amp;E%3C/text%3E%3C/svg%3E"
desc="Målare i Stockholm, Nacka och Värmdö. Invändig och utvändig målning, tapetsering och spackling. Gratis hembesök, fast offert och ROT-avdrag. Ring 0730-57 98 55."
title="Målare i Stockholm | Larssons Måleriservice &amp; Entreprenad AB"
out=f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://www.larssonsmaleriservice.se/">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://www.larssonsmaleriservice.se/">
<link rel="icon" href="{fav}">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
{head_part.strip()}
</head>
<body style="margin:0">
{body.strip()}
</body>
</html>
"""
os.makedirs(outdir,exist_ok=True)
open(os.path.join(outdir,'index.html'),'w',encoding='utf8').write(out)
open(os.path.join(outdir,'robots.txt'),'w').write("User-agent: *\nAllow: /\nSitemap: https://www.larssonsmaleriservice.se/sitemap.xml\n")
open(os.path.join(outdir,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>https://www.larssonsmaleriservice.se/</loc><lastmod>2026-11-12</lastmod></url>\n</urlset>\n')

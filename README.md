# Hemsida för Larssons Måleriservice & Entreprenad AB

Sidan ligger på GitHub Pages och visas på https://www.larssonsmaleriservice.se

- `src/sida.html` är källan. Ändra där.
- `src/build.py` bygger den färdiga sidan till `public/`.
- `./publicera.sh "vad som ändrats"` bygger, sparar och publicerar. Grenen `gh-pages` innehåller bara `public/` och är den som visas.
- `public/CNAME` håller domänen. Ta inte bort den.
- Offertformuläret skickas via FormSubmit till kevin@larssonsmaleriservice.se.
- Bilder ligger i `public/bilder/`, typsnitt i `public/fonts/`.

Netlify-projektet larssons-maleri används inte längre (gratiskvoten räckte inte för täta ändringar).

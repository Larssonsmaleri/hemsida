# hemsida

Hemsidan för Larssons Måleriservice & Entreprenad AB.

- `public/` är själva sidan. Netlify publicerar den mappen varje gång något ändras på grenen `main`.
- `public/index.html` är hela sidan. `public/bilder/` och `public/fonts/` är bilder och typsnitt.
- Testadress: https://larssons-maleri.netlify.app

## Ändra sidan

1. Ändra i `src/sida.html`.
2. Kör `python3 src/build.py src/sida.html public`.
3. Lägg upp ändringen på `main`. Netlify publicerar den inom någon minut.

Bilder till jobb läggs i `public/bilder/`.

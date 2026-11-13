#!/bin/sh
# Bygger sidan och publicerar den på GitHub Pages (grenen gh-pages = innehållet i public/).
set -e
python3 src/build.py src/sida.html public
printf 'www.larssonsmaleriservice.se\n' > public/CNAME
touch public/.nojekyll
git add -A
git commit -m "${1:-Uppdatera sidan}" || true
git push origin main
git branch -D gh-pages 2>/dev/null || true
git subtree split --prefix public -b gh-pages
git push -f origin gh-pages

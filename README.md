# Top-down-spill i Python – elevmapper

Denne mappa er GitHub Pages-siden for elevene. Den lages av `_verktoy/lag_nettside.py`
(kjør `lag_elevmappe.py` først). Ikke rediger filene her for hånd.

## Publisere første gang

1. Lag et nytt repo på github.com (for eksempel `topdown-spill`).
2. Last opp alt i denne mappa (dra filene inn på «Add file → Upload files», eller bruk git):

       cd Nettside
       git init -b main
       git add .
       git commit -m "Elevmapper"
       git remote add origin https://github.com/<brukernavn>/topdown-spill.git
       git push -u origin main

3. På GitHub: Settings → Pages → Source: «Deploy from a branch», Branch: `main`, mappe `/ (root)`.
4. Etter et minutt ligger siden på `https://<brukernavn>.github.io/topdown-spill/`.

## Oppdatere

Kjør `python _verktoy/lag_elevmappe.py`, `python _verktoy/lag_teorikurs.py` og `python _verktoy/lag_nettside.py`, og deretter
`git add . && git commit -m "Oppdatert" && git push` fra denne mappa.

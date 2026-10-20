# ============================================================
#  SKATTEJAKTEN – STEG 1: Din egen eng
# ============================================================
#
#  I dag lager du verdenen i spillet: en eng med gress, blomster
#  og en sti. Du setter ut helten og en mynt som snurrer.
#  Ingenting beveger seg ennå – det kommer i steg 2.
#
#  Kjør fila med F5. Endre litt, kjør igjen, og se hva som skjer!
#
#  Skjermen er 240 piksler bred og 160 piksler høy.
#  x er hvor langt mot HØYRE noe står.
#  y er hvor langt NED noe står.
#
#      x = 0                     x = 240
#      +-------------------------+  y = 0
#      |                         |
#      |                         |
#      +-------------------------+  y = 160
#
# ============================================================

from spillmotor import *


# ---------- KARTET ----------
# Hvert tegn er én rute på 16 x 16 piksler.
# Hver linje er en rad, og hver rad har 15 tegn.
#   .  gress      ,  litt annet gress      *  blomster      =  sti

# OPPGAVE 1: Tegn på kartet. Bytt noen . med * (blomster) eller = (sti).
ENGEN = [
    "..,......*...,.",
    ".*....,........",
    "......=====....",
    "..,...=...=..*.",
    "=======...=====",
    "......=...=....",
    ".*....=====..,.",
    "...,.......*...",
    ".......,.......",
    ".*.........,.*.",
]

# RUTER sier hvilket bilde hvert tegn skal ha
RUTER = {
    ".": "gress_stor",
    ",": "gress_2",
    "*": ["gress_blomst", "gress_blomst_2"],    # to bilder = blomstene vaier
    "=": "sti",
}

# Myke kanter der stien møter gresset
KANTER = {"=": ("stikant", ".,*")}

tegn_kart(ENGEN, RUTER, KANTER)


# ---------- FIGURENE ----------
# Figur("bildenavn", x, y) lager en figur med et bilde fra mappen bilder/.

# OPPGAVE 2: Flytt helten midt på skjermen. Bytt ut 0, 0 med 112, 64.
helt = Figur("helt_ned_1", 0, 0, skygge=True)

# OPPGAVE 3: Legg ut en mynt. Bildet heter "mynt_1". Sett den der du vil.
pass

# OPPGAVE 4: Få mynten til å snurre med mynt.animer(...).
pass


# ---------- START ----------
# OPPGAVE 5: Gi spillet ditt eget navn. Teksten står øverst i vinduet.
start(tittel="Skriv navnet på spillet her")

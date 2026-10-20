# ============================================================
#  SKATTEJAKTEN – STEG 4: Plukk opp mynten
# ============================================================
#
#  I dag kan helten ta mynten! Når han går på den, skal det
#  si «pling», mynten skal hoppe til et nytt sted, og du får
#  ett poeng. Poengene står øverst til venstre.
#
#  Taster:  piltastene = gå
#
#  Nytt i dag:
#    - helt.treffer(mynt) er sant når helten står oppå mynten
#    - en funksjon: def ta_mynt(): er noen linjer med et navn.
#      ta_mynt() kjører linjene.
#    - random.randint(0, 224) gir et tilfeldig tall fra 0 til 224
#    - en variabel som teller: poeng = poeng + 1
#    - global: trengs når en funksjon skal ENDRE en variabel utenfor seg selv
#
# ============================================================

import random
from spillmotor import *


# ---------- KARTET ----------
# Hvert tegn er én rute på 16 x 16 piksler.
#   .  gress      ,  litt annet gress      *  blomster      =  sti

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

RUTER = {
    ".": "gress_stor",
    ",": "gress_2",
    "*": ["gress_blomst", "gress_blomst_2"],
    "=": "sti",
}

KANTER = {"=": ("stikant", ".,*")}

tegn_kart(ENGEN, RUTER, KANTER)


# ---------- FIGURENE ----------

helt = Figur("helt_ned_1", 112, 64, skygge=True)

mynt = Figur("mynt_1", 48, 32)
mynt.animer(["mynt_1", "mynt_2", "mynt_3", "mynt_4"], fart=8)

FART = 2

poeng = 0           # hvor mange mynter helten har tatt


# ---------- TEKST ----------
# Tekst("tekst", x, y) skriver en tekst. skygge gir en mørk kant, så teksten synes bedre.

melding = Tekst("Finn mynten!", 4, 148, skygge="#181820")
poengtekst = Tekst("Mynter: 0", 4, 4, skygge="#181820")


# ---------- FUNKSJONER ----------

def ta_mynt():
    """Kjøres når helten treffer mynten."""
    global poeng

    # Mynten hopper til et tilfeldig sted på skjermen
    mynt.x = random.randint(0, 224)
    # OPPGAVE 1: Gjør det samme med mynt.y. Mynten er 16 høy, så y kan være 0 til 144.
    pass

    # OPPGAVE 2: Spill lyden "mynt", og lag glitter der helten står.
    pass

    # OPPGAVE 3: Tell opp poengene: poeng skal bli én mer enn før.
    pass
    poengtekst.tekst = f"Mynter: {poeng}"     # viser poengene på skjermen


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Denne funksjonen kjøres 60 ganger i sekundet.

    # ---- gå med piltastene ----
    if tast_holdes("hoyre"):
        helt.x = helt.x + FART
        helt.bilde = "helt_hoyre_1"
    if tast_holdes("venstre"):
        helt.x = helt.x - FART
        helt.bilde = "helt_venstre_1"
    if tast_holdes("ned"):
        helt.y = helt.y + FART
        helt.bilde = "helt_ned_1"
    if tast_holdes("opp"):
        helt.y = helt.y - FART
        helt.bilde = "helt_opp_1"

    # ---- hold helten på skjermen ----
    # Venstre kant: er x mindre enn 0, setter vi den tilbake til 0.
    if helt.x < 0:
        helt.x = 0

    # Høyre kant: helten er 16 bred, så x kan være høyst 240 - 16 = 224.
    if helt.x > 224:
        helt.x = 224

    # Toppen: y kan ikke være mindre enn 0.
    if helt.y < 0:
        helt.y = 0

    # Bunnen: helten er 24 høy, så y kan være høyst 160 - 24 = 136.
    if helt.y > 136:
        helt.y = 136

    # ---- ta mynten ----
    # Står helten oppå mynten? Da kjører vi alle linjene i ta_mynt().
    if helt.treffer(mynt):
        ta_mynt()
        # OPPGAVE 4: Bytt teksten nederst til «Bra! Finn en til!».
        pass


start(tittel="Skattejakten")

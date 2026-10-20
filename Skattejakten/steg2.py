# ============================================================
#  SKATTEJAKTEN – STEG 2: Gå med piltastene
# ============================================================
#
#  I dag får helten bevege seg! Nederst i fila er det en ny
#  funksjon, oppdater(). Spillet kjører den 60 ganger i sekundet.
#  Hver gang flytter vi helten litt, og da ser det ut som han går.
#
#  Taster:  piltastene = gå
#
#  Nytt i dag:
#    - oppdater() kjøres 60 ganger i sekundet
#    - if: gjør noe BARE hvis noe er sant
#    - tast_holdes("hoyre") er sant så lenge du holder tasten nede
#    - helt.x = helt.x + 1 flytter helten én piksel mot høyre
#
# ============================================================

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

# Hvor mange piksler helten går hver gang oppdater() kjøres
# OPPGAVE 1: Gjør helten raskere. Prøv 2 – eller 5!
FART = 1


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Denne funksjonen kjøres 60 ganger i sekundet.

    # Høyre piltast: helten går mot høyre (x blir større) og ser mot høyre
    if tast_holdes("hoyre"):
        helt.x = helt.x + FART
        helt.bilde = "helt_hoyre_1"

    # OPPGAVE 2: Venstre piltast. Kopier de tre linjene over og endre dem.
    pass

    # OPPGAVE 3: Pil ned. Nå er det y som skal bli større.
    pass

    # OPPGAVE 4: Pil opp. y skal bli mindre.
    pass


start(tittel="Skattejakten")

# ============================================================
#  SKATTEJAKTEN – STEG 3: Hold deg på skjermen
# ============================================================
#
#  Nå kan helten gå rett ut av skjermen og forsvinne. I dag
#  stopper du ham ved kantene, og du skriver en tekst på skjermen.
#
#  Taster:  piltastene = gå
#
#  Nytt i dag:
#    - < betyr «mindre enn», > betyr «større enn»
#    - en if som sjekker et tall: if helt.x < 0:
#    - Tekst("Hei", x, y) skriver tekst på skjermen
#
#  Helten er 16 piksler bred og 24 piksler høy.
#  x og y er øverste venstre hjørne av bildet hans.
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

FART = 2


# ---------- TEKST ----------
# Tekst("tekst", x, y) skriver en tekst. skygge gir en mørk kant, så teksten synes bedre.

# OPPGAVE 1: Skriv «Finn mynten!» nederst til venstre (x = 4, y = 148).
melding = Tekst("", 4, 148, skygge="#181820")


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

    # OPPGAVE 2: Høyre kant. Helten er 16 bred, så x kan være høyst 240 - 16 = 224.
    pass

    # OPPGAVE 3: Toppen. y kan ikke være mindre enn 0.
    pass

    # OPPGAVE 4: Bunnen. Helten er 24 høy, så y kan være høyst 160 - 24 = 136.
    pass


start(tittel="Skattejakten")

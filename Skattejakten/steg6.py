# ============================================================
#  SKATTEJAKTEN – STEG 6: Vinn spillet
# ============================================================
#
#  I dag blir spillet ferdig: det får musikk, slimet blir
#  raskere for hver mynt du tar, du VINNER når du har 10 mynter,
#  og du kan spille igjen med Enter.
#
#  Taster:  piltastene = gå   Enter = spill igjen (når spillet er over)
#
#  Nytt i dag:
#    - spill_musikk("navn") spiller musikk om og om igjen
#    - en variabel som vokser litt hver gang: slim_fart = slim_fart + 0.1
#    - tast_trykket("enter") er sant bare i det øyeblikket du trykker
#    - en funksjon som setter alt tilbake slik det var i starten
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


# ---------- MUSIKK ----------
# Musikken ligger i mappen musikk/. Prøv "oververden", "landsby" eller "tittel".
# OPPGAVE 1: Start musikken "oververden".
pass


# ---------- FIGURENE ----------

helt = Figur("helt_ned_1", 112, 64, skygge=True)

mynt = Figur("mynt_1", 48, 32)
mynt.animer(["mynt_1", "mynt_2", "mynt_3", "mynt_4"], fart=8)

FART = 2

poeng = 0           # hvor mange mynter helten har tatt
liv = 3             # hvor mange liv helten har igjen
ferdig = False      # blir True når spillet er over

slim = Figur("slim_1", 208, 128)
slim.animer(["slim_1", "slim_2"], fart=12)

# Hvor mange piksler slimet kryper hver gang oppdater() kjøres. 0.5 er en halv piksel.
slim_fart = 0.5


# ---------- TEKST ----------
# Tekst("tekst", x, y) skriver en tekst. skygge gir en mørk kant, så teksten synes bedre.

melding = Tekst("Finn mynten!", 4, 148, skygge="#181820")
poengtekst = Tekst("Mynter: 0", 4, 4, skygge="#181820")
livtekst = Tekst("Liv: 3", 200, 4, skygge="#181820")
stor = Tekst("", 0, 68, storrelse=2, skygge="#181820")     # stor tekst midt på skjermen


# ---------- FUNKSJONER ----------

def ta_mynt():
    """Kjøres når helten treffer mynten."""
    global poeng, slim_fart, ferdig

    # Mynten hopper til et tilfeldig sted på skjermen
    mynt.x = random.randint(0, 224)
    mynt.y = random.randint(0, 144)

    # Pling og glitter
    spill_lyd("mynt")
    effekt("glitter", helt.midt_x, helt.midt_y)

    # Ett poeng til
    poeng = poeng + 1
    poengtekst.tekst = f"Mynter: {poeng}"     # viser poengene på skjermen

    # OPPGAVE 2: Gjør slimet litt raskere: slim_fart skal bli 0.1 mer enn før.
    pass

    # OPPGAVE 3: Har helten 10 mynter, har du VUNNET. Se hvordan GAME OVER er laget i au().
    pass


def vis_stor(tekst):
    """Skriver en stor tekst midt på skjermen."""
    stor.tekst = tekst
    stor.x = (240 - stor.bredde) / 2


def flytt_slim():
    """Slimet kryper mot helten."""
    # Er slimet til venstre for helten, kryper det mot høyre – og omvendt.
    if slim.x < helt.x:
        slim.x = slim.x + slim_fart
    if slim.x > helt.x:
        slim.x = slim.x - slim_fart

    # ... og opp og ned
    if slim.y < helt.y:
        slim.y = slim.y + slim_fart
    if slim.y > helt.y:
        slim.y = slim.y - slim_fart


def au():
    """Kjøres når slimet tar helten."""
    global liv, ferdig
    spill_lyd("au")
    helt.blink(1)
    rist_skjerm()

    # Slimet hopper til hjørnet som er lengst unna helten
    if helt.x < 120:
        slim.x = 224
    else:
        slim.x = 0
    if helt.y < 80:
        slim.y = 144
    else:
        slim.y = 0

    # Ett liv mindre
    liv = liv - 1
    livtekst.tekst = f"Liv: {liv}"

    # Er liv blitt 0, er det GAME OVER
    if liv == 0:
        vis_stor("GAME OVER")
        spill_lyd("game_over")
        ferdig = True


def nytt_spill():
    """Setter alt tilbake slik det var i starten."""
    global poeng, liv, ferdig, slim_fart
    poeng = 0
    liv = 3
    ferdig = False
    slim_fart = 0.5
    poengtekst.tekst = "Mynter: 0"
    livtekst.tekst = "Liv: 3"
    melding.tekst = "Finn mynten!"
    vis_stor("")
    helt.x = 112
    helt.y = 64
    helt.bilde = "helt_ned_1"
    slim.x = 208
    slim.y = 128


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Denne funksjonen kjøres 60 ganger i sekundet.

    # Er spillet over, skal ingenting flytte seg. return avslutter oppdater() her.
    if ferdig:
        melding.tekst = "Trykk Enter for å spille igjen"
        # OPPGAVE 4: Trykker spilleren Enter, skal nytt_spill() kjøres.
        pass
        return

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
        melding.tekst = "Bra! Finn en til!"

    # ---- slimet ----
    flytt_slim()
    if helt.treffer(slim):
        au()


start(tittel="Skattejakten")

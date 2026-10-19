# ============================================================
#  EVENTYRET – STEG 1: Kart og bevegelse
# ============================================================
#
#  I dag lager du starten på et eventyrspill: en eng med gress,
#  en sti, et lite vann og noen steiner. Helten skal gå rundt
#  med piltastene, holde seg på skjermen og stoppe når han går
#  inn i noe.
#
#  Taster:  piltastene = gå
#
#  Nytt i dag:
#    - spill-løkka: oppdater() kjøres 60 ganger i sekundet
#    - koordinater: x er piksler mot høyre, y er piksler NEDOVER
#    - kartet er en liste med tekst, der hvert tegn er én rute
#    - kollisjon: rute_ved(x, y) sier hva som ligger på et punkt
#
#  Skjermen er 15 ruter bred og 10 ruter høy.
#  Hver rute er 16 x 16 piksler, så skjermen er 240 x 160 piksler.
#
#      x = 0                     x = 240
#      +-------------------------+  y = 0
#      |                         |
#      |                         |
#      +-------------------------+  y = 160
#
# ============================================================

from spillmotor import *

BREDDE = 240        # skjermen i piksler
HOYDE = 160


# ---------- KARTET ----------
# Hvert tegn er én rute. Ordboka RUTER sier hvilket bilde hvert tegn skal ha.
#   .  ,  *   gress (litt forskjellig)      =   sti
#   ~         vann                          B   busk
#   S         stein

ENGEN = [
    "BBBBBBB=BBBBBBB",
    "B..,...=....*.B",
    "B.*....=..,...B",
    "B..~~~~=......B",
    "B..~~~~=====...",
    "B..~~~~....====",
    "B.....,..S.....",
    "B.S.......*...B",
    "B....,....SS..B",
    "BBBBBBBBBBBBBBB",
]

RUTER = {
    ".": "gress_stor",                       # et stort mønster (like stort som skjermen)
    ",": "gress_2",
    "*": ["gress_blomst", "gress_blomst_2"], # blomstene vaier
    "=": "sti",
    "~": ["vann_1", "vann_2", "vann_3"],     # en liste med bilder = animert rute
    "B": "busk",
    "S": "stein",
}

# Myke kanter der stien og vannet møter gresset
KANTER = {"=": ("stikant", ".,*"), "~": ("vannkant", ".,*=B")}

# Tegn som helten IKKE kan gå gjennom
# OPPGAVE 4: Gjør buskene og vannet til hindringer også.
HINDRINGER = ["S"]

tegn_kart(ENGEN, RUTER, KANTER)


# ---------- HELTEN ----------
# Helten er 16 piksler bred og 24 piksler høy.
# treffboks=(2, 16, 12, 8) betyr at bare føttene kan krasje i ting:
# en firkant som starter 2 piksler inn og 16 piksler ned i bildet,
# og som er 12 piksler bred og 8 piksler høy.

helt = Figur("helt_ned_1", 5 * RUTE, 6 * RUTE - 8, treffboks=(2, 16, 12, 8), skygge=True)

FART = 1            # hvor mange piksler helten går hver gang oppdater() kjøres


# ---------- FUNKSJONER ----------

def kan_gaa(figur, x, y):
    """Gir True hvis figuren kan stå på x, y uten å stå i en hindring."""
    # boks() gir treffboksen (føttene) slik den ville vært hvis figuren sto på x, y
    venstre, topp, bredde, hoyde = figur.boks(x, y)

    # OPPGAVE 5: Sjekk alle fire hjørnene av føttene, ikke bare midten.
    # Nå sjekker vi bare ett punkt: midten av føttene
    hjorner = [(venstre + bredde / 2, topp + hoyde / 2)]

    for punkt in hjorner:
        rute = rute_ved(punkt[0], punkt[1])     # hvilket tegn i kartet ligger her?
        if rute in HINDRINGER:
            return False
    return True


def gaa():
    """Flytter helten med piltastene."""
    dx = 0          # hvor mye helten skal flytte seg mot høyre (minus = venstre)
    dy = 0          # hvor mye helten skal flytte seg nedover (minus = oppover)

    fart = FART
    # OPPGAVE 6: Hold inne shift for å løpe dobbelt så fort.
    pass

    if tast_holdes("opp"):
        dy = -fart
    # OPPGAVE 1: Få helten til å gå ned, til venstre og til høyre.
    pass

    # Hvor vil helten stå etterpå?
    ny_x = helt.x + dx
    ny_y = helt.y + dy

    # OPPGAVE 2: Hold helten innenfor skjermen.
    pass

    # OPPGAVE 3: Flytt helten bare hvis han kan gå dit (bruk kan_gaa).
    helt.x = ny_x
    helt.y = ny_y


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Denne funksjonen kjøres 60 ganger i sekundet, helt til spillet lukkes.
    gaa()


start(tittel="Eventyret – steg 1")

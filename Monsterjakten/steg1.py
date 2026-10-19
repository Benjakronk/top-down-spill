# =====================================================================
#  MONSTERJAKTEN – STEG 1: Kart og rutebevegelse
# =====================================================================
#
#  I dag lager du: et kart med gress, sti, vann, busker og steiner,
#  og en helt som går rundt på kartet én rute om gangen – akkurat som
#  i de gamle Game Boy-spillene.
#
#  Taster:  piltastene = gå
#
#  Nytt i dag:
#   - spill-løkka: funksjonen oppdater() kjøres 60 ganger i sekundet
#   - koordinater: x er piksler bortover, y er piksler nedover
#   - ruter: skjermen er 15 × 10 ruter, og hver rute er 16 × 16 piksler
#   - global: når en funksjon skal ENDRE en variabel som ligger utenfor
#
#  Oppgavene står i koden som  # OPPGAVE 1,  # OPPGAVE 2  osv.
#  Gjør dem i rekkefølge, og kjør spillet ofte for å se hva som skjer!
# =====================================================================

from spillmotor import *

# ---------- KARTET ----------
# Kartet er en liste med tekst. Hvert tegn er én rute på 16 × 16 piksler.
# Det er 15 tegn bortover (kolonne 0–14) og 10 linjer nedover (rad 0–9).

KART = [
    "b.,....=....,.b",
    "b...,..=..s...b",
    "b.~~~..=.....,b",
    "b.~~~~.====...b",
    "b..~~....,=...b",
    ".......====.s..",
    "b.s....=......b",
    "b...,..=...~~.b",
    "b..,...=...~~,b",
    "b......=......b",
]

# Hvilket bilde hvert tegn skal ha. En liste med bilder gir en animert rute.
RUTER = {
    ".": "gress_flate",     # gress_flate og sti_flate er store bilder (mønstre):
    ",": "gress_2",         # hver rute viser sin egen bit, så rutenettet ikke synes
    "=": "sti_flate",
    "~": ["vann_flate_1", "vann_flate_2", "vann_flate_3"],
    "b": "busk",
    "s": "stein",
}

# Myke kanter der stien og vannet møter gresset
KANTER = {
    "=": ("stikant", ".,bs"),
    "~": ("vannkant", ".,bs"),
}

# Ruter som helten IKKE kan gå på
HINDRINGER = ["~", "b", "s"]

tegn_kart(KART, RUTER, KANTER)


# ---------- HELTEN ----------
# Helten er 16 piksler bred og 24 piksler høy. Føttene skal stå i ruta,
# så hodet stikker 8 piksler opp i ruta over. Derfor står det  - 8  bak y.
#
#     x = kolonne * RUTE          y = rad * RUTE - 8

# OPPGAVE 1: Flytt helten så den starter på stien midt på kartet: kolonne 7, rad 5.
helt = Figur("helt_ned_1", 0 * RUTE, 0 * RUTE - 8, skygge=True)

# Variabler som husker hva helten holder på med
steg_igjen = 0      # hvor mange piksler helten har igjen av steget sitt (0 = står stille)
dx = 0              # retning bortover:  1 = høyre, -1 = venstre, 0 = ingen av dem
dy = 0              # retning nedover:   1 = ned,   -1 = opp,     0 = ingen av dem


# ---------- FUNKSJONER ----------

def rute_under_fotene(x, y):
    """Gir tegnet i kartet under føttene til helten, hvis helten står på x, y."""
    # Føttene er 8 piksler inn fra venstre og 16 piksler ned fra toppen av bildet
    return rute_ved(x + 8, y + 16)


def kan_ga_til(x, y):
    """Gir True hvis helten kan stå på x, y, og False hvis noe er i veien."""
    rute = rute_under_fotene(x, y)

    # OPPGAVE 4: Helten skal ikke kunne gå på vann, busker eller steiner.
    #            Hvis rute er en av HINDRINGER, skal funksjonen gi False.
    pass

    # OPPGAVE 5: Helten skal ikke kunne gå ut av skjermen.
    #            Utenfor kartet gir rute_ved() verdien None.
    pass

    return True


# ---------- SPILL-LØKKA ----------
# oppdater() kjøres 60 ganger i sekundet. Hver gang flytter vi helten litt.

def oppdater():
    # global: vi skal ENDRE disse variablene inni funksjonen, ikke bare lese dem.
    global steg_igjen, dx, dy

    # --- Helten er midt i et steg: gå én piksel videre ---
    if steg_igjen > 0:
        # OPPGAVE 2: Få helten til å gli. Flytt helten dx piksler bortover og
        #            dy piksler nedover, og tell steg_igjen ned med 1.
        pass
        return      # ferdig for dette bildet

    # --- Helten står stille i en rute: hvilken piltast holdes nede? ---
    dx = 0
    dy = 0
    if tast_holdes("hoyre"):
        dx = 1
    # OPPGAVE 3: Gjør ferdig: venstre, opp og ned (bruk elif).
    pass

    # Ingen piltast? Da står helten stille.
    if dx == 0 and dy == 0:
        return

    # Hvor havner helten etter ett helt steg (16 piksler)?
    ny_x = helt.x + dx * RUTE
    ny_y = helt.y + dy * RUTE

    if kan_ga_til(ny_x, ny_y):
        steg_igjen = RUTE           # start et nytt steg på 16 piksler
    else:
        # OPPGAVE 6: Noe er i veien! Spill lyden "bump", og la helten trampe
        #            på stedet i ett steg: dx og dy blir 0, steg_igjen blir RUTE.
        pass


start(tittel="Monsterjakten")

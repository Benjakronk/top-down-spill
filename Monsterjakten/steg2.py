# =====================================================================
#  MONSTERJAKTEN – STEG 2: Animasjon, by og sti
# =====================================================================
#
#  I dag lager du: en liten by der husene er bygget av fliser, og en sti
#  med trær og høyt gress. Helten går mellom byen og stien, ser i riktig
#  retning og beveger beina når den går. Hvert kart har sin egen musikk.
#
#  Taster:  piltastene = gå
#
#  Nytt i dag:
#   - retning lagret som tekst: "opp", "ned", "venstre", "hoyre"
#   - bildenavn som settes sammen:  "helt_" + retning + "_1"
#   - animasjon med figur.animer([...], fart)
#   - flere kart, og hus og trær bygget av fliser (flere ruter sammen)
#   - overgang(funksjon): skjermen toner ut, funksjonen kjøres, og skjermen toner inn
#
#  Fra steg 1 har du: kartet, rutebevegelsen, hindringer og bump.
# =====================================================================

from spillmotor import *

# ---------- KARTENE ----------
# Nye tegn:  ^ = veien ut av byen (til stien)   v = veien ned fra stien (til byen)
#            k = skilt   p = postkasse   g = gjerde   c = kantstein   " = høyt gress
#            {} over [] = et tre (fire ruter)     qr over xy = en gran     f = blomsterbed
#            tu over hi = en bjørk
#            Husene er bygget av fliser – se HUSBYGGESETTET under RUTER_UTE.

KART_BYEN = [
    ".7809.*^.RTTTTY",
    ".1223..=.FUGGUH",
    "f(Id)..=*VBBBBN",
    "p<#e>..=.jm!lmn",
    ".,.=====.JMMLMP",
    # OPPGAVE 1: Bygg hvilehuset av fliser i kolonne 1–5, rad 5–8 (de fire radene
    #            under). Se hvilehuset i HUSBYGGESETTET under RUTER_UTE, og bytt ut
    #            punktum nr. 2–6 i hver rad med flisene. Hver rad skal fortsatt ha 15 tegn.
    ".......=======.",
    ".......=..*..{}",
    ".......=.k...[]",
    ".......=...~~~~",
    "b...====..~~~~~",
]

KART_STIEN = [
    "{}{}{}.c.{}{}{}",
    "[][][].=.[][][]",
    "{}b.k..=...qr{}",
    '[]"""".=.,.xy[]',
    '{}"""".=...tu{}',
    "[].,*..=..*hi[]",
    '{}cccc.="""""{}',
    '[]..,..="""""[]',
    '{}.....="""""{}',
    "[]...,.v....b[]",
]

RUTER_UTE = {
    # natur. gress_flate, sti_flate og vann_flate_1..3 er store bilder (mønstre): hver rute viser sin egen bit,
    # så rutenettet ikke synes. Det samme gjelder kantstein_rad og tak_gronn_o_rad, og trærne (tre_ov,
    # tre_oh, tre_nv, tre_nh): de har tre varianter, så trær ved siden av hverandre blir litt ulike.
    ".": "gress_flate", ",": "gress_2", "*": ["blomster_1", "blomster_2", "blomster_3"],
    "=": "sti_flate", "^": "sti_flate", "v": "sti_flate",
    "~": ["vann_flate_1", "vann_flate_2", "vann_flate_3"], '"': "hoyt_gress",
    "b": "busk", "s": "stein", "k": "skilt", "p": "postkasse", "g": "gjerde", "c": "kantstein_rad",
    "f": "blomsterbed",
    "{": "tre_ov", "}": "tre_oh", "[": "tre_nv", "]": "tre_nh",
    "q": "gran_ov", "r": "gran_oh", "x": "gran_nv", "y": "gran_nh",
    "t": "bjork_ov", "u": "bjork_oh", "h": "bjork_nv", "i": "bjork_nh",
    # rødt tak (hjemmet)
    "7": "tak_rod_ov", "8": "tak_rod_o", "9": "tak_rod_oh", "0": "tak_rod_pipe",
    "1": "tak_rod_nv", "2": "tak_rod_n", "3": "tak_rod_nh",
    # grønt tak (hvilehuset)
    "Q": "tak_gronn_ov", "W": "tak_gronn_o_rad", "E": "tak_gronn_oh",
    "Z": "tak_gronn_nv", "X": "tak_gronn_n", "C": "tak_gronn_nh",
    # grått tak (laben)
    "R": "tak_gra_ov", "T": "tak_gra_o", "Y": "tak_gra_oh",
    "F": "tak_gra_v", "G": "tak_gra_m", "H": "tak_gra_h", "U": "tak_gra_vindu",
    "V": "tak_gra_nv", "B": "tak_gra_n", "N": "tak_gra_nh",
    # hvit vegg: øvre rad og nedre rad
    "(": "vegg_hvit_o_v", "_": "vegg_hvit_o", ")": "vegg_hvit_o_h",
    "I": "vindu_hvit", "d": "dor_hvit_o", "o": "glassdor_hvit_o", "+": "skilt_hvil",
    "<": "vegg_hvit_v", "-": "vegg_hvit", ">": "vegg_hvit_h",
    "#": "vegg_hvit_blomst", "e": "dor_hvit", "O": "glassdor_hvit",
    # labvegg: øvre rad og nedre rad
    "j": "vegg_lab_o_v", "m": "vegg_lab_o", "n": "vegg_lab_o_h", "%": "vindu_lab",
    "!": "skilt_lab", "l": "dor_lab_o",
    "J": "vegg_lab_v", "M": "vegg_lab", "P": "vegg_lab_h", "L": "dor_lab",
}
# HUSBYGGESETTET: et hus er tak (2 rader) og vegg (2 rader). Gjør det bredere ved å
# gjenta midten. Døra er to ruter høy: den øverste (d, o, l) er vegg, den nederste
# (e, O, L) er der helten skal gå inn (dørene er låst til neste steg).
#     hjemmet      hvilehuset     laben
#     "7809"       "QWWWE"        "RTTTTY"
#     "1223"       "ZXXXC"        "FUGGUH"
#     "(Id)"       "(I+o)"        "VBBBBN"
#     "<#e>"       "<#-O>"        "jm!lmn"
#                                 "JMMLMP"

# Myke kanter der stien og vannet møter gresset, og skyggene fra husene og trærne.
# Står det en liste, får ruta flere kanter. De tegnes i den rekkefølgen de står i.
# HUSTEGN er flisene husene er bygget av. E og C mangler: de skrå hjørnene på valmtaket har sin egen skygge
# (E har den tegnet inn, og gresset til høyre for C får valmskygge).
HUSTEGN = "7890123QWZXRTYFGHUVBN(_)Id+o<->#jmn%!lJMPeOL"
NATUR = '.,"*bskpgcf{}[]qrxytuhi'                              # gress, busker, trær og annet ute
GRESSKANT = [("husskygge", HUSTEGN), ("valmskygge", "C"), ("treskygge_v", "[xh"), ("treskygge_h", "]yi")]
STIKANT = [("stikant", NATUR), ("husskygge_sti", HUSTEGN)]
KANTER_UTE = {
    ".": GRESSKANT, ",": GRESSKANT, "*": GRESSKANT,
    "=": STIKANT, "^": STIKANT, "v": STIKANT,
    "~": ("vannkant", NATUR + "="),
    # trær i rader: kronen til treet under dekker stammen til treet over
    "[": ("tre_topp_v", "{"), "]": ("tre_topp_h", "}"),
    "{": ("trekrone_v", "["), "}": ("trekrone_h", "]"),
    # kantsteinen er en sammenhengende steinkant med avrundet ende der naboen ikke er kantstein
    "c": ("kantstein", NATUR.replace("c", "") + "=^v"),
}

# Ruter som helten IKKE kan gå på. list("abc") blir ["a", "b", "c"].
HINDRINGER = (list("~bskpgcf{}[]qrxytuhi")
              + list("7890123QWEZXCRTYFGHUVBN")         # takene
              + list("(_)Id+o<->#jmn%!lJMP")            # veggene
              + list("eOL"))                            # dørene (låst i dag)


# ---------- HELTEN ----------
helt = Figur("helt_ned_1", 7 * RUTE, 5 * RUTE - 8, skygge=True)

steg_igjen = 0      # hvor mange piksler helten har igjen av steget sitt (0 = står stille)
dx = 0              # retning bortover:  1 = høyre, -1 = venstre, 0 = ingen av dem
dy = 0              # retning nedover:   1 = ned,   -1 = opp,     0 = ingen av dem
retning = "ned"     # hvilken vei helten ser: "opp", "ned", "venstre" eller "hoyre"

sted = "byen"       # hvilket kart vi er på: "byen" eller "stien"


# ---------- KARTFUNKSJONER ----------

def bygg_byen():
    global sted
    sted = "byen"
    tegn_kart(KART_BYEN, RUTER_UTE, KANTER_UTE)
    spill_musikk("by")


def bygg_stien():
    global sted
    sted = "stien"
    tegn_kart(KART_STIEN, RUTER_UTE, KANTER_UTE)
    # OPPGAVE 2: Spill musikken "sti" når helten kommer til stien.
    pass


def gaa_til_stien():
    """Kjøres midt i overgangen, mens skjermen er svart."""
    bygg_stien()
    helt.y = 8 * RUTE - 8       # nederst på stien (x er den samme som før)


def gaa_til_byen():
    """Kjøres midt i overgangen, mens skjermen er svart."""
    # OPPGAVE 3: Bygg byen, og sett helten i rad 1 (øverst i byen).
    pass


# ---------- HELTEN GÅR ----------

def rute_under_fotene(x, y):
    """Gir tegnet i kartet under føttene til helten, hvis helten står på x, y."""
    return rute_ved(x + 8, y + 16)


def kan_ga_til(x, y):
    """Gir True hvis helten kan stå på x, y, og False hvis noe er i veien."""
    rute = rute_under_fotene(x, y)
    if rute in HINDRINGER:
        return False
    if rute == None:
        return False
    return True


def ferdig_med_steg():
    """Kjøres hver gang helten er ferdig med et steg og står midt i en rute."""
    rute = rute_under_fotene(helt.x, helt.y)
    if rute == "^":
        overgang(gaa_til_stien)
    # OPPGAVE 4: Står helten på en v-rute, skal vi gå til byen.
    pass


# ---------- SPILL-LØKKA ----------

def oppdater():
    global steg_igjen, dx, dy, retning

    # Mens skjermen toner ut og inn, skal ingenting skje.
    if i_overgang():
        return

    # --- Helten er midt i et steg: gå én piksel videre ---
    if steg_igjen > 0:
        helt.x = helt.x + dx
        helt.y = helt.y + dy
        steg_igjen = steg_igjen - 1
        if steg_igjen == 0:
            ferdig_med_steg()
        return

    # --- Helten står stille i en rute: hvilken piltast holdes nede? ---
    dx = 0
    dy = 0
    if tast_holdes("hoyre"):
        dx = 1
        retning = "hoyre"
    elif tast_holdes("venstre"):
        dx = -1
        retning = "venstre"
    elif tast_holdes("opp"):
        dy = -1
        retning = "opp"
    elif tast_holdes("ned"):
        dy = 1
        retning = "ned"

    # Ingen piltast? Da står helten stille.
    if dx == 0 and dy == 0:
        # OPPGAVE 5: Stopp animasjonen (helt.animer(None)), og vis bildet der
        #            helten står stille og ser i riktig retning, f.eks. "helt_opp_1".
        pass
        return

    # OPPGAVE 6: Helten går! Start gang-animasjonen med de fire bildene
    #            "helt_" + retning + "_2", "_3", "_4" og "_1", med fart=8.
    pass

    ny_x = helt.x + dx * RUTE
    ny_y = helt.y + dy * RUTE

    if kan_ga_til(ny_x, ny_y):
        steg_igjen = RUTE
    else:
        spill_lyd("bump")
        # Helten står fast: stopp gang-animasjonen og vis bildet der han står stille
        helt.animer(None)
        helt.bilde = "helt_" + retning + "_1"
        dx = 0
        dy = 0
        steg_igjen = RUTE


# ---------- START ----------
bygg_byen()
start(tittel="Monsterjakten")

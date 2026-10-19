# =====================================================================
#  MONSTERJAKTEN – STEG 3: Hus med innside
# =====================================================================
#
#  I dag kan du gå INN i husene! Hvert hus har sitt eget kart for innsiden:
#  hjemme, laben og hvilehuset. Dørene fører mellom kartene, og dørmatta
#  inne fører ut igjen. Nå har spillet fem kart – i stedet for å skrive en
#  egen funksjon for hvert kart, samler vi alt i én ordbok: KARTENE.
#
#  Taster:  piltastene = gå
#
#  Nytt i dag:
#   - en ordbok med ordbøker:  KARTENE["laben"]["musikk"]  gir "lab"
#   - én funksjon for alle kartene:  bygg_kart(navn)
#   - en dørtabell (DORER): en liste med ordbøker som sier hvor hver dør fører
#   - en for-løkke som leter i en liste og gir (return) det den finner
#   - hver kart har egne tegn: "." er gress ute, men gulv inne
#
#  Fra før har du: kartene, rutebevegelse, animasjon og byen av fliser.
# =====================================================================

from spillmotor import *

# ---------- KARTENE ----------
# Hvert kart er en liste med tekst. Hvert tegn er én rute (16 x 16 piksler).
# Ute (byen og stien):
#   .  ,  *   gress (litt forskjellig)      =   sti       ~   vann      "   høyt gress
#   b  busk     s  stein     k  skilt     p  postkasse     g  gjerde     c  kantstein
#   f  blomsterbed     {} over []  et tre (2 x 2 ruter)     qr over xy  en gran (2 x 2 ruter)
#   tu over hi  en bjørk (2 x 2 ruter)   (inne betyr h noe annet: stol eller krakk)
#   ^  veien ut av byen (til stien)       v  veien ned fra stien (til byen)
#   Husene er bygget av fliser – se HUSBYGGESETTET under RUTER_UTE.
#   Dørene:  e = døra hjemme   L = døra til laben   O = døra til hvilehuset

KART_BYEN = [
    ".7809.*^.RTTTTY",
    ".1223..=.FUGGUH",
    "f(Id)..=*VBBBBN",
    "p<#e>..=.jm!lmn",
    ".,.=====.JMMLMP",
    ".QWWWE.=======.",
    ".ZXXXC.=..*..{}",
    ".(I+o).=.k...[]",
    ".<#-O>.=...~~~~",
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
# (e, O, L) er der helten går inn.
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
HINDRINGER_UTE = (list("~bskpgcf{}[]qrxytuhi")
                  + list("7890123QWEZXCRTYFGHUVBN")         # takene
                  + list("(_)Id+o<->#jmn%!lJMP"))           # veggene (men ikke e, O og L)

# Inne i husene. Alt utenfor rommet er X (mørkt). Øverst står veggen (2 rader).
#   .  ,  gulv      M  dørmatta (gå ut her)      1–9  teppe (i hvilehuset: merket på gulvet)
#   ^  _  vegg (øvre og nedre rad)   w  vindu   p  bilde/plakat   c  klokke
#   Møblene (stor bokstav = øverste rute, liten = nederste):
#   T/t trapp   K/k bokhylle (hjemme), kolbehylle (laben) eller bladhylle (hvilehuset)   B/b bokhylle
#   S/s skap   F/f kjøleskap   Q/q maskin (i hvilehuset: brusautomat)   R/r hylle   Y/y helbredermaskin
#   C pc   P plante   h stol (i hvilehuset: krakk; ute er h en del av bjørka)   v tv
#   [ ] bord   { } benk   < > sofa   ( o ) lyktebordet i laben   ( - ) skranken i hvilehuset

KART_HJEMME = [
    "XX^w^^c^^^w^TXX",
    "XX_K_____FSStXX",
    "XX.k..v..fss,XX",
    "XX...h[]h....XX",
    "XX...........XX",
    "XX...789.....XX",
    "XX...456...<>XX",
    "XX...123.....XX",
    "XXP....M....PXX",
    "XXXXXXXXXXXXXXX",
]

KART_LABEN = [
    "X^^w^^^p^c^w^^X",
    "X_KQ_BB__QK___X",
    "X.kq.bb..qk.C.X",
    "X.............X",
    "X..{}....(o).PX",
    "X.............X",
    "XRRR.......RRRX",
    "Xrrr.......rrrX",
    "XP.....M.....PX",
    "XXXXXXXXXXXXXXX",
]

KART_HVILEHUSET = [
    "XX^pw^^c^^w^^XX",
    "XX_K_Y____Q__XX",
    "XX.k.y....q.CXX",
    "XXP(-------)PXX",
    "XX.........<>XX",
    "XX{}..789.h[]XX",
    "XXh...456...hXX",
    "XXP...123...PXX",
    "XX.....M.....XX",
    "XXXXXXXXXXXXXXX",
]

RUTER_HJEMME = {
    "X": "morkt", ".": "gulv_tre", ",": "gulv_tre_2", "M": "dormatte_tre",
    "^": "innervegg_hjem_o", "_": "innervegg_hjem_n", "w": "innervindu_hjem",
    "p": "veggbilde_hjem", "c": "klokke_hjem", "T": "trapp_o", "t": "trapp_n",
    "K": "bokhylle_o", "k": "bokhylle_n", "[": "bord_v", "]": "bord_h", "h": "stol",
    "v": "tv", "P": "plante", "S": "skap_o", "s": "skap_n", "F": "kjoleskap_o", "f": "kjoleskap_n",
    "<": "sofa_hjem_v", ">": "sofa_hjem_h",
    "7": "teppe_ov", "8": "teppe_o", "9": "teppe_oh", "4": "teppe_v", "5": "teppe_m",
    "6": "teppe_h", "1": "teppe_nv", "2": "teppe_n", "3": "teppe_nh",
}

RUTER_LABEN = {
    "X": "morkt", ".": "gulv_flis", "M": "dormatte_flis",
    "^": "innervegg_lab_o", "_": "innervegg_lab_n", "w": "innervindu_lab", "p": "plakat_lab",
    "c": "klokke_lab",
    "Q": "maskin_o", "q": "maskin_n", "K": "kolbehylle_o", "k": "kolbehylle_n",
    "B": "bokhylle_lab_o", "b": "bokhylle_lab_n", "C": "pc", "R": "reol_o", "r": "reol_n",
    "{": "labbenk_v", "}": "labbenk_h", "P": "plante_flis",
    "(": "lyktebord_v", "o": "lyktebord", ")": "lyktebord_h",
}

RUTER_HVILEHUSET = {
    "X": "morkt", ".": "gulv_hvile", "M": "dormatte_hvile",
    "^": "innervegg_hvile_o", "_": "innervegg_hvile_n", "w": "innervindu_hvile",
    "p": "plakat_hvile", "c": "klokke_hvile",
    "Y": "helbreder_o", "y": "helbreder_n",
    "(": "disk_v", "-": "disk_rad", ")": "disk_h",        # disk_rad er et mønster: hver rute er ulik
    "{": "benk_v", "}": "benk_h", "P": "plante_hvile", "C": "pc_hvile",
    "K": "bladhylle_hvile_o", "k": "bladhylle_hvile_n", "Q": "automat_hvile_o", "q": "automat_hvile_n",
    "h": "krakk_hvile",
    "<": "sofa_v", ">": "sofa_h", "[": "glassbord_v", "]": "glassbord_h",
    "7": "hvileteppe_ov", "8": "hvileteppe_o", "9": "hvileteppe_oh", "4": "hvileteppe_v",
    "5": "hvileteppe_m", "6": "hvileteppe_h", "1": "hvileteppe_nv", "2": "hvileteppe_n",
    "3": "hvileteppe_nh",
}

# Skygge på gulvet langs veggene, og veggene rundt rommet: de tegnes i X-rutene
# som ligger inntil rommet (ROMTEGN er alle tegnene i rommene unntatt X og M).
# Lager du et nytt tegn i rommet, legg det til i ROMTEGN også.
# Skranken og lyktebordet ( - o ) kaster skygge på gulvruta under (mobelskygge).
VEGGTEGN = "^_wpcTtKkQqBbYySF"
ROMTEGN = "^_wpcTtKkQqBbYySsFfRr[]hvP{}()o-C<>.,123456789"
KANTER_INNE = {
    ".": [("inneskygge", VEGGTEGN), ("romskygge", "X"), ("mobelskygge", "(-o)")],
    ",": [("inneskygge", VEGGTEGN), ("romskygge", "X"), ("mobelskygge", "(-o)")],
    "X": [("romkant", ROMTEGN), ("romdor", "M")],
    "^": ("veggkant_o", "X"),
    "_": ("veggkant_n", "X"),
}

# Inne kan helten gå på gulvet, teppet og dørmatta – alt annet er i veien.
HINDRINGER_INNE = list("X^_wpcTtKkQqBbYySsFfRr[]hvP{}()o-C<>")

# Alle kartene i spillet. Hvert kart har sin egen tegneordbok (ruter),
# sine egne kanter, hindringer og musikk.
KARTENE = {
    "byen":       {"kart": KART_BYEN, "ruter": RUTER_UTE, "kanter": KANTER_UTE,
                   "hindringer": HINDRINGER_UTE, "musikk": "by"},
    "stien":      {"kart": KART_STIEN, "ruter": RUTER_UTE, "kanter": KANTER_UTE,
                   "hindringer": HINDRINGER_UTE, "musikk": "sti"},
    "hjemme":     {"kart": KART_HJEMME, "ruter": RUTER_HJEMME, "kanter": KANTER_INNE,
                   "hindringer": HINDRINGER_INNE, "musikk": "by"},
    # OPPGAVE 5: Legg til laben i KARTENE: kartet KART_LABEN, ruter RUTER_LABEN,
    #            kanter KANTER_INNE, hindringer HINDRINGER_INNE og musikken "lab".
    #            Se på "hjemme" rett over.
    # (laben mangler her)
    "hvilehuset": {"kart": KART_HVILEHUSET, "ruter": RUTER_HVILEHUSET, "kanter": KANTER_INNE,
                   "hindringer": HINDRINGER_INNE, "musikk": "hvilehus"},
}

# ---------- DØRENE ----------
# En dør er en rute som fører til et annet kart. Går helten inn på ruta
# (kolonne, rad) i kartet "fra", havner han på (til_kolonne, til_rad) i kartet "til".
# Inne er dørmatta (M) døra ut. Veien mellom byen og stien er også «dører».
DORER = [
    {"fra": "byen", "kolonne": 7, "rad": 0, "til": "stien", "til_kolonne": 7, "til_rad": 8},
    {"fra": "stien", "kolonne": 7, "rad": 9, "til": "byen", "til_kolonne": 7, "til_rad": 1},
    {"fra": "byen", "kolonne": 3, "rad": 3, "til": "hjemme", "til_kolonne": 7, "til_rad": 7},
    {"fra": "hjemme", "kolonne": 7, "rad": 8, "til": "byen", "til_kolonne": 3, "til_rad": 4},
    # OPPGAVE 6: Lag de to dørene til laben: døra i byen (kolonne 12, rad 4) skal føre
    #            til laben (kolonne 7, rad 7), og dørmatta i laben (kolonne 7, rad 8)
    #            skal føre ut til ruta foran døra i byen (kolonne 12, rad 5).
    # (dørene til laben mangler her)
    {"fra": "byen", "kolonne": 4, "rad": 8, "til": "hvilehuset", "til_kolonne": 7, "til_rad": 7},
    {"fra": "hvilehuset", "kolonne": 7, "rad": 8, "til": "byen", "til_kolonne": 4, "til_rad": 9},
]


# ---------- HELTEN ----------
helt = Figur("helt_ned_1", 7 * RUTE, 5 * RUTE - 8, skygge=True)

steg_igjen = 0      # hvor mange piksler helten har igjen av steget sitt (0 = står stille)
dx = 0              # retning bortover:  1 = høyre, -1 = venstre, 0 = ingen av dem
dy = 0              # retning nedover:   1 = ned,   -1 = opp,     0 = ingen av dem
retning = "ned"     # hvilken vei helten ser: "opp", "ned", "venstre" eller "hoyre"

sted = "byen"       # hvilket kart vi er på: "byen", "stien", "hjemme", "laben" eller "hvilehuset"
neste_dor = None    # døra helten skal gå gjennom (se gaa_gjennom)


# ---------- KARTFUNKSJONER ----------

def bygg_kart(navn):
    """Tegner kartet som heter navn (f.eks. "laben") og spiller musikken til kartet."""
    global sted
    sted = navn
    # OPPGAVE 1: Slå opp kartet i KARTENE:  info = KARTENE[navn]
    #            Tegn det med tegn_kart(info["kart"], info["ruter"], info["kanter"]),
    #            og spill musikken info["musikk"]. Slett den midlertidige linja under.
    tegn_kart(KART_BYEN, RUTER_UTE, KANTER_UTE)      # midlertidig: alltid byen


def dor_ved(kolonne, rad):
    """Gir døra på ruta (kolonne, rad) på dette kartet, eller None hvis det ikke er noen dør der."""
    # OPPGAVE 2: Gå gjennom alle dørene i DORER. Hvis dor["fra"] er sted, og
    #            dor["kolonne"] er kolonne og dor["rad"] er rad, skal funksjonen
    #            gi (return) døra.
    pass
    return None


def gaa_gjennom():
    """Kjøres midt i overgangen, mens skjermen er svart: helten går gjennom neste_dor."""
    # OPPGAVE 3: Bygg kartet døra fører til (neste_dor["til"]), og sett helten på
    #            ruta (neste_dor["til_kolonne"], neste_dor["til_rad"]). Husk - 8 på y.
    pass


# ---------- HELTEN GÅR ----------

def rute_under_fotene(x, y):
    """Gir tegnet i kartet under føttene til helten, hvis helten står på x, y."""
    return rute_ved(x + 8, y + 16)


def kan_ga_til(x, y):
    """Gir True hvis helten kan stå på x, y, og False hvis noe er i veien."""
    rute = rute_under_fotene(x, y)
    # OPPGAVE 4: Inne er "." gulv og "X" mørke – ute er "." gress. Bruk derfor
    #            hindringene til kartet vi er på: KARTENE[sted]["hindringer"].
    if rute in HINDRINGER_UTE:
        return False
    if rute == None:
        return False
    return True


def ferdig_med_steg():
    """Kjøres hver gang helten er ferdig med et steg og står midt i en rute."""
    global neste_dor
    # Står helten på en dør? Da går han gjennom den til et annet kart.
    # (helt.x // RUTE er kolonnen. // deler og runder ned.)
    dor = dor_ved(helt.x // RUTE, (helt.y + 8) // RUTE)
    if dor != None:
        neste_dor = dor
        if dor["fra"] != "stien" and dor["til"] != "stien":
            spill_lyd("dor")
        overgang(gaa_gjennom)


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
        helt.animer(None)
        helt.bilde = "helt_" + retning + "_1"
        return

    # Helten går: start gang-animasjonen
    helt.animer(["helt_" + retning + "_2", "helt_" + retning + "_3",
                 "helt_" + retning + "_4", "helt_" + retning + "_1"], fart=8)

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
bygg_kart("byen")
# TEST AV OPPGAVE 1: ta bort # foran linja under. Da starter spillet hjemme i stedet for
# i byen – men bare hvis bygg_kart() bruker KARTENE. (Sett # foran igjen etterpå.)
# bygg_kart("hjemme")
start(tittel="Monsterjakten")

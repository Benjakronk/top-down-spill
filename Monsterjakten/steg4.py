# =====================================================================
#  MONSTERJAKTEN – STEG 4: Folk og tekstbokser
# =====================================================================
#
#  I dag lager du: folk som står i byen, i husene og på stien. Gå bort til en
#  person, se mot personen og trykk MELLOMROM, så sier personen noe i
#  en tekstboks nederst på skjermen. Personen snur seg mot deg.
#
#  Taster:  piltastene = gå    MELLOMROM = snakk / neste linje
#
#  Nytt i dag:
#   - en liste med dictionaries: hver person er en dictionary
#   - person["figur"]: en figur kan lagres i en dictionary
#   - en funksjon som gir to verdier:  x, y = ruta_foran()
#   - tast_trykket(): bare i det øyeblikket tasten trykkes ned
#   - Tekst-figurer og en tekstboks som vises og skjules (.synlig)
#
#  Fra før har du: byen, stien og husene med innside (KARTENE og DORER), rutebevegelse og animasjon.
#
#  Folk rusler nå rolig rundt (ferdig kode under FOLK SOM RUSLER).
# =====================================================================

import random
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
    "laben":      {"kart": KART_LABEN, "ruter": RUTER_LABEN, "kanter": KANTER_INNE,
                   "hindringer": HINDRINGER_INNE, "musikk": "lab"},
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
    {"fra": "byen", "kolonne": 12, "rad": 4, "til": "laben", "til_kolonne": 7, "til_rad": 7},
    {"fra": "laben", "kolonne": 7, "rad": 8, "til": "byen", "til_kolonne": 12, "til_rad": 5},
    {"fra": "byen", "kolonne": 4, "rad": 8, "til": "hvilehuset", "til_kolonne": 7, "til_rad": 7},
    {"fra": "hvilehuset", "kolonne": 7, "rad": 8, "til": "byen", "til_kolonne": 4, "til_rad": 9},
]


# ---------- FOLK ----------
# Hver person er en dictionary, akkurat som fiendene i teksteventyret.
#   "bilde"      starten på bildenavnet: "mor" gir mor_ned, mor_opp, mor_venstre, mor_hoyre
#   "kart"       hvilket kart personen står på: "byen", "stien", "hjemme" ...
#   "star_stille"  (valgfri) personen rusler ikke rundt
#   "kolonne", "rad"  hvilken rute personen står i
#   "retning"    hvilken vei personen ser
#   "replikker"  det personen sier, én tekstboks om gangen

folk = [
    {"bilde": "mor", "kart": "hjemme", "kolonne": 10, "rad": 4, "retning": "venstre",
     "replikker": ["MOR: God morgen! Professoren venter på deg i laben.",
                   "MOR: Laben er det store huset med grått tak, rett over gata."]},
    {"bilde": "professor", "kart": "laben", "kolonne": 10, "rad": 3, "retning": "ned",
     "replikker": ["PROFESSOR: Ville monstre gjemmer seg i det høye gresset på stien.",
                   "PROFESSOR: Gjør dem svake først, så er de lettere å fange!"]},
    {"bilde": "vert", "kart": "hvilehuset", "kolonne": 7, "rad": 2, "retning": "ned", "star_stille": True,
     "replikker": ["VERT: Velkommen til hvilehuset!",
                   "VERT: Her kan monstrene dine hvile seg når de er slitne."]},
    {"bilde": "gutt", "kart": "stien", "kolonne": 9, "rad": 3, "retning": "venstre",
     "replikker": ["GUTT: Hørte du det raslet i gresset?",
                   "GUTT: Det er monstre der inne!"]},
]

# OPPGAVE 1: Legg til en jente i byen: kolonne 10, rad 8, som ser mot høyre
#            (mot vannet). Bruk folk.append({...}) og finn på hva hun sier.
pass

# Det som står på skiltene, for hvert kart som har skilt
SKILT = {"byen": ["LILLEVIK", "Hvilehuset: grønt tak.  Laben: grått tak."],
         "stien": ["RUTE 1", "Nord: Store skogen (stengt).  Sør: Lillevik."]}

# Hvilken vei en person må se for å se på helten
MOTSATT = {"opp": "ned", "ned": "opp", "venstre": "hoyre", "hoyre": "venstre"}


# ---------- HELTEN ----------
helt = Figur("helt_ned_1", 7 * RUTE, 5 * RUTE - 8, skygge=True)

steg_igjen = 0      # hvor mange piksler helten har igjen av steget sitt (0 = står stille)
dx = 0              # retning bortover:  1 = høyre, -1 = venstre, 0 = ingen av dem
dy = 0              # retning nedover:   1 = ned,   -1 = opp,     0 = ingen av dem
retning = "ned"     # hvilken vei helten ser: "opp", "ned", "venstre" eller "hoyre"

sted = "byen"       # hvilket kart vi er på: "byen", "stien", "hjemme", "laben" eller "hvilehuset"
neste_dor = None    # døra helten skal gå gjennom (se gaa_gjennom)
ting = []           # figurene som hører til kartet (folkene)


# ---------- TEKSTBOKSEN ----------
TEKSTFARGE = "#484858"
TEKSTSKYGGE = "#d0d0d8"

tekstboks = Figur("tekstboks", 4, 114, lag=3)
tekst = Tekst("", 12, 121, farge=TEKSTFARGE, skygge=TEKSTSKYGGE, maks_bredde=210)
tekstboks.synlig = False
tekst.synlig = False

samtale = []        # replikkene som venter på å bli vist
prater = False      # True mens helten prater med noen


# ---------- KARTFUNKSJONER ----------

def lag_folk():
    """Lager en figur for hver person som står på dette kartet."""
    for person in folk:
        if person["kart"] == sted:
            # OPPGAVE 2: Lag en figur for personen og legg den i person["figur"]
            #            og i lista ting. Bildet er f.eks. "mor_ned", og personen
            #            står i ruta (kolonne, rad) – akkurat som helten (husk - 8).
            pass


def fjern_ting():
    """Fjerner alle figurene som hører til kartet vi går fra."""
    for figur in ting:
        figur.fjern()
    ting.clear()
    for person in folk:
        person["steg_igjen"] = 0      # folk som var midt i et steg, starter på nytt


def bygg_kart(navn):
    """Tegner kartet som heter navn (f.eks. "laben"), med folk og musikk."""
    global sted
    sted = navn
    fjern_ting()
    info = KARTENE[navn]
    tegn_kart(info["kart"], info["ruter"], info["kanter"])
    lag_folk()
    spill_musikk(info["musikk"])


def dor_ved(kolonne, rad):
    """Gir døra på ruta (kolonne, rad) på dette kartet, eller None hvis det ikke er noen dør der."""
    for dor in DORER:
        if dor["fra"] == sted and dor["kolonne"] == kolonne and dor["rad"] == rad:
            return dor
    return None


def gaa_gjennom():
    """Kjøres midt i overgangen, mens skjermen er svart: helten går gjennom neste_dor."""
    bygg_kart(neste_dor["til"])
    helt.x = neste_dor["til_kolonne"] * RUTE
    helt.y = neste_dor["til_rad"] * RUTE - 8


# ---------- FOLK OG PRAT ----------

def person_ved(x, y):
    """Gir personen som står på x, y på dette kartet, eller None hvis ingen står der."""
    # OPPGAVE 3: Gå gjennom alle i folk. Hvis personen er på dette kartet (sted),
    #            og person["kolonne"] * RUTE er x, og person["rad"] * RUTE - 8 er y,
    #            skal funksjonen gi (return) personen.
    pass
    return None


def vis_tekst(ny_tekst):
    """Viser en tekst i tekstboksen."""
    tekst.tekst = ny_tekst
    tekstboks.synlig = True
    tekst.synlig = True


def skjul_tekst():
    """Skjuler tekstboksen."""
    tekstboks.synlig = False
    tekst.synlig = False


def si(replikker):
    """Starter en samtale: replikkene vises én om gangen."""
    global samtale, prater
    samtale = list(replikker)       # en kopi, så lista til personen ikke blir tom
    prater = True
    neste_replikk()


def neste_replikk():
    """Viser neste replikk, eller avslutter samtalen hvis det ikke er flere."""
    global prater
    # OPPGAVE 4: Er det flere replikker igjen i samtale? Da skal den første vises
    #            (vis_tekst(samtale.pop(0))) og lyden "tekst_pip" spilles.
    #            Ellers skal tekstboksen skjules og prater bli False.
    pass


def ruta_foran():
    """Gir x og y for ruta helten ser mot."""
    x = helt.x
    y = helt.y
    if retning == "hoyre":
        x = x + RUTE
    elif retning == "venstre":
        x = x - RUTE
    elif retning == "opp":
        y = y - RUTE
    elif retning == "ned":
        y = y + RUTE
    return x, y


def snakk():
    """Kjøres når spilleren trykker mellomrom på kartet."""
    x, y = ruta_foran()

    # Står det en skranke foran helten? Da snakker vi med den som står bak:
    # vi går ett steg til i samme retning.
    if sted == "hvilehuset" and rute_under_fotene(x, y) in ["(", "-", ")"]:
        x = x + (x - helt.x)
        y = y + (y - helt.y)

    stopp_folk_ved(x, y)        # står det noen der, stopper de opp

    # Står det et skilt foran helten? Da leser vi det som står på skiltet på dette kartet.
    if rute_under_fotene(x, y) == "k" and sted in SKILT:
        si(SKILT[sted])

    person = person_ved(x, y)

    # OPPGAVE 5: Står det en person foran helten (person er ikke None)?
    #            Da skal du starte en samtale med replikkene til personen.
    pass

    # OPPGAVE 6: Personen skal snu seg mot helten. Bytt bildet til figuren til
    #            personen. Bruk MOTSATT: ser helten "opp", må personen se "ned".
    pass


# ---------- FOLK SOM RUSLER ----------
# Folk går rolig rundt i nærheten av der de startet, én rute om gangen – akkurat
# som helten. Hver person husker selv hvor mye den har igjen av steget sitt.
# (Denne delen er ferdig. Les den gjerne – den bruker de samme ideene som helten.)

# Hvor mange piksler en person flytter seg bortover og nedover per bilde i hver retning
STEG_X = {"opp": 0, "ned": 0, "venstre": -1, "hoyre": 1}
STEG_Y = {"opp": -1, "ned": 1, "venstre": 0, "hoyre": 0}


def helten_er_ved(x, y):
    """True hvis helten står på x, y – eller er på vei til eller fra den ruta."""
    mal_x = helt.x + dx * steg_igjen        # der helten står når steget er ferdig
    mal_y = helt.y + dy * steg_igjen
    if x == mal_x and y == mal_y:
        return True
    if steg_igjen > 0 and x == mal_x - dx * RUTE and y == mal_y - dy * RUTE:
        return True                         # ruta helten går fra
    return False


def person_kan_ga_til(person, kolonne, rad):
    """True hvis personen kan gå til ruta (kolonne, rad)."""
    # Ikke lenger enn 1 rute fra startplassen (abs gjør minus til pluss)
    if abs(kolonne - person["hjem_kolonne"]) > 1 or abs(rad - person["hjem_rad"]) > 1:
        return False
    x = kolonne * RUTE
    y = rad * RUTE - 8
    rute = rute_under_fotene(x, y)
    if "star_stille" in person:
        return False
    if rute == None or rute in KARTENE[sted]["hindringer"] or rute == '"':
        return False
    if dor_ved(kolonne, rad) != None:       # folk går ikke ut gjennom dørene
        return False
    if person_ved(x, y) != None or helten_er_ved(x, y):
        return False
    return True


def stopp_folk_ved(x, y):
    """En person som står på x, y, stopper opp og venter en stund (helten vil prate)."""
    for person in folk:
        if person["kart"] == sted and "figur" in person:
            if person["kolonne"] * RUTE == x and person["rad"] * RUTE - 8 == y:
                person["figur"].animer(None)
                person["vent"] = 240            # står stille i 4 sekunder


def oppdater_folk():
    """Kjøres 60 ganger i sekundet: hver person på kartet venter, snur seg eller går."""
    for person in folk:
        if person["kart"] != sted or "figur" not in person:
            continue                            # continue: hopp videre til neste person
        figur = person["figur"]
        if "hjem_kolonne" not in person:        # første gang: husk startplassen
            person["hjem_kolonne"] = person["kolonne"]
            person["hjem_rad"] = person["rad"]
            person["steg_igjen"] = 0
            person["vent"] = random.randint(30, 150)

        # Midt i et steg: gå én piksel videre
        if person["steg_igjen"] > 0:
            figur.x = figur.x + STEG_X[person["retning"]]
            figur.y = figur.y + STEG_Y[person["retning"]]
            person["steg_igjen"] = person["steg_igjen"] - 1
            if person["steg_igjen"] == 0:
                figur.animer(None)
                figur.bilde = person["bilde"] + "_" + person["retning"]
            else:
                figur.animer([person["bilde"] + "_" + person["retning"] + "_2",
                              person["bilde"] + "_" + person["retning"] + "_3",
                              person["bilde"] + "_" + person["retning"] + "_4",
                              person["bilde"] + "_" + person["retning"] + "_1"], fart=8)
            continue

        # Står stille: vent litt før personen gjør noe
        person["vent"] = person["vent"] - 1
        if person["vent"] > 0:
            continue
        person["vent"] = random.randint(60, 200)
        if "star_stille" in person:
            continue                            # står stille og ser samme vei hele tiden

        # Snu seg i en tilfeldig retning ...
        ny_retning = random.choice(["opp", "ned", "venstre", "hoyre"])
        person["retning"] = ny_retning
        figur.bilde = person["bilde"] + "_" + ny_retning

        # ... og 2 av 3 ganger: prøv å gå ett steg dit
        if random.randint(1, 3) > 1:
            kolonne = person["kolonne"] + STEG_X[ny_retning]
            rad = person["rad"] + STEG_Y[ny_retning]
            if person_kan_ga_til(person, kolonne, rad):
                person["kolonne"] = kolonne     # personen «tar» ruta med en gang,
                person["rad"] = rad             # så ingen andre går dit samtidig
                person["steg_igjen"] = RUTE


# ---------- HELTEN GÅR ----------

def rute_under_fotene(x, y):
    """Gir tegnet i kartet under føttene til helten, hvis helten står på x, y."""
    return rute_ved(x + 8, y + 16)


def kan_ga_til(x, y):
    """Gir True hvis helten kan stå på x, y, og False hvis noe er i veien."""
    rute = rute_under_fotene(x, y)
    if rute in KARTENE[sted]["hindringer"]:
        return False
    if rute == None:
        return False
    if person_ved(x, y) != None:        # folk er også i veien
        return False
    return True


def ferdig_med_steg():
    """Kjøres hver gang helten er ferdig med et steg og står midt i en rute."""
    global neste_dor
    # Står helten på en dør? Da går han gjennom den til et annet kart.
    dor = dor_ved(helt.x // RUTE, (helt.y + 8) // RUTE)
    if dor != None:
        neste_dor = dor
        if dor["fra"] != "stien" and dor["til"] != "stien":
            spill_lyd("dor")
        overgang(gaa_gjennom)
        return

    rute = rute_under_fotene(helt.x, helt.y)


# ---------- SPILL-LØKKA ----------

def oppdater():
    global steg_igjen, dx, dy, retning

    # Mens skjermen toner ut og inn, skal ingenting skje.
    if i_overgang():
        return

    # --- Helten prater: mellomrom viser neste replikk, ellers skjer ingenting ---
    if prater:
        if tast_trykket("mellomrom"):
            neste_replikk()
        return

    # --- Folk rusler rundt ---
    oppdater_folk()

    # --- Helten er midt i et steg: gå én piksel videre ---
    if steg_igjen > 0:
        helt.x = helt.x + dx
        helt.y = helt.y + dy
        steg_igjen = steg_igjen - 1
        if steg_igjen == 0:
            ferdig_med_steg()
        return

    # --- Helten står stille: vil spilleren snakke? ---
    if tast_trykket("mellomrom"):
        snakk()
        return

    # --- Hvilken piltast holdes nede? ---
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
start(tittel="Monsterjakten")

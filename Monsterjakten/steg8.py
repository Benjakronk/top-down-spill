# =====================================================================
#  MONSTERJAKTEN – STEG 8: Fange monstre og laget
# =====================================================================
#
#  I dag lager du: fangstlykter! Kast en lykt på et vilt monster, se den
#  vugge, og håp at monsteret blir i lykta. Jo mindre liv monsteret har,
#  jo lettere er det å fange. Monstrene du fanger, kommer med i laget
#  ditt, og i kampen kan du bytte hvem som kjemper.
#
#  Taster:  piltastene = gå / flytt pila    MELLOMROM = snakk / velg
#           ESC = tilbake fra lagmenyen
#
#  Nytt i dag:
#   - laget er en liste med dictionaries:  laget[0]["navn"]
#   - append(): et fanget monster legges til i laget
#   - en dictionary som teller ting:  sekk["fangstlykt"]
#   - en for-løkke med nummer:  for nr in range(len(laget))
#   - sannsynlighet: jo mindre liv, jo større sjanse
#   - is: er det AKKURAT det samme monsteret?
#
#  Fra før har du: byen, stien og husene, folk, møter, kamp med meny, typer og HP-stolper.
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
    {"bilde": "jente", "kart": "byen", "kolonne": 10, "rad": 8, "retning": "hoyre",
     "replikker": ["JENTE: Jeg så en vott som fløy over vannet i går!",
                   "JENTE: Kanskje det var et monster?"]},
]

# Det som står på skiltene, for hvert kart som har skilt
SKILT = {"byen": ["LILLEVIK", "Hvilehuset: grønt tak.  Laben: grått tak."],
         "stien": ["RUTE 1", "Nord: Store skogen (stengt).  Sør: Lillevik."]}

# Hvilken vei en person må se for å se på helten
MOTSATT = {"opp": "ned", "ned": "opp", "venstre": "hoyre", "hoyre": "venstre"}


# ---------- MONSTRE ----------
# Alle monsterartene i spillet. Nøkkelen er starten på bildenavnet:
# "tanngris" har bildene tanngris_foran, tanngris_bak og tanngris_ikon.
#   "navn"    navnet som vises (kort, så det får plass i boksen)
#   "type"    ild, gress, vann, lyn, stein eller normal
#   "liv"     hvor mye liv arten har på nivå 0 (den får 2 ekstra per nivå)
#   "styrke"  hvor hardt den slår på nivå 0 (den får 1 ekstra per 2. nivå)
#   "angrep"  navnet på angrepet
ARTER = {
    "tulimeles": {"navn": "TULIMELES", "type": "ild",    "liv": 20, "styrke": 3, "angrep": "GLØDKLO"},
    "sammalus":  {"navn": "SAMMALUS",  "type": "gress",  "liv": 22, "styrke": 2, "angrep": "MOSESLAG"},
    "merikorn":  {"navn": "MERIKORN",  "type": "vann",   "liv": 21, "styrke": 3, "angrep": "BØLGESTØT"},
    "tanngris":  {"navn": "TANNGRIS",  "type": "lyn",    "liv": 16, "styrke": 2, "angrep": "LYNSTANG"},
    "vardkivi":  {"navn": "VARDKIVI",  "type": "stein",  "liv": 20, "styrke": 1, "angrep": "STEINRAS"},
    "lepulvis":  {"navn": "LEPULVIS",  "type": "normal", "liv": 15, "styrke": 1, "angrep": "STØVSKY"},
    "kvistulus": {"navn": "KVISTULUS", "type": "gress",  "liv": 14, "styrke": 1, "angrep": "KVISTPISK"},
    "lapanvett": {"navn": "LAPANVETT", "type": "normal", "liv": 18, "styrke": 2, "angrep": "KALDGUFS"},
}

# Monstrene som bor i det høye gresset. Står et monster flere ganger, er det vanligere.
VILLE_MONSTRE = ["lepulvis", "lepulvis", "kvistulus", "kvistulus", "tanngris",
                 "vardkivi", "lapanvett"]


def terning(minste, storste):
    """Gir et tilfeldig heltall fra minste til og med storste. (Fra teksteventyret!)"""
    return random.randint(minste, storste)


def lag_monster(art, nivaa):
    """Lager et nytt monster av en art på et nivå, og gir det tilbake som en dictionary."""
    oppskrift = ARTER[art]
    maks_liv = oppskrift["liv"] + nivaa * 2
    monster = {
        "art": art,                                 # f.eks. "tanngris" (til bildene)
        "navn": oppskrift["navn"],
        "type": oppskrift["type"],
        "angrep": oppskrift["angrep"],
        "nivaa": nivaa,
        "liv": maks_liv,                            # livet monsteret har nå
        "maks_liv": maks_liv,                       # fullt liv
        "styrke": oppskrift["styrke"] + nivaa // 2, # // deler og runder ned
    }
    return monster


# ---------- TYPER ----------
# Hver type har sin egen effekt og lyd når den angriper.
TYPER = {
    "ild":    {"effekt": "ild",   "lyd": "angrep_ild"},
    "gress":  {"effekt": "blad",  "lyd": "angrep_blad"},
    "vann":   {"effekt": "vann",  "lyd": "angrep_vann"},
    "lyn":    {"effekt": "lyn",   "lyd": "angrep_lyn"},
    "stein":  {"effekt": "stein", "lyd": "angrep_stein"},
    "normal": {"effekt": "slag",  "lyd": "angrep_normal"},
}

# Hvilke typer hver type er STERK mot (gjør dobbel skade på).
STERK_MOT = {
    "ild": ["gress"],
    "gress": ["vann", "stein"],
    "vann": ["ild", "stein"],
    "lyn": ["vann"],
    "stein": ["ild", "lyn"],
    "normal": [],
}


# ---------- LAGET OG SEKKEN ----------
laget = [lag_monster("tulimeles", 5)]     # alle monstrene dine (en liste med dictionaries)
egen = laget[0]                           # monsteret som kjemper akkurat nå
motstander = None                         # det ville monsteret (lages når kampen starter)
sekk = {"fangstlykt": 5}                  # hvor mange av hver ting du har i sekken


# ---------- HELTEN ----------
helt = Figur("helt_ned_1", 7 * RUTE, 5 * RUTE - 8, skygge=True)

# Toppen av det høye gresset, som legges over føttene til helten
gress_over = Figur("hoyt_gress_over", 0, 0)
gress_over.synlig = False

steg_igjen = 0      # hvor mange piksler helten har igjen av steget sitt (0 = står stille)
dx = 0              # retning bortover:  1 = høyre, -1 = venstre, 0 = ingen av dem
dy = 0              # retning nedover:   1 = ned,   -1 = opp,     0 = ingen av dem
retning = "ned"     # hvilken vei helten ser: "opp", "ned", "venstre" eller "hoyre"

sted = "byen"       # hvilket kart vi er på: "byen", "stien", "hjemme", "laben" eller "hvilehuset"
neste_dor = None    # døra helten skal gå gjennom (se gaa_gjennom)
ting = []           # figurene som hører til kartet (folkene)

modus = "kart"      # hva spillet holder på med: "kart" eller "kamp"
kampfase = "venter" # hva kampen venter på: "meny", "lag" (lagmenyen) eller "venter" (på etter)


# ---------- TEKSTBOKSEN ----------
TEKSTFARGE = "#484858"
TEKSTSKYGGE = "#d0d0d8"

tekstboks = Figur("tekstboks", 4, 114, lag=3)
tekst = Tekst("", 12, 121, farge=TEKSTFARGE, skygge=TEKSTSKYGGE, maks_bredde=210)
tekstboks.synlig = False
tekst.synlig = False

samtale = []        # replikkene som venter på å bli vist
prater = False      # True mens helten prater med noen


# ---------- KAMPSKJERMEN ----------
# Alt på kampskjermen lages én gang her, men er skjult til det blir kamp.
# Bakgrunn, plattformer og monstre ligger i lag 0. Boksene og tekstene i lag 3.

# Fargene på HP-stolpen
GRONN = "#18c020"
GUL = "#c8a808"
ROD = "#a82818"

kamp_bakgrunn = Figur("kamp_bakgrunn", 0, 0, lag=0)
kamp_bunn = Rektangel(0, 112, 240, 48, "#283040", lag=0)      # mørkt bak tekstboksen
plattform_motstander = Figur("plattform_motstander", 136, 48, lag=0)
plattform_egen = Figur("plattform_egen", 8, 98, lag=0)

# Monstrene står på plattformene
motstander_figur = Figur("tanngris_foran", 152, 0, lag=0)
egen_figur = Figur("tulimeles_bak", 32, 50, lag=0)

# Infoboksen til motstanderen (oppe til venstre)
infoboks_motstander = Figur("infoboks_motstander", 8, 8, lag=3)
navn_motstander = Tekst("", 16, 13, farge=TEKSTFARGE, skygge=TEKSTSKYGGE)
nivaa_motstander = Tekst("", 86, 13, farge=TEKSTFARGE, skygge=TEKSTSKYGGE)
hp_motstander = Rektangel(41, 27, 64, 3, GRONN, lag=3)
ramme_motstander = Figur("hp_ramme", 34, 25, lag=3)

# Infoboksen til ditt eget monster (nede til høyre)
infoboks_egen = Figur("infoboks_egen", 126, 72, lag=3)
navn_egen = Tekst("", 134, 77, farge=TEKSTFARGE, skygge=TEKSTSKYGGE)
nivaa_egen = Tekst("", 208, 77, farge=TEKSTFARGE, skygge=TEKSTSKYGGE)
hp_egen = Rektangel(165, 91, 64, 3, GRONN, lag=3)
ramme_egen = Figur("hp_ramme", 158, 89, lag=3)
hp_tall = Tekst("", 200, 98, farge=TEKSTFARGE, skygge=TEKSTSKYGGE)

# Alt som hører til kampskjermen, samlet i én liste
kampting = [kamp_bakgrunn, kamp_bunn, plattform_motstander, plattform_egen,
            motstander_figur, egen_figur,
            infoboks_motstander, navn_motstander, nivaa_motstander, hp_motstander,
            ramme_motstander,
            infoboks_egen, navn_egen, nivaa_egen, hp_egen, ramme_egen, hp_tall]

for figur in kampting:
    figur.synlig = False

# Menyen nede til høyre. Valg nummer 0, 1, 2 og 3 ligger slik:
#     0 ANGRIP    1 SEKK
#     2 MONSTRE   3 FLYKT
MENYVALG = ["ANGRIP", "SEKK", "MONSTRE", "FLYKT"]
MENY_X = [144, 190, 144, 190]       # x for hvert valg
MENY_Y = [124, 124, 137, 137]       # y for hvert valg

menyboks = Figur("menyboks", 130, 118, lag=3)
menyting = [menyboks]
for nr in range(4):
    menyting.append(Tekst(MENYVALG[nr], MENY_X[nr], MENY_Y[nr],
                          farge=TEKSTFARGE, skygge=TEKSTSKYGGE))
pil = Figur("pil", MENY_X[0] - 8, MENY_Y[0] + 1, lag=3)
menyting.append(pil)

for figur in menyting:
    figur.synlig = False

valg = 0            # hvilket menyvalg pila peker på

# Fangstlykta som kastes
lykt = Figur("fangstkule_1", 0, 0, lag=2)
lykt.synlig = False
lykt_flyr = 0       # hvor mange bilder lykta har igjen å fly (0 = den flyr ikke)

# Lagmenyen: figurene lages når menyen åpnes, og fjernes når den lukkes
lagmeny_ting = []
lagpil = Figur("pil", 12, 0, lag=3)
lagpil.synlig = False
lagvalg = 0             # hvilket monster i laget pila peker på
tvunget_bytte = False   # True når monsteret ditt har besvimt og du MÅ velge et nytt


# ---------- KARTFUNKSJONER ----------

def lag_folk():
    """Lager en figur for hver person som står på dette kartet."""
    for person in folk:
        if person["kart"] == sted:
            figur = Figur(person["bilde"] + "_" + person["retning"],
                          person["kolonne"] * RUTE, person["rad"] * RUTE - 8, skygge=True)
            person["figur"] = figur
            ting.append(figur)


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
    gress_over.synlig = False


# ---------- FOLK OG PRAT ----------

def person_ved(x, y):
    """Gir personen som står på x, y på dette kartet, eller None hvis ingen står der."""
    for person in folk:
        if person["kart"] == sted:
            if person["kolonne"] * RUTE == x and person["rad"] * RUTE - 8 == y:
                return person
    return None


def vis_tekst(ny_tekst):
    """Viser en tekst i tekstboksen."""
    tekst.tekst = ny_tekst
    tekst.maks_bredde = 210
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
    if len(samtale) > 0:
        vis_tekst(samtale.pop(0))       # pop(0) tar ut den første i lista
        spill_lyd("tekst_pip")
    else:
        skjul_tekst()
        prater = False


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

    # Står det en person foran helten? Da snur personen seg og sier noe.
    person = person_ved(x, y)
    if person != None:
        person["figur"].bilde = person["bilde"] + "_" + MOTSATT[retning]
        si(person["replikker"])


# ---------- KAMP ----------

def vis_kampskjerm(synlig):
    """synlig=True: vis kampskjermen og skjul kartfigurene. synlig=False: omvendt."""
    for figur in kampting:
        figur.synlig = synlig
    for figur in ting:
        figur.synlig = not synlig
    helt.synlig = not synlig
    vis_kart(not synlig)            # kampskjermen dekker kartet: ikke tegn det


def mote():
    """Et vilt monster hopper fram!"""
    stopp_musikk()
    spill_lyd("mote")
    overgang(start_kamp, stil="kamp")


def start_kamp():
    """Kjøres midt i kamp-overgangen, mens skjermen er svart."""
    global modus, motstander, kampfase, valg
    modus = "kamp"
    valg = 0                    # pila starter på ANGRIP
    vis_kampskjerm(True)
    gress_over.synlig = False
    spill_musikk("kamp")

    # Et tilfeldig vilt monster på et tilfeldig nivå
    art = random.choice(VILLE_MONSTRE)
    motstander = lag_monster(art, random.randint(2, 4))
    motstander_figur.bilde = motstander["art"] + "_foran"
    egen_figur.bilde = egen["art"] + "_bak"
    oppdater_infobokser()
    hp_motstander.bredde = stolpe_lengde(motstander)    # stolpene starter på riktig lengde
    hp_egen.bredde = stolpe_lengde(egen)

    vis_tekst("En vill " + motstander["navn"] + " dukket opp!")
    kampfase = "venter"
    etter(2.0, vis_meny)


def oppdater_infobokser():
    """Skriver navn, nivå og liv i de to infoboksene."""
    navn_motstander.tekst = motstander["navn"]
    nivaa_motstander.tekst = "Nv" + str(motstander["nivaa"])

    navn_egen.tekst = egen["navn"]
    nivaa_egen.tekst = "Nv" + str(egen["nivaa"])
    hp_tall.tekst = str(egen["liv"]) + "/" + str(egen["maks_liv"])


def stolpe_lengde(monster):
    """Hvor lang HP-stolpen til monsteret skal være (fra 0 til 64 piksler)."""
    return round(64 * monster["liv"] / monster["maks_liv"])


def hp_farge(andel):
    """Gir fargen på HP-stolpen. andel er fra 0 (tom) til 1 (full)."""
    if andel > 0.5:
        return GRONN
    elif andel > 0.2:
        return GUL
    else:
        return ROD


def oppdater_stolpe(stolpe, monster):
    """Kjøres 60 ganger i sekundet: stolpen glir mot riktig lengde."""
    maal = stolpe_lengde(monster)
    if stolpe.bredde > maal:
        stolpe.bredde = stolpe.bredde - 1
    elif stolpe.bredde < maal:
        stolpe.bredde = stolpe.bredde + 1
    stolpe.farge = hp_farge(stolpe.bredde / 64)


def vis_meny():
    """Viser menyen og venter på at spilleren velger."""
    global kampfase
    kampfase = "meny"
    vis_tekst("Hva vil " + egen["navn"] + " gjøre?")
    tekst.maks_bredde = 110         # smal tekst, så menyen får plass til høyre
    for figur in menyting:
        figur.synlig = True


def skjul_meny():
    """Skjuler menyen. Nå venter kampen på etter() i stedet for på spilleren."""
    global kampfase
    kampfase = "venter"
    for figur in menyting:
        figur.synlig = False


def styr_menyen():
    """Kjøres 60 ganger i sekundet mens menyen vises."""
    global valg

    pil.x = MENY_X[valg] - 8
    pil.y = MENY_Y[valg] + 1

    if tast_trykket("hoyre") and (valg == 0 or valg == 2):
        valg = valg + 1
        spill_lyd("meny_pip")
    elif tast_trykket("venstre") and (valg == 1 or valg == 3):
        valg = valg - 1
        spill_lyd("meny_pip")
    elif tast_trykket("ned") and (valg == 0 or valg == 1):
        valg = valg + 2
        spill_lyd("meny_pip")
    elif tast_trykket("opp") and (valg == 2 or valg == 3):
        valg = valg - 2
        spill_lyd("meny_pip")

    if tast_trykket("mellomrom"):
        spill_lyd("velg")
        skjul_meny()
        if valg == 0:
            spiller_angriper()
        elif valg == 1:
            bruk_fangstlykt()
        elif valg == 2:
            vis_lagmeny()
        elif valg == 3:
            flykt()


def flykt():
    """Spilleren løper fra kampen."""
    vis_tekst("Du kom deg unna!")
    spill_lyd("flykt")
    etter(1.5, slutt_kamp)


# ---------- FANGST ----------

def bruk_fangstlykt():
    """Spilleren valgte SEKK: kast en fangstlykt hvis du har noen."""
    # OPPGAVE 1: Er sekk["fangstlykt"] 0? Vis "Du har ingen fangstlykter!" og
    #            gå tilbake til menyen om 1.5 sekunder (etter(1.5, vis_meny)).
    #            Ellers: trekk 1 fra sekk["fangstlykt"] og kall kast_lykt().
    vis_tekst("Det kan du ikke ennå!")
    etter(1.5, vis_meny)


def kast_lykt():
    """Lykta starter nede til venstre og skal fly i en bue mot motstanderen."""
    global lykt_flyr
    vis_tekst("Du kastet en FANGSTLYKT! (" + str(sekk["fangstlykt"]) + " igjen)")
    spill_lyd("kast")
    lykt.x = 40
    lykt.y = 80
    lykt.synlig = True
    lykt.animer(["fangstkule_kast_1", "fangstkule_kast_2", "fangstkule_kast_3", "fangstkule_kast_4"],
                fart=3)                         # lykta snurrer mens den flyr
    lykt_flyr = 34


def flytt_lykt():
    """Kjøres hvert bilde mens lykta flyr. Den går 4 piksler bortover og i en bue."""
    global lykt_flyr
    lykt_flyr = lykt_flyr - 1
    t = 34 - lykt_flyr                          # hvor mange bilder lykta har fløyet
    lykt.x = 40 + 4 * t
    lykt.y = 80 - 4.6 * t + 0.1 * t * t         # først opp, så ned igjen
    if lykt_flyr == 0:
        lykt_lander()


def lykt_lander():
    """Lykta treffer: monsteret forsvinner inn i den, og lykta vugger tre ganger."""
    lykt.animer(["fangstkule_apen", "fangstkule_1"], fart=18, gjenta=False)   # åpen i 0,3 s, så lukket
    effekt("glitter", motstander_figur.midt_x, motstander_figur.midt_y + 8)
    motstander_figur.synlig = False
    etter(0.8, vugg)
    etter(1.6, vugg)
    etter(2.4, vugg)
    etter(3.2, fangst_resultat)


def vugg():
    spill_lyd("vugge")
    lykt.animer(["fangstkule_2", "fangstkule_1", "fangstkule_3", "fangstkule_1"],
                fart=5, gjenta=False)


def klarte_fangst():
    """Gir True hvis monsteret blir i lykta, og False hvis det slipper fri."""
    # OPPGAVE 2: Jo mindre liv motstanderen har, jo større sjanse.
    #            andel = liv / maks_liv  (1 = fullt liv, 0 = tomt)
    #            sjanse = 100 - round(70 * andel)  (fullt liv gir 30, nesten tomt nesten 100)
    #            Slå terning(1, 100). Er kastet mindre enn eller lik sjanse: True.
    return False


def fangst_resultat():
    if klarte_fangst():
        fanget()
    else:
        slapp_fri()


def fanget():
    """Monsteret ble i lykta!"""
    # OPPGAVE 3: Spill lyden "fanget", vis "Hurra! Du fanget TANNGRIS!",
    #            legg motstander til i laget (append), og avslutt kampen
    #            om 2.5 sekunder.
    slutt_kamp()


def slapp_fri():
    """Monsteret slapp ut av lykta, og nå er det motstanderens tur."""
    lykt.synlig = False
    motstander_figur.synlig = True
    effekt("poff", lykt.midt_x, lykt.midt_y)
    spill_lyd("slapp_fri")
    vis_tekst("Å nei! " + motstander["navn"] + " slapp fri!")
    etter(2.0, motstander_svarer)


# ---------- LAGMENYEN ----------

def vis_lagmeny():
    """Viser alle monstrene i laget, ett per linje, med ikon, navn, nivå og liv."""
    global kampfase, lagvalg
    kampfase = "lag"
    lagvalg = 0
    lagmeny_ting.append(Figur("lag_bakgrunn", 0, 0, lag=3))     # seks tomme plasser
    for nr in range(len(laget)):
        monster = laget[nr]
        y = 6 + nr * 17             # hver linje er 17 piksler lenger ned
        felt = "lag_felt"
        if monster is egen:             # monsteret som kjemper nå, får et eget felt
            felt = "lag_felt_aktiv"
        if monster["liv"] <= 0:         # et besvimt monster får et rødt felt
            felt = "lag_felt_besvimt"
        lagmeny_ting.append(Figur(felt, 18, y, lag=3))     # feltet bak linja
        # OPPGAVE 4: Lag ikonet (f.eks. "tanngris_ikon") på x=24, og tre tekster
        #            4 piksler lenger ned: navnet på x=46, "Nv3" på x=126 og
        #            "12/21" (liv/maks_liv) på x=176. Legg alt i lagmeny_ting.
        pass
        # En liten HP-stav under navnet (sporet er tegnet i lag_felt)
        lagmeny_ting.append(Rektangel(46, y + 13, stolpe_lengde(monster) * 3 // 4, 2,
                                      hp_farge(monster["liv"] / monster["maks_liv"]), lag=3))
    lagpil.synlig = True
    lagpil.legg_overst()            # pila skal ligge over bakgrunnen
    if tvunget_bytte:
        vis_tekst("Hvem skal kjempe nå?")
    else:
        vis_tekst("Hvem skal kjempe? (ESC = tilbake)")


def lukk_lagmeny():
    for figur in lagmeny_ting:
        figur.fjern()
    lagmeny_ting.clear()
    lagpil.synlig = False


def styr_lagmenyen():
    """Kjøres 60 ganger i sekundet mens lagmenyen vises."""
    global lagvalg
    # OPPGAVE 5: Opp og ned skal flytte lagvalg (men ikke under 0 eller forbi det
    #            siste monsteret: len(laget) - 1). Spill "meny_pip" når valget flytter seg.
    #            Pila skal stå på y = 6 + lagvalg * 17 + 5.
    pass

    if tast_trykket("mellomrom"):
        bytt_monster(lagvalg)
    elif tast_trykket("escape") and not tvunget_bytte:
        lukk_lagmeny()
        vis_meny()


def bytt_monster(nr):
    """Bytter til monster nummer nr i laget."""
    global egen, kampfase, tvunget_bytte
    valgt = laget[nr]
    if valgt is egen and not tvunget_bytte:     # is: akkurat det samme monsteret
        vis_tekst(valgt["navn"] + " kjemper allerede!")
        return

    # OPPGAVE 6: Har det valgte monsteret 0 liv? Vis "... har ikke krefter igjen!"
    #            og return. Ellers: lukk lagmenyen, la egen bli valgt, bytt bildet
    #            til egen_figur (f.eks. "tanngris_bak") og kall oppdater_infobokser().
    vis_tekst("Du kan ikke bytte ennå!")
    return

    egen_figur.synlig = True
    hp_egen.bredde = stolpe_lengde(egen)
    kampfase = "venter"
    spill_lyd("velg")
    vis_tekst("Kom igjen, " + egen["navn"] + "!")
    if tvunget_bytte:
        tvunget_bytte = False
        etter(1.5, vis_meny)            # det forrige monsteret besvimte: din tur
    else:
        etter(1.5, motstander_svarer)   # å bytte koster en tur


def noen_kan_kjempe():
    """Gir True hvis minst ett monster i laget har liv igjen."""
    # OPPGAVE 7: Gå gjennom laget. Har et monster mer enn 0 liv, gi True.
    #            Har ingen liv igjen, gi False.
    return False


# ---------- ANGREP ----------

def effektivitet(angrep_type, forsvar_type):
    """Gir 2 hvis angrepet er supereffektivt, ellers 1."""
    if forsvar_type in STERK_MOT[angrep_type]:
        return 2
    return 1


def angrip(angriper, forsvarer, figur):
    """angriper slår forsvarer. figur er bildet til den som blir truffet.
    Gir tilbake 2 hvis det var supereffektivt, ellers 1."""
    ganger = effektivitet(angriper["type"], forsvarer["type"])
    skade = (terning(1, 4) + angriper["styrke"]) * ganger
    forsvarer["liv"] = forsvarer["liv"] - skade
    if forsvarer["liv"] < 0:
        forsvarer["liv"] = 0

    type_info = TYPER[angriper["type"]]
    effekt(type_info["effekt"], figur.midt_x, figur.midt_y)
    spill_lyd(type_info["lyd"])
    figur.glimt(0.2)
    figur.rist(0.4, 2)

    if ganger == 2:
        spill_lyd("supereffektiv")
        rist_skjerm(0.3, 2)
    flytende_tekst("-" + str(skade), figur.midt_x, figur.midt_y - 12)
    oppdater_infobokser()
    return ganger


def spiller_angriper():
    """Ditt monster angriper motstanderen."""
    ganger = angrip(egen, motstander, motstander_figur)
    melding = egen["navn"] + " brukte " + egen["angrep"] + "!"
    if ganger == 2:
        melding = melding + " Det var supereffektivt!"
    vis_tekst(melding)

    # Besvimte motstanderen? Ellers er det motstanderens tur.
    if motstander["liv"] == 0:
        etter(2.0, motstander_besvimer)
    else:
        etter(2.0, motstander_svarer)


def motstander_svarer():
    """Motstanderen angriper ditt monster."""
    ganger = angrip(motstander, egen, egen_figur)
    melding = "Den ville " + motstander["navn"] + " brukte " + motstander["angrep"] + "!"
    if ganger == 2:
        melding = melding + " Det var supereffektivt!"
    vis_tekst(melding)

    # Besvimte ditt monster? Ellers er det din tur igjen.
    if egen["liv"] == 0:
        etter(2.0, egen_besvimer)
    else:
        etter(2.0, vis_meny)


def motstander_besvimer():
    effekt("poff", motstander_figur.midt_x, motstander_figur.midt_y + 16)
    motstander_figur.synlig = False
    spill_lyd("besvimer")
    vis_tekst("Den ville " + motstander["navn"] + " besvimte!")
    etter(2.0, vant)


def vant():
    stopp_musikk()
    spill_lyd("seier")
    vis_tekst("Du vant kampen!")
    etter(2.5, slutt_kamp)


def egen_besvimer():
    global tvunget_bytte
    effekt("poff", egen_figur.midt_x, egen_figur.midt_y + 16)
    egen_figur.synlig = False
    spill_lyd("besvimer")
    if noen_kan_kjempe():
        vis_tekst(egen["navn"] + " besvimte! Velg et nytt monster.")
        tvunget_bytte = True
        etter(2.0, vis_lagmeny)
    else:
        vis_tekst(egen["navn"] + " besvimte! Du bærer laget til hvilehuset ...")
        etter(2.5, tapt)


def tapt():
    """Ditt monster besvimte: tone ut og gå til hvilehuset."""
    overgang(til_hvilehuset)


def til_hvilehuset():
    """Kjøres midt i overgangen, mens skjermen er svart."""
    global retning
    tilbake_til_kartet()
    bygg_kart("hvilehuset")
    helt.x = 7 * RUTE
    helt.y = 4 * RUTE - 8
    retning = "opp"
    helt.bilde = "helt_opp_1"
    gress_over.synlig = False
    for monster in laget:
        monster["liv"] = monster["maks_liv"]
    spill_lyd("helbred")
    si(["Du hviler i hvilehuset ...", "Alle monstrene dine er friske igjen!"])


def slutt_kamp():
    """Toner ut og går tilbake til kartet."""
    overgang(tilbake_til_kartet)


def tilbake_til_kartet():
    """Kjøres midt i overgangen tilbake, mens skjermen er svart."""
    global modus
    modus = "kart"
    vis_kampskjerm(False)
    skjul_meny()
    skjul_tekst()
    lykt.synlig = False
    spill_musikk(KARTENE[sted]["musikk"])
    if rute_under_fotene(helt.x, helt.y) == '"':
        gress_over.synlig = True


def oppdater_kamp():
    """Kjøres 60 ganger i sekundet mens det er kamp."""
    # HP-stolpene glir litt hver gang
    oppdater_stolpe(hp_motstander, motstander)
    oppdater_stolpe(hp_egen, egen)

    # Lykta flyr
    if lykt_flyr > 0:
        flytt_lykt()

    if kampfase == "meny":
        styr_menyen()
    elif kampfase == "lag":
        styr_lagmenyen()


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

    # Står helten i høyt gress? Da dekker gresset føttene.
    if rute == '"':
        gress_over.x = helt.x
        gress_over.y = helt.y + 16
        gress_over.synlig = True

    # I høyt gress er det 1 sjanse av 8 for å møte et monster.
    if rute == '"' and random.randint(1, 8) == 1:
        mote()


def oppdater_kart():
    """Kjøres 60 ganger i sekundet mens helten er på kartet."""
    global steg_igjen, dx, dy, retning

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
        gress_over.synlig = False       # helten går ut av gresset
    else:
        spill_lyd("bump")
        # Helten står fast: stopp gang-animasjonen og vis bildet der han står stille
        helt.animer(None)
        helt.bilde = "helt_" + retning + "_1"
        dx = 0
        dy = 0
        steg_igjen = RUTE


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Mens skjermen toner ut og inn, skal ingenting skje.
    if i_overgang():
        return

    # Hva spillet gjør, kommer an på modus
    if modus == "kart":
        oppdater_kart()
    elif modus == "kamp":
        oppdater_kamp()


# ---------- START ----------
bygg_kart("byen")
start(tittel="Monsterjakten")

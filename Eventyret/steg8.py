# ============================================================
#  EVENTYRET – STEG 8: Ferdigstilling
# ============================================================
#
#  Nå gjør vi spillet ferdig! Det får en tittelskjerm, musikk som
#  passer til hvert sted, og en tidtaker: hvor fort klarer du å
#  beseire Slimkongen? Den beste tiden blir lagret i en fil, så
#  rekorden huskes til neste gang.
#
#  Spillet får også en pausemeny: trykk Escape, så fryser alt,
#  og du kan slå av musikken eller gå tilbake til tittelskjermen.
#
#  Og så: gjør spillet til DITT eget!
#
#  Taster:  piltastene = gå   shift = løp
#           mellomrom = slå, eller snakk / åpne når du står foran noe
#           Enter = start spillet (på tittelskjermen)
#           Escape = pausemeny (pil opp/ned og Enter i menyen)
#
#  Nytt i dag:
#    - musikk med spill_musikk() og stopp_musikk()
#    - tittelskjerm med stor pikselskrift: Tekst(..., storrelse=2)
#    - tid(): hvor mange sekunder spillet har gått
#    - å lagre og lese en fil (rekord.txt) med open()
#    - copy.deepcopy(): en helt ny kopi av alle rommene til et nytt spill
#    - pause(True) og pause(False): fryser spillet mens pausemenyen er åpen
#
#  Endret fra steg 7:
#    - Spillet starter på tittelskjermen (tilstand = "tittel").
#    - Hvert rom har en "musikk".
#    - Etter seieren går du tilbake til tittelskjermen.
#
# ============================================================

from spillmotor import *
import random
import copy
import os

BREDDE = 240        # skjermen i piksler
HOYDE = 160


# ---------- KARTENE ----------
# Hvert tegn er én rute. Ordboka RUTER sier hvilket bilde hvert tegn skal ha.
#   .  ,  *   gress (litt forskjellig)      =   sti
#   ~         vann                          B   busk (kan kuttes)
#   h         hekk langs kanten (kan ikke kuttes)
#   S  s      stein (to bilder)             T  t  tre (to slags trær)
#   #  V      hulevegg (topp og forside)    H   huleinngang
#   Y         tett skog (kan ikke kuttes)
#   M  m      klippe (M = de to øverste radene, m = foten)
#   n         buen over huleinngangen (to ruter høy, stenger: helten går inn i hulen fra H)
#   [  ]      klippekant på sidene av fjellet
#   A         avsats (lav steinkant ned mot engen)
#   _  -      hulegulv                      L   låst dør      D   åpen dør
#   v         hulevegg med mose og røtter
#   k  o      toppen av nordveggen (o = over en dør)
#   F         fakkel                        K   kloss
#   b  p      bryter (av og på)             +   ornamentgulv (bossrommet)

ENGEN = [
    "hhhhhh.=.hhhhhh",
    "h..,B..=....*.h",
    "h.*BB..=..,...h",
    "h..~~~~=......h",
    "h..~~~~=====...",
    "h..~~~~....====",
    "ht....,..S.....",
    "h.S.......*...h",
    "h....,....SS.Th",
    "hhhhhhhhhhhhhhh",
]

SKOGEN = [
    "YYYYYYYYYYYYYYY",
    "Y.,YYYYY..,...Y",
    "Y..T....t..*.YY",
    "Y.....,......YY",
    "...B..T...BBBBY",
    "=====.....B..BY",
    "....===...B..BY",
    "YYt...=...BBBBY",
    "YYY.,.=...YYYYY",
    "YYYYYYYYYYYYYYY",
]

RUTER = {
    ".": "gress_stor",                       # et stort mønster (like stort som skjermen)
    ",": "gress_2",
    "*": ["gress_blomst", "gress_blomst_2"], # blomstene vaier
    "=": "sti",
    "~": ["vann_1", "vann_2", "vann_3"],     # en liste med bilder = animert rute
    "B": "busk",
    "h": "hekk_monster",                    # kantblokk, kan ikke kuttes
    "S": "stein",
    "s": "stein_2",
    "T": "gress_stor",                       # selve treet er en figur oppå gresset
    "t": "gress_stor",                       # et annet slags tre (tre_2)
    "#": "hulevegg_topp_stor",               # veggen sett ovenfra (et mønster)
    "V": "hulevegg_stor",                    # nordveggen (like bred som skjermen)
    "H": "huleinngang",
    "Y": "skog_stor",                        # tett skog (kan ikke kuttes), et stort mønster
    "M": "klippe_stor",                      # klippen på fjellet: de to øverste radene ...
    "m": "klippe_stor",                      # ... og foten (samme store bilde, så lagene henger sammen)
    "n": "huleinngang_bue_hoy",              # buen over huleinngangen (to ruter høy)
    "[": "fjellside_stor_venstre",           # klippekant på sidene (like høy som skjermen)
    "]": "fjellside_stor_hoyre",
    "A": "avsats",                           # lav steinkant nederst på fjellet
    "_": "hulegulv_stor",                    # hulegulvet (like stort som skjermen)
    "-": "hulegulv_2_stor",                  # gulv med sprekker (et mønster)
    "v": "hulevegg_mose",                   # vegg med mose og røtter
    "+": "bossgulv_stor",                    # ornamentgulv i bossrommet (ett stort segl)
    "L": "dor_laast",
    "D": "dor_aapen",
    "k": "hulevegg_kappe_stor",             # toppen av den høye nordveggen
    "o": "dor_topp",                        # veggen rett over en dør
    "K": "kloss",
    "b": "bryter_av",
    "p": "bryter_paa",
}

# (steg 7) Gjør faklene (F) om til en animert rute med bildene fakkel_1 og fakkel_2.
RUTER["F"] = ["fakkel_1", "fakkel_2"]

# Myke kanter der stien og vannet møter gresset
KANTER = {"=": ("stikant", ".,*"), "~": ("vannkant", ".,*=B")}
# Kanten av skogen (Y) mot gresset, og skyggen skogen og klippene kaster på gresset
KANTER["Y"] = ("skogkant", ".,*=BTt")
KANTER["."] = [("skogskygge", "Y"), ("fjellskygge", "[]m")]
KANTER[","] = [("skogskygge", "Y"), ("fjellskygge", "[]m")]
KANTER["*"] = [("skogskygge", "Y"), ("fjellskygge", "[]m")]
# Hjørnene der klippene på fjellet møtes, og endene av avsatsen
KANTER["["] = [("klippehjorne_topp", "M"), ("klippehjorne_fot", "m")]
KANTER["]"] = [("klippehjorne_topp", "M"), ("klippehjorne_fot", "m")]
KANTER["A"] = [("avsats", ".,*"), ("avsatsfeste", "[]")]
# Hekken sett ovenfra der den går langs kanten nedover
KANTER["h"] = ("hekkant", ".,*=BTtSs")
# Skyggestripe på gulvet langs veggene i hulen (gir dybde – ferdig kode)
KANTER["_"] = [("gulvskygge", "#VvFLD"), ("fakkellys", "F")]
KANTER["-"] = [("gulvskygge", "#VvFLD"), ("fakkellys", "F")]
# Avfaset kant der veggen møter gulvet
KANTER["#"] = ("veggkant", "_-+bpK")
# Gullkant rundt arenaen i bossrommet
KANTER["+"] = [("ornament", "_-"), ("gulvskygge", "#VvFLD"), ("fakkellys", "F")]

# Tegn som helten IKKE kan gå gjennom
HINDRINGER = ["S", "s", "B", "h", "~", "T", "#", "V", "L", "F", "K", "k", "o", "Y", "M", "m", "n", "[", "]", "A", "v", "t"]

# Trærne er figurer oppå gresset. Ordboka sier hvilket bilde hvert tre-tegn får.
TRAER = {"T": "tre", "t": "tre_2"}

# ---------- ROMMENE ----------
# Hvert rom har et kart, og sier hvilket rom som ligger i hver retning.
# "hoyre": "skogen" betyr: går du ut til høyre, kommer du til skogen.

ROM = {
    "engen":  {"kart": ENGEN, "hoyre": "skogen"},
    "skogen": {"kart": SKOGEN, "venstre": "engen"},
}

# (steg 2) Lag et nytt rom over engen.
FJELLET = [
    "[MMMMMMnMMMMMM]",
    "[MMMMMMnMMMMMM]",
    "[mmmmmmHmmmmmm]",
    "[.T....=..,...]",
    "[...*..=....t.]",
    "[..S...=......]",
    "[...,..=..*...]",
    "[.T....=...S..]",
    "[.....,=..,...]",
    "[AAAAA.=.AAAAA]",
]
ROM["fjellet"] = {"kart": FJELLET, "ned": "engen"}
ROM["engen"]["opp"] = "fjellet"

# Fiendene i hvert rom: [art, kolonne, rad]
ROM["engen"]["fiender"] = [["slim", 10, 2], ["slim", 11, 6]]
ROM["skogen"]["fiender"] = [["slim", 8, 3], ["slim", 4, 7], ["flaggermus", 11, 1]]
ROM["fjellet"]["fiender"] = [["slim", 9, 5], ["flaggermus", 12, 6], ["flaggermus", 4, 6]]

# ---------- HULEN ----------
HULEN = [
    "#kkkkkkokkkkkk#",
    "#vVFVVVLVVVFVv#",
    "#_____-_______#",
    "#_-_________-_#",
    "#_____________#",
    "#______-______#",
    "#_-___________#",
    "#_________-___#",
    "#___-_________#",
    "#######_#######",
]
GANGEN = [
    "#kkkkkkokkkkkk#",
    "#VVFVvVDVvVFVV#",
    "#_____________#",
    "#__-______-___#",
    "#KKKKKKKKKKKKK#",
    "#______-______#",
    "#_-___________#",
    "#_________-___#",
    "#_b_-_________#",
    "#######_#######",
]
BOSSROMMET = [
    "#kkkkkkkkkkkkk#",
    "#VVFVVvVvVVFVV#",
    "#_____________#",
    "#__+++++++++__#",
    "#__+++++++++__#",
    "#__+++++++++__#",
    "#__+++++++++__#",
    "#__+++++++++__#",
    "#_____________#",
    "#######_#######",
]
ROM["hulen"] = {"kart": HULEN, "ned": "fjellet", "opp": "gangen"}
ROM["gangen"] = {"kart": GANGEN, "ned": "hulen", "opp": "bossrommet"}
ROM["bossrommet"] = {"kart": BOSSROMMET, "ned": "gangen"}
ROM["fjellet"]["opp"] = "hulen"

ROM["hulen"]["fiender"] = [["flaggermus", 3, 4], ["flaggermus", 11, 4]]
ROM["gangen"]["fiender"] = [["slim", 4, 6], ["slim", 10, 7], ["flaggermus", 7, 2]]
ROM["bossrommet"]["fiender"] = [["boss", 6.5, 3]]

# Tingene i hvert rom: [art, kolonne, rad]. En kiste har også innholdet sitt.
ROM["engen"]["ting"] = [["ragna", 5, 8], ["mynt", 1, 1], ["mynt", 13, 2]]
ROM["skogen"]["ting"] = [["kiste", 11, 5, "nøkkel"], ["mynt", 12, 6], ["mynt", 1, 1], ["mynt", 8, 8]]
ROM["fjellet"]["ting"] = [["mynt", 1, 8], ["mynt", 13, 3]]
ROM["hulen"]["ting"] = [["mynt", 1, 2], ["mynt", 13, 8], ["krukke", 1, 8], ["krukke", 2, 8]]
ROM["gangen"]["ting"] = [["mynt", 1, 2], ["mynt", 13, 2], ["mynt", 7, 3],
                         ["krukke", 12, 8], ["krukke", 13, 8], ["krukke", 11, 8]]
ROM["bossrommet"]["ting"] = [["krukke", 1, 2], ["krukke", 13, 2], ["krukke", 1, 8], ["krukke", 13, 8]]

# Musikken i hvert rom (filene ligger i mappen musikk/)
ROM["engen"]["musikk"] = "landsby"
ROM["skogen"]["musikk"] = "oververden"
ROM["fjellet"]["musikk"] = "oververden"
ROM["hulen"]["musikk"] = "hule"
ROM["gangen"]["musikk"] = "hule"
ROM["bossrommet"]["musikk"] = "boss"

# OPPGAVE 7: Gjør spillet ditt eget! Lag nye rom, flytt fiender og ting, endre reglene ...
# Husk: et nytt rom trenger "kart", "fiender", "ting" og "musikk", og åpninger som passer.

# En urørt kopi av alle rommene. Den bruker vi når vi starter et helt nytt spill.
START_ROM = copy.deepcopy(ROM)

# Rekorden lagres i en fil i samme mappe som spillet
REKORDFIL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rekord.txt")

# Ting man ikke kan gå gjennom
FASTE = ["kiste", "ragna", "krukke"]

# Det Gamle Ragna sier, én replikk om gangen
RAGNA_SIER = [
    "Gamle Ragna: Å, der er du endelig! Slimkongen har tatt over hulen oppe ved fjellet.",
    "Døra inn i hulen er låst. Men nøkkelen ligger i en kiste i skogen, mot høyre.",
    "Kisten står gjemt bak noen busker. Kanskje sverdet ditt kan hjelpe?",
    "Lykke til, lille venn. Og pass deg for slimene!",
]

# Egenskapene til hver fiende-art
FIENDER = {
    "slim":       {"liv": 2, "fart": 0.5, "skade": 1, "treffboks": (2, 6, 12, 10)},
    "flaggermus": {"liv": 1, "fart": 0.6, "skade": 1, "treffboks": (2, 3, 12, 10)},
    "boss":       {"liv": 10, "fart": 1,  "skade": 2, "treffboks": (2, 8, 28, 24)},
}


# ---------- HELTEN ----------
# Helten er 16 piksler bred og 24 piksler høy.
# treffboks=(2, 16, 12, 8) betyr at bare føttene kan krasje i ting.

helt = Figur("helt_ned_1", 5 * RUTE, 6 * RUTE - 8, treffboks=(2, 16, 12, 8), skygge=True)

FART = 1            # hvor mange piksler helten går hver gang oppdater() kjøres
MAKS_LIV = 6        # 6 halve hjerter = 3 hjerter

# Hvor sverdet skal stå, sett fra øverste venstre hjørne av helten.
# (0, 24) betyr: 0 piksler mot høyre og 24 piksler ned, altså rett under føttene.
SVERD_PLASS = {
    "ned": (0, 24),
    "opp": (0, -8),
    "venstre": (-16, 8),
    "hoyre": (16, 8),
}

# Sverdslaget vises i tre faser: 1 = oppsving, 2 = hugg, 3 = etterslag.
# Her står hvor sverdet tegnes i hver fase (fra heltens øverste venstre hjørne).
# Treffet regnes fortsatt ut med SVERD_PLASS over, så slaget treffer som før.
SVERD_FASER = {
    "ned":     [(-9, -4), (-7, 17), (12, 16)],     # sverdet i høyre hånd
    "opp":     [(10, 14), (8, -6), (-8, -6)],
    "venstre": [(6, -4), (-14, 2), (-13, 14)],
    "hoyre":   [(-6, -4), (14, 2), (13, 14)],
}

# Ett skritt i hver retning: (dx, dy)
RETNINGER = {
    "ned": (0, 1),
    "opp": (0, -1),
    "venstre": (-1, 0),
    "hoyre": (1, 0),
}


# ---------- VARIABLER ----------

rom = "engen"       # rommet helten er i nå (som sted i teksteventyret)
retning = "ned"     # "opp", "ned", "venstre" eller "hoyre"
gaa_teller = 0      # teller hvor lenge helten har gått (til animasjonen)
ut_av = None        # hvilken kant helten går ut av skjermen ("venstre", "hoyre", ...)
traer = []          # trærne i rommet
slag = 0            # hvor mange bilder igjen av sverdslaget (0 = slår ikke)
sverd = None        # sverd-figuren mens helten slår, ellers None
fiender = []        # fiendene i rommet
liv = MAKS_LIV      # hvor mange halve hjerter helten har igjen
tilstand = "tittel" # "tittel", "spill", "pause", "game_over", "prat", "jubel" eller "seier"
starttid = 0        # tid() da spillet startet
dytt = 0            # hvor mange bilder igjen helten blir dyttet bakover
dytt_x = 0          # hvor mye helten dyttes hvert bilde
dytt_y = 0
lite_liv_teller = 0 # teller til varsellyden når helten har lite liv
ting_i_rommet = []  # mynter, hjerter, kister og personer i rommet
mynter = 0
nokler = 0
replikker = []      # det personen sier (en liste med tekster)
replikk_nr = 0      # hvilken replikk som vises nå
skatt = None        # figuren helten holder over hodet når han jubler
valg = 0            # hvilket valg pila peker på i pausemenyen (0 = det øverste)
musikk_paa = True   # blir False hvis du slår av musikken i pausemenyen


# ---------- HUD (hjertene øverst) ----------
# Ett hjerte for hvert andre liv. Lag 3 betyr at de tegnes over alt annet.
# Mørk bakgrunn bak hjertene, så de synes på alle kart (ferdig kode)
hud_bakgrunn_venstre = Figur("hud_bakgrunn_venstre", 1, 1, lag=3)
hjerter = []
for i in range(MAKS_LIV // 2):
    hjerte = Figur("hud_hjerte_full", 4 + i * 9, 4, lag=3)
    hjerter.append(hjerte)

# Mynter og nøkler øverst til høyre
hud_bakgrunn_hoyre = Figur("hud_bakgrunn_hoyre", 196, 1, lag=3)     # bak tellerne (ferdig kode)
mynt_ikon = Figur("hud_mynt", 200, 4, lag=3)
mynt_tekst = Tekst("000", 210, 3, farge="white", skygge="#181820")
nokkel_ikon = Figur("hud_nokkel", 200, 14, lag=3)
nokkel_tekst = Tekst("0", 210, 13, farge="white", skygge="#181820")

# Dialogvinduet nederst (usynlig til noen snakker)
vindu = Figur("vindu", 4, 112, lag=3)
vindu.synlig = False
prat_tekst = Tekst("", 12, 117, farge="white", skygge="#101020", maks_bredde=216)
prat_tekst.synlig = False

# Game over-skjermen lages nå, men er usynlig til helten dør
game_over_bilde = Figur("game_over", 0, 0, lag=3)
game_over_bilde.synlig = False
game_over_tittel = Tekst("GAME OVER", 0, 24, farge="white", skygge="#181820", storrelse=2)
game_over_tittel.x = (BREDDE - game_over_tittel.bredde) / 2     # midt på skjermen
game_over_tittel.synlig = False
game_over_tekst = Tekst("Trykk Enter for å prøve igjen", 0, 144, farge="white", skygge="#181820")
game_over_tekst.x = (BREDDE - game_over_tekst.bredde) / 2
game_over_tekst.synlig = False

# Tittelskjermen
tittel_bilde = Figur("tittel", 0, 0, lag=3)
tittel_navn = Tekst("EVENTYRET", 0, 14, farge="#f8e070", skygge="#181820", storrelse=2)
tittel_navn.x = (BREDDE - tittel_navn.bredde) / 2
tittel_under = Tekst("Slimkongens hule", 0, 36, farge="white", skygge="#181820")
tittel_under.x = (BREDDE - tittel_under.bredde) / 2
rekord_tekst = Tekst("", 4, 4, farge="white", skygge="#181820")
trykk_tekst = Tekst("Trykk Enter for å starte", 0, 144, farge="white", skygge="#181820")
trykk_tekst.x = (BREDDE - trykk_tekst.bredde) / 2
# Glitter som blinker over logoen (ferdig kode). Hver glitter starter på et annet bilde.
GLITTERBILDER = ["fx_glitter_1", "fx_glitter_2", "fx_glitter_3"]
tittel_glitter = []
for nr, (gx, gy) in enumerate([(66, 10), (116, 20), (166, 6)]):
    glitter = Figur("fx_glitter_1", gx, gy, lag=3)
    glitter.animer(GLITTERBILDER[nr:] + GLITTERBILDER[:nr], fart=10)
    tittel_glitter.append(glitter)

# Pausemenyen (ferdig kode). Valgene står i en liste, og pila peker på PAUSEVALG[valg].
PAUSEVALG = ["Fortsett", "Musikk", "Til tittelskjermen"]
pause_dim = Figur("pausemeny_dim", 0, 0, lag=3)         # gjør spillet bak menyen mørkere
pause_ramme = Figur("pausemeny", 60, 41, lag=3)
pause_valgt = Figur("pausemeny_valgt", 68, 0, lag=3)    # den lyse stripa bak valget
pause_pil = Figur("pausemeny_pil", 71, 0, lag=3)
pause_tittel = Tekst("PAUSE", 0, 48, farge="#f8d850", skygge="#101020", storrelse=2)
pause_tittel.x = (BREDDE - pause_tittel.bredde) / 2
pause_tekster = []                                      # én tekst for hvert valg
for i in range(len(PAUSEVALG)):
    pause_tekster.append(Tekst(PAUSEVALG[i], 84, 75 + i * 13, skygge="#101020"))
PAUSEMENY = [pause_dim, pause_ramme, pause_valgt, pause_pil, pause_tittel] + pause_tekster
for ting in PAUSEMENY:
    ting.synlig = False


# ---------- FUNKSJONER ----------

def lag_fiende(art, x, y):
    """Lager en ny fiende og legger den i lista fiender."""
    egenskaper = FIENDER[art]
    fiende = Figur(f"{art}_1", x, y, treffboks=egenskaper["treffboks"], skygge=True)

    # Egne variabler (attributter) på figuren:
    fiende.art = art                        # "slim" eller "flaggermus"
    fiende.liv = egenskaper["liv"]
    fiende.fart = egenskaper["fart"]
    fiende.dx = random.choice([-1, 1])      # retningen slimet går i
    fiende.dy = 0
    fiende.teller = random.randint(30, 90)  # hvor lenge til slimet bytter retning

    # (steg 4) Få fienden til å veksle mellom bilde 1 og 2 (bruk animer).
    fiende.animer([f"{art}_1", f"{art}_2"], fart=12)

    # Bossen har noen ekstra attributter
    if art == "boss":
        fiende.tilstand = "vent"        # "vent", "hopp" eller "angrip"
        fiende.teller = 90              # hvor lenge til bossen gjør noe nytt
        fiende.antall_hopp = 0
        fiende.vent_tid = 60            # hvor lenge bossen venter etter et hopp

    fiender.append(fiende)


def lag_ting(art, x, y, info=None):
    """Lager en ting (mynt, hjerte, kiste, person) og legger den i ting_i_rommet.
    info er lista fra ROM, så vi kan huske det når tingen blir tatt eller åpnet."""
    if art == "kiste":
        if info[3] == None:             # kisten er allerede tømt
            bilde = "kiste_aapen"
        else:
            bilde = "kiste_lukket"
    elif art == "ragna":
        bilde = "ragna_1"
        y = y - 8                       # Ragna er 24 høy, som helten
    else:
        bilde = art                     # "mynt" har ikke eget bilde, men "mynt_1"
        if art == "mynt":
            bilde = "mynt_1"

    ting = Figur(bilde, x, y, skygge=True)
    ting.art = art
    ting.info = info

    if art == "ragna":
        ting.treffboks = (2, 16, 12, 8)     # bare føttene, som helten
        ting.animer(["ragna_1", "ragna_2"], fart=30)

    # (steg 6) Få myntene til å snurre (bilde mynt_1, mynt_2, mynt_3 og mynt_4).
    if art == "mynt":
        ting.animer(["mynt_1", "mynt_2", "mynt_3", "mynt_4"], fart=8)

    ting_i_rommet.append(ting)


def fjern_ting(ting):
    """Fjerner en ting fra rommet – og fra ROM, så den ikke kommer tilbake."""
    ting.fjern()
    ting_i_rommet.remove(ting)
    if ting.info != None:
        ROM[rom]["ting"].remove(ting.info)


def endre_kart(kol, rad, tegn):
    """Bytter en rute på skjermen OG i kartet i ROM, så endringen blir husket."""
    endre_rute(kol, rad, tegn)
    kart = ROM[rom]["kart"]
    kart[rad] = kart[rad][:kol] + tegn + kart[rad][kol + 1:]


def tegn_rom():
    """Tegner kartet til rommet helten er i, med trær, fiender og ting."""
    global traer, fiender, ting_i_rommet
    for ting in ting_i_rommet:  # fjern tingene fra forrige rom
        ting.fjern()
    ting_i_rommet = []
    for tre in traer:           # fjern trærne fra forrige rom
        tre.fjern()
    traer = []
    for fiende in fiender:      # og fiendene
        fiende.fjern()
    fiender = []

    kart = ROM[rom]["kart"]
    tegn_kart(kart, RUTER, KANTER)

    # Gå gjennom hver rad og hver kolonne i kartet
    for rad in range(len(kart)):
        for kol in range(len(kart[rad])):
            if kart[rad][kol] in TRAER:
                # Treet er 32 x 32 piksler. Stammen skal stå midt i ruta.
                tre = Figur(TRAER[kart[rad][kol]], kol * RUTE - 8, rad * RUTE - 16)
                traer.append(tre)

    # Lag fiendene i rommet
    for info in ROM[rom]["fiender"]:
        lag_fiende(info[0], info[1] * RUTE, info[2] * RUTE)

    # Lag tingene i rommet
    for info in ROM[rom]["ting"]:
        lag_ting(info[0], info[1] * RUTE, info[2] * RUTE, info)

    # OPPGAVE 3: Spill musikken som hører til rommet.
    # (oppgave 6c) Spill den bare hvis musikk_paa er True – ellers slår den seg på igjen i neste rom.
    pass


def finn_ledig_plass():
    """Står helten i en hindring etter et rombytte, flytter vi ham til nærmeste sted
    han kan stå – helst innover i kartet. Ferdig kode, en sikring mot å bli fanget."""
    if kan_gaa(helt, helt.x, helt.y):
        return
    innover = {"hoyre": (1, 0), "venstre": (-1, 0), "ned": (0, 1), "opp": (0, -1)}.get(ut_av, (0, 1))
    side = (innover[1], innover[0])
    retninger = [innover, side, (-side[0], -side[1]),
                 (innover[0] + side[0], innover[1] + side[1]), (innover[0] - side[0], innover[1] - side[1])]
    start_x = helt.x
    start_y = helt.y
    for avstand in range(1, 240):
        for r in retninger:
            x = start_x + r[0] * avstand
            y = start_y + r[1] * avstand
            if 0 <= x <= BREDDE - 16 and -8 <= y <= HOYDE - 24 and kan_gaa(helt, x, y):
                helt.x = x
                helt.y = y
                return


def bytt_rom():
    """Går til rommet ved siden av, og setter helten på motsatt side."""
    global rom
    rom = ROM[rom][ut_av]
    tegn_rom()

    # (steg 2) Sett helten på motsatt side av skjermen i det nye rommet.
    if ut_av == "hoyre":
        helt.x = 0
    elif ut_av == "venstre":
        helt.x = BREDDE - 16
    elif ut_av == "ned":
        helt.y = -8
    elif ut_av == "opp":
        helt.y = HOYDE - 24

    # Står helten i en hindring nå, flytter vi ham til nærmeste ledige plass (ferdig kode)
    finn_ledig_plass()


def overlapper(boks1, boks2):
    """Gir True hvis to bokser (venstre, topp, bredde, hoyde) overlapper hverandre."""
    x1, y1, b1, h1 = boks1
    x2, y2, b2, h2 = boks2
    return x1 < x2 + b2 and x2 < x1 + b1 and y1 < y2 + h2 and y2 < y1 + h1


def kan_gaa(figur, x, y):
    """Gir True hvis figuren kan stå på x, y uten å stå i en hindring."""
    # boks() gir treffboksen (føttene) slik den ville vært hvis figuren sto på x, y
    venstre, topp, bredde, hoyde = figur.boks(x, y)

    # Faste ting (kister, personer) kan man ikke gå gjennom
    for ting in ting_i_rommet:
        if ting.art in FASTE and overlapper(figur.boks(x, y), ting.boks()):
            return False

    hoyre = venstre + bredde - 1
    bunn = topp + hoyde - 1
    hjorner = [(venstre, topp), (hoyre, topp), (venstre, bunn), (hoyre, bunn)]

    for punkt in hjorner:
        rute = rute_ved(punkt[0], punkt[1])     # hvilket tegn i kartet ligger her?
        if rute == None or rute in HINDRINGER:  # None betyr utenfor kartet
            return False
    return True


def gaa():
    """Flytter og animerer helten med piltastene."""
    global retning, gaa_teller, ut_av

    dx = 0          # hvor mye helten skal flytte seg mot høyre (minus = venstre)
    dy = 0          # hvor mye helten skal flytte seg nedover (minus = oppover)

    fart = FART
    if tast_holdes("shift"):
        fart = FART * 2

    # (steg 2) Husk hvilken retning helten går i (variabelen retning).
    if tast_holdes("opp"):
        dy = -fart
        retning = "opp"
    if tast_holdes("ned"):
        dy = fart
        retning = "ned"
    if tast_holdes("venstre"):
        dx = -fart
        retning = "venstre"
    if tast_holdes("hoyre"):
        dx = fart
        retning = "hoyre"

    if dx != 0 or dy != 0:
        # (steg 2) Animer beina: bytt mellom bilde 1, 2, 3 og 4 mens helten går.
        gaa_teller = gaa_teller + 1
        bilde_nr = gaa_teller // 8 % 4 + 1      # 1, 1, ... 2, 2, ... 3, ... 4, ... 1
        helt.bilde = f"helt_{retning}_{bilde_nr}"
    else:
        # (steg 2) Når helten står stille, skal han stå rett opp og ned (bilde 1).
        helt.bilde = f"helt_{retning}_1"

    # Hvor vil helten stå etterpå?
    ny_x = helt.x + dx
    ny_y = helt.y + dy

    # (steg 2) Finn ut om helten går ut av en kant, og hvilken.
    ut_av = None
    if ny_x < 0:
        ut_av = "venstre"
    elif ny_x > BREDDE - 16:
        ut_av = "hoyre"
    elif ny_y < -8:
        ut_av = "opp"
    elif ny_y > HOYDE - 24:
        ut_av = "ned"

    # Ut gjennom en åpen dør (D) i den høye nordveggen: går helten oppover
    # med føttene i døra, går han til rommet over (ferdig kode)
    if dy < 0 and ny_y < 0 and rute_ved(helt.x + 8, helt.y + 16) == "D":
        ut_av = "opp"

    # Inn i hulen: buen over huleinngangen (n) er en hindring. Går helten oppover
    # fra inngangen (H) og inn under buen, går han til rommet over (ferdig kode)
    if dy < 0 and rute_ved(helt.x + 8, ny_y + 16) == "n":
        ut_av = "opp"

    # Finnes det et rom på den siden? Da går vi dit.
    if ut_av in ROM[rom]:
        overgang(bytt_rom)
        return

    # Ellers holder vi helten innenfor skjermen.
    # Øverst får hodet stikke 8 piksler ut, så føttene kan nå den øverste raden.
    if ny_x < 0:
        ny_x = 0
    if ny_x > BREDDE - 16:
        ny_x = BREDDE - 16
    if ny_y < -8:
        ny_y = -8
    if ny_y > HOYDE - 24:
        ny_y = HOYDE - 24

    # Flytt helten bare hvis han kan gå dit
    if kan_gaa(helt, ny_x, helt.y):
        helt.x = ny_x
    if kan_gaa(helt, helt.x, ny_y):
        helt.y = ny_y


def animer_slag():
    """Viser sverdslaget i tre faser. Ferdig kode – den leser bare slag-telleren.
    slag teller ned fra 15: de 3 første bildene er oppsving, de 4 neste hugg, resten etterslag."""
    if slag <= 0:
        return
    if slag > 11:
        fase = 1
    elif slag > 7:
        fase = 2
    else:
        fase = 3
    helt.bilde = f"helt_slag_{retning}_{fase}"
    if sverd != None:
        plass = SVERD_FASER[retning][fase - 1]
        sverd.bilde = f"sverd_{retning}_{fase}"
        if retning == "opp":
            sverd.lag = 0               # slår helten oppover, ligger sverdet bak ham
        else:
            sverd.lag = 1
        sverd.x = helt.x + plass[0]
        sverd.y = helt.y + plass[1]


def kutt_busk(x, y):
    """Kutter busken som står på punktet x, y (hvis det står en busk der)."""
    kol = int(x // RUTE)        # hvilken kolonne og rad i kartet punktet er i
    rad = int(y // RUTE)
    midt_x = kol * RUTE + 8     # midten av ruta, til effektene
    midt_y = rad * RUTE + 8

    # (steg 3) Er det en busk her? Bytt den ut med gress, og lag en blad-effekt.
    if rute_ved(x, y) == "B":
        endre_rute(kol, rad, ".")
        effekt("blader", midt_x, midt_y)

    # (steg 3) Slår du i en stein, skal det komme gnister og lyden "bump".
    if rute_ved(x, y) == "S":
        effekt("gnister", midt_x, midt_y)
        spill_lyd("bump")


def slaa():
    """Svinger sverdet når du trykker mellomrom."""
    global slag, sverd

    if tast_trykket("mellomrom") and slag == 0:
        # Står helten foran noe han kan bruke, bruker han det i stedet for å slå
        if bruk_foran():
            return

        # Start slaget: sett slag til 15, bytt bilde på helten og spill lyden "sverd".
        slag = 15
        helt.bilde = f"helt_slag_{retning}"
        spill_lyd("sverd")

        # (steg 3) Lag sverd-figuren ved siden av helten, i retningen han ser.
        plass = SVERD_PLASS[retning]
        sverd = Figur(f"sverd_{retning}", helt.x + plass[0], helt.y + plass[1])

        # Kutt busken der sverdet treffer
        if sverd != None:
            kutt_busk(sverd.midt_x, sverd.midt_y)

            # Knus krukkene sverdet treffer
            for ting in ting_i_rommet[:]:
                if ting.art == "krukke" and sverd.treffer(ting):
                    knus_krukke(ting)

            # (steg 4) Gå gjennom fiendene. Treffer sverdet en fiende, kall skade_fiende(fiende).
            for fiende in fiender[:]:       # [:] er en kopi, så vi kan fjerne fiender underveis
                if sverd.treffer(fiende):
                    skade_fiende(fiende)

    # (steg 3) Tell slag ned til 0. Når slaget er ferdig, skal sverdet bort.
    if slag > 0:
        slag = slag - 1
        if slag == 0:
            if sverd != None:
                sverd.fjern()
                sverd = None
            helt.bilde = f"helt_{retning}_1"


def skade_fiende(fiende):
    """Fienden blir truffet av sverdet."""
    fiende.glimt(0.15)                              # blir hvit et øyeblikk
    frys(0.05)                                      # hitstop: alt står stille et øyeblikk
    effekt("treff", fiende.midt_x, fiende.midt_y)
    spill_lyd("treff")

    # (steg 4) Trekk fra ett liv. Har fienden 0 liv igjen, skal den forsvinne i en røyksky.
    fiende.liv = fiende.liv - 1
    if fiende.liv <= 0:
        effekt("poff", fiende.midt_x, fiende.midt_y)
        spill_lyd("fiende_borte")
        fiende.fjern()
        fiender.remove(fiende)

        # (steg 6) Trekk et tall fra 1 til 3. Er det 1, slipper fienden et hjerte. Er det 2, en mynt.
        tall = random.randint(1, 3)
        if tall == 1:
            lag_ting("hjerte", fiende.x, fiende.y)
        elif tall == 2:
            lag_ting("mynt", fiende.x, fiende.y)

        if fiende.art == "boss":
            boss_beseiret()
        return

    # Bossen er for tung til å bli slått tilbake
    if fiende.art == "boss":
        if fiende.liv <= 5:
            # (steg 7) Bossen blir sint: rødt bilde og kortere ventetid.
            fiende.animer(["boss_skadet", "boss_2"], fart=10)
            fiende.vent_tid = 30
        return

    # (steg 4) Slå fienden 12 piksler bakover, i retningen helten ser – men ikke inn i en vegg.
    steg = RETNINGER[retning]
    for i in range(12):
        ny_x = fiende.x + steg[0]
        ny_y = fiende.y + steg[1]
        if kan_gaa(fiende, ny_x, ny_y):
            fiende.x = ny_x
            fiende.y = ny_y


def flytt_slim(slim):
    """Slimet hopper rundt på måfå."""
    # (steg 4) Flytt slimet med slim.dx og slim.dy ganger farten – men bare hvis det kan gå dit.
    ny_x = slim.x + slim.dx * slim.fart
    ny_y = slim.y + slim.dy * slim.fart
    if kan_gaa(slim, ny_x, slim.y):
        slim.x = ny_x
    if kan_gaa(slim, slim.x, ny_y):
        slim.y = ny_y

    # (steg 4) Tell ned slim.teller. Når den er 0, velg en ny tilfeldig retning og en ny teller.
    slim.teller = slim.teller - 1
    if slim.teller <= 0:
        slim.dx = random.choice([-1, 0, 1])
        slim.dy = random.choice([-1, 0, 1])
        slim.teller = random.randint(30, 90)


def flytt_flaggermus(flaggermus):
    """Flaggermusa flyr mot helten. Den flyr over alt, så den trenger ikke kan_gaa()."""
    # Vi sikter på midten av helten
    maal_x = helt.x
    maal_y = helt.y + 8

    # (steg 4) Flytt flaggermusa litt nærmere maal_x og maal_y (bruk flaggermus.fart).
    if flaggermus.x < maal_x:
        flaggermus.x = flaggermus.x + flaggermus.fart
    elif flaggermus.x > maal_x:
        flaggermus.x = flaggermus.x - flaggermus.fart
    if flaggermus.y < maal_y:
        flaggermus.y = flaggermus.y + flaggermus.fart
    elif flaggermus.y > maal_y:
        flaggermus.y = flaggermus.y - flaggermus.fart


def vis_liv():
    """Viser riktig bilde på hvert hjerte: fullt, halvt eller tomt."""
    for i in range(len(hjerter)):
        # Hjerte nummer i (0, 1, 2) er fullt hvis liv er minst i * 2 + 2
        # (steg 5) Velg "hud_hjerte_full", "hud_hjerte_halv" eller "hud_hjerte_tom".
        if liv >= i * 2 + 2:
            hjerter[i].bilde = "hud_hjerte_full"
        elif liv == i * 2 + 1:
            hjerter[i].bilde = "hud_hjerte_halv"
        else:
            hjerter[i].bilde = "hud_hjerte_tom"


def skade_helt(skade, fiende):
    """Helten blir skadet av en fiende."""
    global liv, dytt, dytt_x, dytt_y
    liv = liv - skade
    spill_lyd("au")
    helt.blink(1.0)             # blinker i 1 sekund – så lenge kan han ikke skades igjen
    rist_skjerm(0.2, 2)

    # (steg 5) Dytt helten bort fra fienden: sett dytt til 10, og dytt_x og dytt_y til 2 eller -2.
    dytt = 10
    if helt.midt_x < fiende.midt_x:
        dytt_x = -2
    else:
        dytt_x = 2
    if helt.midt_y < fiende.midt_y:
        dytt_y = -2
    else:
        dytt_y = 2

    if liv <= 0:
        game_over()


def bli_dyttet():
    """Flytter helten litt bakover etter at han er truffet."""
    global dytt
    dytt = dytt - 1
    ny_x = helt.x + dytt_x
    ny_y = helt.y + dytt_y
    # Helten skal ikke dyttes ut av skjermen eller inn i en hindring
    if ny_x >= 0 and ny_x <= BREDDE - 16 and kan_gaa(helt, ny_x, helt.y):
        helt.x = ny_x
    if ny_y >= -8 and ny_y <= HOYDE - 24 and kan_gaa(helt, helt.x, ny_y):
        helt.y = ny_y


def sjekk_fiender():
    """Skader helten hvis han kommer borti en fiende."""
    # (steg 5) Gå gjennom fiendene. Treffer helten en fiende, og blinker han ikke, kall skade_helt().
    for fiende in fiender:
        if helt.treffer(fiende) and not helt.blinker:
            skade_helt(FIENDER[fiende.art]["skade"], fiende)


def varsle_lite_liv():
    """Piper én gang i sekundet når helten har ett hjerte eller mindre igjen."""
    global lite_liv_teller
    # (steg 5) Er liv 2 eller mindre (men over 0)? Tell opp, og spill "lite_liv" hvert 60. bilde.
    if liv <= 2 and liv > 0:
        lite_liv_teller = lite_liv_teller + 1
        if lite_liv_teller >= 60:
            spill_lyd("lite_liv")
            lite_liv_teller = 0


def game_over():
    """Helten har ikke mer liv."""
    global tilstand
    # (steg 5) Sett tilstand til "game_over", spill lyden "game_over" og vis game over-skjermen.
    tilstand = "game_over"
    stopp_musikk()
    spill_lyd("game_over")
    game_over_bilde.synlig = True
    game_over_tittel.synlig = True
    game_over_tekst.synlig = True


def start_paa_nytt():
    """Starter på engen igjen med fulle hjerter."""
    global tilstand, liv, rom, retning
    # (steg 5) Gi helten fullt liv, sett ham tilbake på engen, skjul game over-skjermen
    # og sett tilstand tilbake til "spill".
    liv = MAKS_LIV
    rom = "engen"
    retning = "ned"
    helt.x = 5 * RUTE
    helt.y = 6 * RUTE - 8
    helt.bilde = "helt_ned_1"
    game_over_bilde.synlig = False
    game_over_tittel.synlig = False
    game_over_tekst.synlig = False
    tegn_rom()
    tilstand = "spill"


def plukk_opp():
    """Plukker opp mynter og hjerter som helten går på."""
    global liv, mynter
    for ting in ting_i_rommet[:]:
        if helt.treffer(ting):
            if ting.art == "hjerte":
                liv = liv + 2
                if liv > MAKS_LIV:
                    liv = MAKS_LIV
                spill_lyd("hjerte")
                effekt("hjerte", ting.midt_x, ting.midt_y)
                fjern_ting(ting)

            # (steg 6) Plukk opp mynter på samme måte: én mer mynt, lyden "mynt" og effekten "glitter".
            elif ting.art == "mynt":
                mynter = mynter + 1
                spill_lyd("mynt")
                effekt("glitter", ting.midt_x, ting.midt_y)
                fjern_ting(ting)


def vis_hud():
    """Viser antall mynter og nøkler øverst til høyre."""
    mynt_tekst.tekst = f"{mynter:03}"       # :03 betyr alltid tre sifre, som 007
    nokkel_tekst.tekst = str(nokler)


def jubel(bilde):
    """Helten holder noe over hodet og jubler i litt over ett sekund."""
    global tilstand, skatt
    tilstand = "jubel"
    helt.bilde = "helt_jubel"
    skatt = Figur(bilde, helt.x, helt.y - 14, lag=2)
    spill_lyd("skatt")
    etter(1.6, slutt_paa_jubel)        # kall slutt_paa_jubel om 1,6 sekunder


def slutt_paa_jubel():
    global tilstand, skatt
    skatt.fjern()
    skatt = None
    helt.bilde = f"helt_{retning}_1"
    tilstand = "spill"


def aapne_kiste(kiste):
    """Åpner en kiste og gir helten det som ligger i den."""
    global nokler
    innhold = kiste.info[3]
    if innhold == None:
        flytende_tekst("Tom", kiste.midt_x, kiste.y - 4)
        return

    # (steg 6) Åpne kisten: nytt bilde, lyden "kiste", gi helten nøkkelen og la ham juble.
    # Husk også å sette kiste.info[3] til None, så kisten er tom neste gang.
    kiste.bilde = "kiste_aapen"
    spill_lyd("kiste")
    kiste.info[3] = None
    if innhold == "nøkkel":
        nokler = nokler + 1
    jubel(innhold)


def aapne_dor(kol, rad):
    """Helten prøver å åpne en låst dør."""
    global nokler
    x = kol * RUTE + 8
    y = rad * RUTE + 8

    # (steg 6) Har helten en nøkkel? Bruk den: bytt "L" med "D", og spill "laas_opp".
    # Hvis ikke: spill "laast", og vis teksten "Låst!".
    if nokler > 0:
        nokler = nokler - 1
        endre_kart(kol, rad, "D")
        spill_lyd("laas_opp")
        effekt("glitter", x, y)
    else:
        spill_lyd("laast")
        flytende_tekst("Låst!", x, y)


def snakk(hva_som_sies):
    """Starter en samtale. hva_som_sies er en liste med replikker."""
    global tilstand, replikker, replikk_nr
    replikker = hva_som_sies
    replikk_nr = 0
    prat_tekst.tekst = replikker[0]
    prat_tekst.synlig = True
    vindu.synlig = True
    spill_lyd("tekst_pip")
    tilstand = "prat"


def neste_replikk():
    """Viser neste replikk – eller avslutter samtalen etter den siste."""
    global tilstand, replikk_nr
    # (steg 6) Gå til neste replikk. Var det den siste, skal vinduet bort og tilstand bli "spill".
    replikk_nr = replikk_nr + 1
    if replikk_nr < len(replikker):
        prat_tekst.tekst = replikker[replikk_nr]
        spill_lyd("tekst_pip")
    else:
        vindu.synlig = False
        prat_tekst.synlig = False
        tilstand = "spill"


def bruk_foran():
    """Bruker det som står rett foran helten. Gir True hvis det var noe der."""
    # En liten firkant (8 x 8) rett foran helten, midt der sverdet ville vært
    plass = SVERD_PLASS[retning]
    foran = (helt.x + plass[0] + 4, helt.y + plass[1] + 4, 8, 8)

    for ting in ting_i_rommet:
        hele_tingen = (ting.x, ting.y, ting.bredde, ting.hoyde)
        if ting.art in ["kiste", "ragna"] and overlapper(foran, hele_tingen):
            if ting.art == "kiste":
                aapne_kiste(ting)
            elif ting.art == "ragna":
                snakk(RAGNA_SIER)
            return True

    # Står det en låst dør foran helten?
    midt_x = foran[0] + 4
    midt_y = foran[1] + 4
    if rute_ved(midt_x, midt_y) == "L":
        aapne_dor(int(midt_x // RUTE), int(midt_y // RUTE))
        return True

    return False


def knus_krukke(krukke):
    """Krukken knuses i småbiter. Kanskje var det et hjerte inni?"""
    # (steg 7) Lag skår med partikler(), spill lyden "krukke" og fjern krukken.
    # Halvparten av gangene skal det ligge et hjerte der krukken sto.
    partikler(krukke.midt_x, krukke.midt_y, antall=12,
              farger=["#c87850", "#a05830", "#e8a070"], fart=1.5, tyngde=0.1, levetid=0.5)
    spill_lyd("krukke")
    fjern_ting(krukke)
    if random.randint(1, 2) == 1:
        lag_ting("hjerte", krukke.x, krukke.y)


def sjekk_bryter():
    """Trår helten på en bryter, klikker den ned og klossene forsvinner."""
    # Punktet midt under føttene til helten
    x = helt.x + 8
    y = helt.y + 20

    # (steg 7) Står helten på en bryter ("b")? Bytt den til "p" (med endre_kart),
    # spill lyden "bryter" og kall fjern_klosser().
    if rute_ved(x, y) == "b":
        endre_kart(int(x // RUTE), int(y // RUTE), "p")
        spill_lyd("bryter")
        fjern_klosser()


def fjern_klosser():
    """Fjerner alle klossene (K) i rommet."""
    kart = ROM[rom]["kart"]
    # (steg 7) Gå gjennom alle radene og alle kolonnene. Bytt hver "K" med "_", med en poff-effekt.
    for rad in range(len(kart)):
        for kol in range(len(kart[rad])):
            if kart[rad][kol] == "K":
                endre_kart(kol, rad, "_")
                effekt("poff", kol * RUTE + 8, rad * RUTE + 8)
    rist_skjerm(0.3, 2)


def flytt_boss(boss):
    """Slimkongen. Den bytter mellom tre tilstander: vent, hopp og angrip."""
    boss.teller = boss.teller - 1

    if boss.tilstand == "vent":
        # Bossen står stille en stund. Så hopper den mot helten – eller brøler (hver tredje gang).
        if boss.teller <= 0:
            boss.antall_hopp = boss.antall_hopp + 1
            if boss.antall_hopp % 3 == 0:
                boss.tilstand = "angrip"
                boss.teller = 60
                boss.rist(1.0, 2)
                spill_lyd("boss_brol")
            else:
                boss.tilstand = "hopp"
                boss.teller = 40
                # Hvor langt bossen skal flytte seg hvert bilde for å lande der helten står nå
                boss.dx = (helt.midt_x - boss.midt_x) / 40
                boss.dy = (helt.y - 8 - boss.y) / 40

    elif boss.tilstand == "hopp":
        # (steg 7) Flytt bossen med boss.dx og boss.dy (bare hvis den kan gå dit).
        # Når telleren er 0, lander den: rist skjermen, lag effekten "stein" og gå tilbake til "vent".
        if kan_gaa(boss, boss.x + boss.dx, boss.y):
            boss.x = boss.x + boss.dx
        if kan_gaa(boss, boss.x, boss.y + boss.dy):
            boss.y = boss.y + boss.dy
        if boss.teller <= 0:
            rist_skjerm(0.3, 3)
            effekt("stein", boss.midt_x, boss.y + 28)
            boss.tilstand = "vent"
            boss.teller = boss.vent_tid

    elif boss.tilstand == "angrip":
        # (steg 7) Når telleren er 0: lag to slim der bossen står (med lag_fiende), og gå tilbake til "vent".
        if boss.teller <= 0:
            lag_fiende("slim", boss.x, boss.y + 16)
            lag_fiende("slim", boss.x + 16, boss.y + 16)
            boss.tilstand = "vent"
            boss.teller = boss.vent_tid


def boss_beseiret():
    """Bossen er borte! Alle småslimene forsvinner også."""
    stopp_musikk()
    spill_lyd("boss_borte")
    rist_skjerm(0.8, 4)
    blink_skjerm("white", 0.3)
    for fiende in fiender[:]:
        effekt("poff", fiende.midt_x, fiende.midt_y)
        fiende.fjern()
        fiender.remove(fiende)
    ROM[rom]["fiender"] = []        # bossen kommer ikke tilbake
    etter(1.5, seier)


def seier():
    """Helten har vunnet!"""
    global tilstand
    # Gikk spilleren til tittelskjermen fra pausemenyen før dette? Da er det ingen seier (ferdig kode).
    if tilstand != "spill" or rom != "bossrommet":
        return
    tilstand = "seier"
    helt.bilde = "helt_jubel"
    spill_lyd("seier")
    effekt("glitter", helt.midt_x, helt.y)

    brukt = tid() - starttid            # hvor mange sekunder eventyret tok
    tekst = f"Du beseiret Slimkongen på {tid_tekst(brukt)}!"

    # OPPGAVE 5: Er det ny rekord (ingen rekord fra før, eller raskere)? Lagre den,
    # og skriv " NY REKORD!" bak teksten. Ellers: skriv hva rekorden er.
    pass

    prat_tekst.tekst = tekst + " (Trykk mellomrom)"
    prat_tekst.synlig = True
    vindu.synlig = True


def lukk_seiersmelding():
    """Lukker seiersmeldingen og går tilbake til tittelskjermen."""
    vindu.synlig = False
    prat_tekst.synlig = False
    overgang(vis_tittel)


def tid_tekst(sekunder):
    """Gjør et antall sekunder om til tekst med minutter og sekunder, f.eks. 205 -> "3:25"."""
    # OPPGAVE 4: Regn ut hele minutter (//) og sekundene som blir igjen (%). Gi tilbake "minutter:sekunder".
    return str(round(sekunder)) + " sekunder"


def les_rekord():
    """Leser rekorden fra fila. Gir None hvis det ikke finnes noen rekord ennå."""
    try:
        with open(REKORDFIL) as fil:
            return float(fil.read())
    except (OSError, ValueError):       # fila finnes ikke, eller det står noe rart i den
        return None


def lagre_rekord(sekunder):
    """Skriver rekorden til fila."""
    with open(REKORDFIL, "w") as fil:
        fil.write(str(sekunder))


def vis_tittel():
    """Viser tittelskjermen."""
    global tilstand
    tilstand = "tittel"
    tittel_bilde.synlig = True
    tittel_navn.synlig = True
    tittel_under.synlig = True
    trykk_tekst.synlig = True
    rekord_tekst.synlig = True
    for glitter in tittel_glitter:
        glitter.synlig = True
    vis_kart(False)                 # tittelbildet dekker kartet: ikke tegn det
    rekord = les_rekord()
    if rekord == None:
        rekord_tekst.tekst = ""
    else:
        rekord_tekst.tekst = f"Rekord: {tid_tekst(rekord)}"
    if musikk_paa:
        spill_musikk("tittel")


def skjul_tittel():
    tittel_bilde.synlig = False
    tittel_navn.synlig = False
    tittel_under.synlig = False
    trykk_tekst.synlig = False
    rekord_tekst.synlig = False
    for glitter in tittel_glitter:
        glitter.synlig = False
    vis_kart(True)


def nytt_spill():
    """Starter et helt nytt eventyr: urørt verden, fullt liv, ingen mynter."""
    global ROM, rom, liv, mynter, nokler, retning, tilstand, starttid
    ROM = copy.deepcopy(START_ROM)      # en ny kopi, så kister og dører er som før
    rom = "engen"
    liv = MAKS_LIV
    mynter = 0
    nokler = 0
    retning = "ned"
    helt.x = 5 * RUTE
    helt.y = 6 * RUTE - 8
    helt.bilde = "helt_ned_1"
    skjul_tittel()
    tegn_rom()
    starttid = tid()
    tilstand = "spill"


def flytt_fiender():
    """Flytter alle fiendene i rommet."""
    for fiende in fiender:
        if fiende.art == "slim":
            flytt_slim(fiende)
        elif fiende.art == "flaggermus":
            flytt_flaggermus(fiende)
        elif fiende.art == "boss":
            flytt_boss(fiende)


# ---------- PAUSEMENYEN ----------

def vis_pausemeny():
    """Viser pausemenyen over alt annet (ferdig kode)."""
    for ting in PAUSEMENY:
        ting.synlig = True
        ting.legg_overst()          # over HUD-en og alt annet på skjermen
    tegn_pausemeny()


def skjul_pausemeny():
    """Skjuler pausemenyen (ferdig kode)."""
    for ting in PAUSEMENY:
        ting.synlig = False


def tegn_pausemeny():
    """Skriver valgene og flytter pila til det valgte (ferdig kode)."""
    for i in range(len(PAUSEVALG)):
        tekst = PAUSEVALG[i]
        if tekst == "Musikk":
            if musikk_paa:
                tekst = "Musikk: på"
            else:
                tekst = "Musikk: av"
        pause_tekster[i].tekst = tekst
        if i == valg:
            pause_tekster[i].farge = "#f8d850"      # det valgte er gult
        else:
            pause_tekster[i].farge = "white"
    pause_valgt.y = pause_tekster[valg].y - 2
    pause_pil.y = pause_tekster[valg].y - 1


def aapne_pause():
    """Åpner pausemenyen: spillet fryser, og menyen vises."""
    global tilstand, valg
    # OPPGAVE 6a: Sett tilstand til "pause" og valg til 0. Frys spillet med pause(True),
    # og vis menyen med vis_pausemeny().
    pass


def lukk_pause():
    """Lukker pausemenyen, og spillet går videre."""
    global tilstand
    # (oppgave 6a) Gjør det motsatte: pause(False), skjul_pausemeny() og tilstand "spill".
    pass


def styr_pausemeny():
    """Tastene i pausemenyen: Escape lukker, piltastene flytter pila, Enter velger."""
    global valg
    if tast_trykket("escape"):
        lukk_pause()
        return

    # OPPGAVE 6b: Pil ned flytter valget én ned, pil opp én opp. Bruk % så pila
    # hopper rundt: ned fra det nederste valget gir det øverste (og opp fra det øverste
    # gir det nederste). Spill gjerne lyden "tekst_pip".
    pass

    if tast_trykket("enter") or tast_trykket("mellomrom"):
        velg_i_pausemeny()


def velg_i_pausemeny():
    """Gjør det som står på valget pila peker på."""
    global musikk_paa
    hva = PAUSEVALG[valg]           # teksten på valget, f.eks. "Musikk"
    spill_lyd("velg")
    # OPPGAVE 6c: Er hva "Fortsett", lukker du menyen. Er det "Musikk", slår du musikken
    # av eller på (bytt musikk_paa, og bruk stopp_musikk() eller spill_musikk()).
    # Er det "Til tittelskjermen", kaller du til_tittelskjermen().
    pass


def til_tittelskjermen():
    """Avslutter eventyret og går til tittelskjermen (ferdig kode)."""
    global tilstand
    pause(False)
    skjul_pausemeny()
    tilstand = "tittel"
    overgang(vis_tittel)


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Mens skjermen toner over til et nytt rom, skal ingenting skje.
    if i_overgang():
        return

    # Tittelskjermen
    if tilstand == "tittel":
        # OPPGAVE 1: La "Trykk Enter"-teksten blinke: synlig i 0,6 sekunder, borte i 0,4.
        pass

        # OPPGAVE 2: Når spilleren trykker Enter, start et nytt spill med en overgang.
        pass
        return

    # På game over-skjermen venter vi bare på Enter
    if tilstand == "game_over":
        if tast_trykket("enter"):
            overgang(start_paa_nytt)
        return

    # Mens noen snakker, går mellomrom til neste replikk
    if tilstand == "prat":
        if tast_trykket("mellomrom"):
            neste_replikk()
        return

    # Mens helten jubler, står alt stille
    if tilstand == "jubel":
        return

    # Seier! Mellomrom lukker meldingen, og så kan du gå videre.
    if tilstand == "seier":
        if tast_trykket("mellomrom"):
            lukk_seiersmelding()
        return

    # Pausemenyen: alt annet står stille, bare menyen styres
    if tilstand == "pause":
        styr_pausemeny()
        tegn_pausemeny()            # ferdig kode: flytter pila til valget
        return

    # (oppgave 6a) Escape åpner pausemenyen. Etterpå skal ingenting mer skje nå (return).
    pass

    slaa()
    if tilstand != "spill":         # slaa() kan ha startet en samtale eller en jubel
        return

    # Helten skal ikke kunne gå mens han slår eller blir dyttet.
    if dytt > 0:
        bli_dyttet()
    elif slag == 0:
        gaa()

    animer_slag()                   # ferdig kode: viser sverdslaget i tre faser
    flytt_fiender()
    sjekk_fiender()
    plukk_opp()
    sjekk_bryter()
    varsle_lite_liv()
    vis_liv()
    vis_hud()


tegn_rom()
vis_tittel()
start(tittel="Eventyret – steg 8")

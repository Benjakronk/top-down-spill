# ============================================================
#  EVENTYRET – STEG 5: Liv og skade
# ============================================================
#
#  Nå blir det farlig! Fiendene skader helten når de kommer borti
#  ham. Helten har tre hjerter øverst på skjermen, blinker og blir
#  slått bakover når han blir truffet – og mister han alle hjertene,
#  er det GAME OVER.
#
#  Taster:  piltastene = gå   shift = løp   mellomrom = slå
#           Enter = prøv igjen (på game over-skjermen)
#
#  Nytt i dag:
#    - HUD: hjertene øverst er figurer i lag 3, over alt annet
#    - en tilstandsvariabel: tilstand er "spill" eller "game_over",
#      og oppdater() gjør forskjellige ting i hver tilstand
#    - blink(): helten blinker og kan ikke skades så lenge han blinker
#    - rist_skjerm() og lyder når noe vondt skjer
#
#  Liv telles i halve hjerter: liv = 6 er tre fulle hjerter,
#  liv = 5 er to og et halvt hjerte.
#
# ============================================================

from spillmotor import *
import random

BREDDE = 240        # skjermen i piksler
HOYDE = 160


# ---------- KARTENE ----------
# Hvert tegn er én rute. Ordboka RUTER sier hvilket bilde hvert tegn skal ha.
#   .  ,  *   gress (litt forskjellig)      =   sti
#   ~         vann                          B   busk (kan kuttes)
#   h         hekk langs kanten (kan ikke kuttes)
#   S  s      stein (to bilder)             T  t  tre (to slags trær)
#   #  V      fjellvegg (topp og forside)   H   huleinngang
#   Y         tett skog (kan ikke kuttes)
#   M  m      klippe (M = de to øverste radene, m = foten)
#   n         buen over huleinngangen (to ruter høy, stenger: helten går inn i hulen fra H)
#   [  ]      klippekant på sidene av fjellet
#   A         avsats (lav steinkant ned mot engen)

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
    "#": "hulevegg_topp",
    "V": "hulevegg",
    "H": "huleinngang",
    "Y": "skog_stor",                        # tett skog (kan ikke kuttes), et stort mønster
    "M": "klippe_stor",                      # klippen på fjellet: de to øverste radene ...
    "m": "klippe_stor",                      # ... og foten (samme store bilde, så lagene henger sammen)
    "n": "huleinngang_bue_hoy",              # buen over huleinngangen (to ruter høy)
    "[": "fjellside_stor_venstre",           # klippekant på sidene (like høy som skjermen)
    "]": "fjellside_stor_hoyre",
    "A": "avsats",                           # lav steinkant nederst på fjellet
}

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

# Tegn som helten IKKE kan gå gjennom
HINDRINGER = ["S", "s", "B", "h", "~", "T", "#", "V", "Y", "M", "m", "n", "[", "]", "A", "t"]

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

# Egenskapene til hver fiende-art
FIENDER = {
    "slim":       {"liv": 2, "fart": 0.5, "skade": 1, "treffboks": (2, 6, 12, 10)},
    "flaggermus": {"liv": 1, "fart": 0.6, "skade": 1, "treffboks": (2, 3, 12, 10)},
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
tilstand = "spill"  # "spill" eller "game_over"
dytt = 0            # hvor mange bilder igjen helten blir dyttet bakover
dytt_x = 0          # hvor mye helten dyttes hvert bilde
dytt_y = 0
lite_liv_teller = 0 # teller til varsellyden når helten har lite liv


# ---------- HUD (hjertene øverst) ----------
# Ett hjerte for hvert andre liv. Lag 3 betyr at de tegnes over alt annet.
# Mørk bakgrunn bak hjertene, så de synes på alle kart (ferdig kode)
hud_bakgrunn_venstre = Figur("hud_bakgrunn_venstre", 1, 1, lag=3)
hjerter = []
for i in range(MAKS_LIV // 2):
    hjerte = Figur("hud_hjerte_full", 4 + i * 9, 4, lag=3)
    hjerter.append(hjerte)

# Game over-skjermen lages nå, men er usynlig til helten dør
game_over_bilde = Figur("game_over", 0, 0, lag=3)
game_over_bilde.synlig = False
game_over_tittel = Tekst("GAME OVER", 0, 24, farge="white", skygge="#181820", storrelse=2)
game_over_tittel.x = (BREDDE - game_over_tittel.bredde) / 2     # midt på skjermen
game_over_tittel.synlig = False
game_over_tekst = Tekst("Trykk Enter for å prøve igjen", 0, 144, farge="white", skygge="#181820")
game_over_tekst.x = (BREDDE - game_over_tekst.bredde) / 2
game_over_tekst.synlig = False


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

    fiender.append(fiende)


def tegn_rom():
    """Tegner kartet til rommet helten er i, med trær og fiender."""
    global traer, fiender
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


def kan_gaa(figur, x, y):
    """Gir True hvis figuren kan stå på x, y uten å stå i en hindring."""
    # boks() gir treffboksen (føttene) slik den ville vært hvis figuren sto på x, y
    venstre, topp, bredde, hoyde = figur.boks(x, y)
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
        # (steg 3) Start slaget: sett slag til 15, bytt bilde på helten og spill lyden "sverd".
        slag = 15
        helt.bilde = f"helt_slag_{retning}"
        spill_lyd("sverd")

        # (steg 3) Lag sverd-figuren ved siden av helten, i retningen han ser.
        plass = SVERD_PLASS[retning]
        sverd = Figur(f"sverd_{retning}", helt.x + plass[0], helt.y + plass[1])

        # Kutt busken der sverdet treffer
        if sverd != None:
            kutt_busk(sverd.midt_x, sverd.midt_y)

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
        # OPPGAVE 2: Velg "hud_hjerte_full", "hud_hjerte_halv" eller "hud_hjerte_tom".
        pass


def skade_helt(skade, fiende):
    """Helten blir skadet av en fiende."""
    global liv, dytt, dytt_x, dytt_y
    liv = liv - skade
    spill_lyd("au")
    helt.blink(1.0)             # blinker i 1 sekund – så lenge kan han ikke skades igjen
    rist_skjerm(0.2, 2)

    # OPPGAVE 3: Dytt helten bort fra fienden: sett dytt til 10, og dytt_x og dytt_y til 2 eller -2.
    pass

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
    # OPPGAVE 1: Gå gjennom fiendene. Treffer helten en fiende, og blinker han ikke, kall skade_helt().
    pass


def varsle_lite_liv():
    """Piper én gang i sekundet når helten har ett hjerte eller mindre igjen."""
    global lite_liv_teller
    # OPPGAVE 6: Er liv 2 eller mindre (men over 0)? Tell opp, og spill "lite_liv" hvert 60. bilde.
    pass


def game_over():
    """Helten har ikke mer liv."""
    global tilstand
    # OPPGAVE 4: Sett tilstand til "game_over", spill lyden "game_over" og vis game over-skjermen.
    pass


def start_paa_nytt():
    """Starter på engen igjen med fulle hjerter."""
    global tilstand, liv, rom, retning
    # OPPGAVE 5: Gi helten fullt liv, sett ham tilbake på engen, skjul game over-skjermen
    # og sett tilstand tilbake til "spill".
    pass


def flytt_fiender():
    """Flytter alle fiendene i rommet."""
    for fiende in fiender:
        if fiende.art == "slim":
            flytt_slim(fiende)
        elif fiende.art == "flaggermus":
            flytt_flaggermus(fiende)


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Mens skjermen toner over til et nytt rom, skal ingenting skje.
    if i_overgang():
        return

    # På game over-skjermen venter vi bare på Enter
    if tilstand == "game_over":
        if tast_trykket("enter"):
            overgang(start_paa_nytt)
        return

    slaa()

    # Helten skal ikke kunne gå mens han slår eller blir dyttet.
    if dytt > 0:
        bli_dyttet()
    elif slag == 0:
        gaa()

    animer_slag()                   # ferdig kode: viser sverdslaget i tre faser
    flytt_fiender()
    sjekk_fiender()
    varsle_lite_liv()
    vis_liv()


tegn_rom()
start(tittel="Eventyret – steg 5")

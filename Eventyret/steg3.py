# ============================================================
#  EVENTYRET – STEG 3: Sverdet
# ============================================================
#
#  I dag får helten et sverd! Trykk mellomrom, så svinger han
#  sverdet i retningen han ser. Sverdet kan kutte ned busker,
#  så du kan finne nye veier – og det gnistrer når du slår i stein.
#
#  Taster:  piltastene = gå   shift = løp   mellomrom = slå
#
#  Nytt i dag:
#    - tast_trykket(): bare ÉN gang når tasten trykkes ned
#    - en teller som teller NED (slag), så noe varer en kort stund
#    - None: «ingenting» (sverd = None når sverdet ikke vises)
#    - en dictionary med tupler: SVERD_PLASS["ned"] gir (0, 24)
#    - endre_rute(): bytt ut én rute i kartet
#    - effekter og lyd: effekt("blader", x, y) og spill_lyd("sverd")
#
#  Endret fra steg 2:
#    - Fjellet har fått en høy klippe øverst (tegnene M, m, n og H), klippekanter
#      på sidene ([ og ]) og en lav avsats nederst (A).
#
# ============================================================

from spillmotor import *

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


# ---------- HELTEN ----------
# Helten er 16 piksler bred og 24 piksler høy.
# treffboks=(2, 16, 12, 8) betyr at bare føttene kan krasje i ting.

helt = Figur("helt_ned_1", 5 * RUTE, 6 * RUTE - 8, treffboks=(2, 16, 12, 8), skygge=True)

FART = 1            # hvor mange piksler helten går hver gang oppdater() kjøres

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


# ---------- VARIABLER ----------

rom = "engen"       # rommet helten er i nå (som sted i teksteventyret)
retning = "ned"     # "opp", "ned", "venstre" eller "hoyre"
gaa_teller = 0      # teller hvor lenge helten har gått (til animasjonen)
ut_av = None        # hvilken kant helten går ut av skjermen ("venstre", "hoyre", ...)
traer = []          # trærne i rommet
slag = 0            # hvor mange bilder igjen av sverdslaget (0 = slår ikke)
sverd = None        # sverd-figuren mens helten slår, ellers None


# ---------- FUNKSJONER ----------

def tegn_rom():
    """Tegner kartet til rommet helten er i, og setter trær på alle T-er og t-er."""
    global traer
    for tre in traer:           # fjern trærne fra forrige rom
        tre.fjern()
    traer = []

    kart = ROM[rom]["kart"]
    tegn_kart(kart, RUTER, KANTER)

    # Gå gjennom hver rad og hver kolonne i kartet
    for rad in range(len(kart)):
        for kol in range(len(kart[rad])):
            if kart[rad][kol] in TRAER:
                # Treet er 32 x 32 piksler. Stammen skal stå midt i ruta.
                tre = Figur(TRAER[kart[rad][kol]], kol * RUTE - 8, rad * RUTE - 16)
                traer.append(tre)


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
        if rute in HINDRINGER:
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

    # OPPGAVE 5: Er det en busk her? Bytt den ut med gress, og lag en blad-effekt.
    pass

    # OPPGAVE 6: Slår du i en stein, skal det komme gnister og lyden "bump".
    pass


def slaa():
    """Svinger sverdet når du trykker mellomrom."""
    global slag, sverd

    if tast_trykket("mellomrom") and slag == 0:
        # OPPGAVE 1: Start slaget: sett slag til 15, bytt bilde på helten og spill lyden "sverd".
        pass

        # OPPGAVE 2: Lag sverd-figuren ved siden av helten, i retningen han ser.
        pass

        # Kutt busken der sverdet treffer
        if sverd != None:
            kutt_busk(sverd.midt_x, sverd.midt_y)

    # OPPGAVE 3: Tell slag ned til 0. Når slaget er ferdig, skal sverdet bort.
    pass


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Mens skjermen toner over til et nytt rom, skal ingenting skje.
    if i_overgang():
        return

    slaa()

    # OPPGAVE 4: Helten skal ikke kunne gå mens han slår.
    gaa()

    animer_slag()                   # ferdig kode: viser sverdslaget i tre faser


tegn_rom()
start(tittel="Eventyret – steg 3")

# ============================================================
#  EVENTYRET – STEG 2: Animasjon og flere rom
# ============================================================
#
#  I dag får helten liv: han snur seg dit han går, og beina
#  beveger seg. Og verden blir større: går du ut av kanten av
#  skjermen, kommer du til et nytt rom – akkurat som i Zelda.
#
#  Taster:  piltastene = gå   shift = løp
#
#  Nytt i dag:
#    - global: en funksjon som skal ENDRE en variabel utenfor seg selv
#    - animasjon: bytt bilde med en teller, // og %
#    - f-string: f"helt_{retning}_{bilde_nr}" blir for eksempel "helt_ned_2"
#    - rom som en dictionary, og overgang() mellom rommene
#
#  Endret fra steg 1:
#    - Kartet heter nå ENGEN og tegnes av funksjonen tegn_rom().
#    - Trær (T og t) er nye: tegn_rom() setter et tre på hver T og t i kartet.
#    - Helten kan gå til y = -8 øverst (hodet stikker litt ut), så
#      føttene når den øverste raden i kartet. Det trengs for å finne
#      åpningene øverst i kartet.
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
}

# Myke kanter der stien og vannet møter gresset
KANTER = {"=": ("stikant", ".,*"), "~": ("vannkant", ".,*=B")}
# Kanten av skogen (Y) mot gresset, og skyggen skogen kaster på gresset
KANTER["Y"] = ("skogkant", ".,*=BTt")
KANTER["."] = ("skogskygge", "Y")
KANTER[","] = ("skogskygge", "Y")
KANTER["*"] = ("skogskygge", "Y")
# Hekken sett ovenfra der den går langs kanten nedover
KANTER["h"] = ("hekkant", ".,*=BTtSs")

# Tegn som helten IKKE kan gå gjennom
HINDRINGER = ["S", "s", "B", "h", "~", "T", "#", "V", "Y", "t"]

# Trærne er figurer oppå gresset. Ordboka sier hvilket bilde hvert tre-tegn får.
TRAER = {"T": "tre", "t": "tre_2"}

# ---------- ROMMENE ----------
# Hvert rom har et kart, og sier hvilket rom som ligger i hver retning.
# "hoyre": "skogen" betyr: går du ut til høyre, kommer du til skogen.

ROM = {
    "engen":  {"kart": ENGEN, "hoyre": "skogen"},
    "skogen": {"kart": SKOGEN, "venstre": "engen"},
}

# OPPGAVE 6: Lag et nytt rom over engen.
# Skriv kartet FJELLET her, og legg rommet til i ROM.


# ---------- HELTEN ----------
# Helten er 16 piksler bred og 24 piksler høy.
# treffboks=(2, 16, 12, 8) betyr at bare føttene kan krasje i ting.

helt = Figur("helt_ned_1", 5 * RUTE, 6 * RUTE - 8, treffboks=(2, 16, 12, 8), skygge=True)

FART = 1            # hvor mange piksler helten går hver gang oppdater() kjøres


# ---------- VARIABLER ----------

rom = "engen"       # rommet helten er i nå (som sted i teksteventyret)
retning = "ned"     # "opp", "ned", "venstre" eller "hoyre"
gaa_teller = 0      # teller hvor lenge helten har gått (til animasjonen)
ut_av = None        # hvilken kant helten går ut av skjermen ("venstre", "hoyre", ...)
traer = []          # trærne i rommet


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

    # OPPGAVE 5: Sett helten på motsatt side av skjermen i det nye rommet.
    pass

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

    # OPPGAVE 1: Husk hvilken retning helten går i (variabelen retning).
    if tast_holdes("opp"):
        dy = -fart
        # husk retningen her
    if tast_holdes("ned"):
        dy = fart
        # husk retningen her
    if tast_holdes("venstre"):
        dx = -fart
        # husk retningen her
    if tast_holdes("hoyre"):
        dx = fart
        # husk retningen her

    if dx != 0 or dy != 0:
        # OPPGAVE 2: Animer beina: bytt mellom bilde 1, 2, 3 og 4 mens helten går.
        pass
    else:
        # OPPGAVE 3: Når helten står stille, skal han stå rett opp og ned (bilde 1).
        pass

    # Hvor vil helten stå etterpå?
    ny_x = helt.x + dx
    ny_y = helt.y + dy

    # OPPGAVE 4: Finn ut om helten går ut av en kant, og hvilken.
    ut_av = None
    pass

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


# ---------- SPILL-LØKKA ----------

def oppdater():
    # Mens skjermen toner over til et nytt rom, skal ingenting skje.
    if i_overgang():
        return
    gaa()


tegn_rom()
start(tittel="Eventyret – steg 2")

"""
spillmotor.py – en liten spillmotor for top-down-spill
======================================================

Du trenger ikke å endre denne filen. Den sørger for vinduet, bildene,
tastaturet, lyden og effektene, slik at du kan konsentrere deg om selve spillet.

Slik bruker du den:

    from spillmotor import *

    helt = Figur("helt_ned_1", x=32, y=32)

    def oppdater():                 # kjøres 60 ganger i sekundet
        if tast_holdes("hoyre"):
            helt.x = helt.x + 2

    start(tittel="Mitt spill")

Skjermen er 15 × 10 ruter à 16 × 16 piksler (240 × 160, som en Game Boy Advance).

FIGURER, TEKST OG FIRKANTER

    Figur(bilde, x, y)                en figur med et bilde fra mappen bilder/
        .x  .y                        posisjon (øverste venstre hjørne)
        .bilde                        navnet på bildet – bytt det for å animere
        .bredde  .hoyde               størrelsen på bildet
        .midt_x  .midt_y              midtpunktet på figuren
        .synlig                       True eller False
        .treffboks                    (x, y, bredde, hoyde) inni bildet som kan treffes,
                                      f.eks. (2, 16, 12, 8) for bare føttene. None = hele bildet
        .boks(x, y)                   treffboksen hvis figuren sto på x, y:
                                      gir (venstre, topp, bredde, hoyde)
        .treffer(annen)               True hvis treffboksene overlapper
        .skygge                       True gir en liten skygge under føttene
        .lag                          hvilket lag figuren tegnes i (se under)
        .animer(bilder, fart)         bytter bilde automatisk, f.eks.
                                      slim.animer(["slim_1", "slim_2"], fart=12)
        .blink(sekunder)              blinker (f.eks. når helten er skadet)
        .glimt(sekunder, farge)       blir helt hvit et øyeblikk (når noe blir truffet)
        .rist(sekunder, styrke)       rister på stedet
        .fjern()                      fjerner figuren fra spillet
        .legg_overst()                tegner figuren over de andre i samme lag

    Tekst(tekst, x, y, farge, skygge, storrelse, maks_bredde)
        .tekst  .x  .y  .farge  .skygge  .storrelse  .synlig  .lag
        .bredde  .hoyde               størrelsen på teksten
        .fjern()  .legg_overst()      (linjeskift lager du med \n)

    Rektangel(x, y, bredde, hoyde, farge)
        .x  .y  .bredde  .hoyde  .farge  .synlig  .lag  .fjern()  .legg_overst()

    LAG: 0 = bakgrunn, 1 = figurer (standard for Figur), 2 = effekter,
    3 = tekst og firkanter (standard for Tekst og Rektangel). Kartet ligger under alt.
    Figurer i lag 1 tegnes etter hvor føttene står, så den som står lengst
    ned på skjermen, kommer foran. Da kan helten gå bak et tre.

KART

    tegn_kart(kart, ruter)            tegner et kart laget av tekst
    tegn_kart(kart, ruter, kanter)    ... med myke kanter, f.eks.
                                      kanter = {"=": ("stikant", ".,"), "~": ("vannkant", ".,")}
                                      En liste med bilder i ruter gir animerte ruter:
                                      ruter = {"~": ["vann_1", "vann_2", "vann_3"]}
                                      Et rutebilde på f.eks. 32 × 32 er et mønster: hver
                                      rute viser sin egen 16 × 16-bit av det.
                                      Kantbilder: stikant_opp/_ned/_venstre/_hoyre, og
                                      hjørnene stikant_ytre_ov ... stikant_indre_nh.
                                      Bilder som mangler, hoppes over. Finnes
                                      vannkant_opp_2 og _3, er kanten animert som vannet.
    rute_ved(x, y)                    hvilket tegn i kartet som ligger på piksel x, y
    endre_rute(kolonne, rad, tegn)    bytter ut én rute i kartet
    vis_kart(False)                   skjuler kartet (når en skjerm dekker alt), True viser det

TASTATUR

    tast_holdes(navn)                 True så lenge tasten holdes nede
    tast_trykket(navn)                True bare i det øyeblikket tasten trykkes

    Taster: "venstre", "hoyre", "opp", "ned", "mellomrom", "enter", "escape",
    "shift", "ctrl", "tab", "backspace", bokstaver ("a"–"å") og tall ("0"–"9").

EFFEKTER

    effekt(navn, x, y)                en ferdig effekt med midtpunkt i x, y:
                                      "poff", "treff", "glitter", "plask", "stov",
                                      "blader", "gnister", "hjerte", "ild", "vann",
                                      "blad", "lyn", "stein", "slag"
    partikler(x, y, antall, farger, fart, tyngde, levetid, retning, spredning)
                                      lag din egen sprut av små piksler
    flytende_tekst(tekst, x, y, farge) tekst som stiger opp og forsvinner (f.eks. "-3")
    rist_skjerm(sekunder, styrke)     rister hele skjermen
    blink_skjerm(farge, sekunder)     skjermen blinker i en farge
    tone_ut(sekunder, farge)          skjermen toner ut til svart (eller en annen farge)
    tone_inn(sekunder)                skjermen toner inn igjen
    overgang(funksjon, stil)          toner ut, kaller funksjonen og toner inn igjen.
                                      stil="tone" (vanlig) eller stil="kamp" (blink og striper)
    i_overgang()                      True mens en overgang pågår
    frys(sekunder)                    fryser spillet et øyeblikk når et slag treffer
                                      («hitstop»), f.eks. frys(0.05). oppdater() venter,
                                      men skjermen vises, så glimt og risting synes

LYD

    spill_lyd(navn)                   spiller en lyd fra mappen lyder/
    spill_musikk(navn, volum=60)      spiller musikk fra mappen musikk/ om og om igjen
    stopp_musikk()

TID OG ANNET

    etter(sekunder, funksjon)         kaller funksjonen om litt
    tid()                             antall sekunder siden spillet startet
    pause(True)  /  pause(False)      fryser spillet / setter det i gang igjen: animasjoner,
                                      effekter, etter() og tid() står stille, men oppdater()
                                      kjøres fortsatt, så du kan lage en pausemeny
    er_pause()                        True mens spillet står på pause
    bilder_per_sekund()               hvor fort spillet faktisk går
    tregeste_bilde()                  hvor mange ms det tregeste av de siste 60 bildene tok
                                      (over 17 ms: et bilde gikk tapt, over 25 ms: det hakker)
    avslutt()                         lukker spillet
    start(bredde, hoyde, tittel)      starter spillet – helt nederst i programmet

Bildenavn kan skrives med æ, ø og å: "nøkkel" finner fila nokkel.png.
"""

import base64
import math
import os
import random
import struct
import sys
import time
import traceback
import zlib
import tkinter as tk

__all__ = [
    "RUTE", "Figur", "Tekst", "Rektangel",
    "tegn_kart", "rute_ved", "endre_rute",
    "tast_holdes", "tast_trykket",
    "effekt", "EFFEKTER", "partikler", "flytende_tekst",
    "rist_skjerm", "blink_skjerm", "tone_ut", "tone_inn", "overgang", "i_overgang",
    "spill_lyd", "spill_musikk", "stopp_musikk",
    "etter", "tid", "pause", "er_pause", "frys", "bilder_per_sekund", "tregeste_bilde", "vis_kart", "avslutt", "start",
]

RUTE = 16
_BILDER_PER_SEKUND = 60
_MAPPE = os.path.dirname(os.path.abspath(__file__))
_BILDEMAPPE = os.path.join(_MAPPE, "bilder")
_LYDMAPPE = os.path.join(_MAPPE, "lyder")
_MUSIKKMAPPE = os.path.join(_MAPPE, "musikk")


# ----------------------------------------------------------------------
# Feilmeldinger på norsk
# ----------------------------------------------------------------------

class Spillfeil(Exception):
    """En feil med en forklaring som er ment for den som lager spillet."""


def _finnes_ikke(hva, navn, mappe, filtyper):
    if os.path.isdir(mappe):
        navnene = sorted(
            os.path.splitext(f)[0] for f in os.listdir(mappe)
            if os.path.splitext(f)[1].lower() in filtyper
        )
    else:
        navnene = []
    # Foreslå navn som ligner, i stedet for å liste opp alle
    import difflib
    lignende = difflib.get_close_matches(navn, navnene, n=5, cutoff=0.5)
    if lignende:
        hint = "Mente du " + " eller ".join(f'"{n}"' for n in lignende) + "?"
    elif navnene:
        hint = f"Det finnes {len(navnene)} filer i {os.path.basename(mappe)}/, men ingen som ligner."
    else:
        hint = f"Mappen {os.path.basename(mappe)}/ er tom eller mangler."
    return Spillfeil(f'Fant ikke {hva} "{navn}". {hint}')


def _filnavn(navn):
    """Gjør et navn om til et filnavn: små bokstaver og æ/ø/å -> ae/o/aa."""
    return (navn.lower().replace("æ", "ae").replace("ø", "o").replace("å", "aa")
            .replace(" ", "_"))


# ----------------------------------------------------------------------
# Bilder
# ----------------------------------------------------------------------

_bildestorrelser = {}   # navn -> (bredde, hoyde), lest fra fila uten tkinter
_bildecache = {}        # navn -> forstørret tk.PhotoImage
_glimtcache = {}        # (navn, farge) -> forstørret ensfarget silhuett


def _bildenavn(navn):
    if not isinstance(navn, str):
        raise Spillfeil(f"Et bildenavn må være tekst, men fikk {navn!r}.")
    if navn.lower().endswith(".png"):
        navn = navn[:-4]
    return _filnavn(navn)


def _bildesti(navn):
    sti = os.path.join(_BILDEMAPPE, navn + ".png")
    if not os.path.isfile(sti):
        raise _finnes_ikke("bildet", navn, _BILDEMAPPE, {".png"})
    return sti


def _finnes_bilde(navn):
    return os.path.isfile(os.path.join(_BILDEMAPPE, _bildenavn(navn) + ".png"))


def _bildestorrelse(navn):
    if navn not in _bildestorrelser:
        with open(_bildesti(navn), "rb") as fil:
            hode = fil.read(24)
        if hode[:8] != b"\x89PNG\r\n\x1a\n":
            raise Spillfeil(f'Bildet "{navn}" er ikke en ekte PNG-fil.')
        _bildestorrelser[navn] = struct.unpack(">II", hode[16:24])
    return _bildestorrelser[navn]


def _hent_bilde(navn):
    if navn not in _bildecache:
        original = tk.PhotoImage(file=_bildesti(navn))
        _bildecache[navn] = original.zoom(_skala, _skala)
    return _bildecache[navn]


_forhandslast = {"navn": None}


def _forhandslast_bilder(frist):
    """Laster bildene i bilder-mappa i ledig tid mellom bildene (til tidspunktet frist), så spillet
    ikke hakker første gang et bilde vises (å lese en PNG og forstørre den tar litt tid)."""
    navn = _forhandslast["navn"]
    if navn is None:
        try:
            navn = sorted((f[:-4] for f in os.listdir(_BILDEMAPPE) if f.endswith(".png")), reverse=True)
        except OSError:
            navn = []
        _forhandslast["navn"] = navn
    while navn and time.perf_counter() < frist:
        n = navn.pop()
        if n not in _bildecache:
            try:
                b, h = _bildestorrelse(n)
                if b * h > 64 * 64:           # store bakgrunner lastes når de trengs (tar for lang tid)
                    continue
                _hent_bilde(n)
            except (Spillfeil, tk.TclError):
                pass


# Glimt-bildet (en ensfarget silhuett) må lages ved å spørre Tk om hver piksel er gjennomsiktig.
# Det tar tid for store figurer (50 ms for et 64 × 64-monster), så motoren lager det i ledig tid,
# noen rader om gangen, så snart en figur vises. Da er det ferdig før figuren blir truffet.
_glimt_arbeid = {}      # (navn, farge) -> generator som lager silhuetten litt om gangen
_glimt_ko = []


def _lag_glimt(navn, farge):
    original = _hent_bilde(navn)          # forstørret; vi leser hver _skala-te piksel
    s = _skala
    b, h = original.width() // s, original.height() // s
    try:
        piksel = _rgba(farge)
    except tk.TclError:
        raise Spillfeil(f'Kjenner ikke fargen "{farge}".') from None
    tom = bytes(4)
    rader = []
    for y in range(h):
        rader.append(b"".join(tom if original.transparency_get(x * s, y * s) else piksel
                              for x in range(b)))
        yield
    silhuett = tk.PhotoImage(data=base64.b64encode(_png(b, h, rader)), format="png")
    _glimtcache[(navn, farge)] = silhuett.zoom(s, s) if s > 1 else silhuett


def _hent_glimt(navn, farge):
    """En ensfarget silhuett av bildet, til glimt når noe blir truffet."""
    nokkel = (navn, farge)
    if nokkel not in _glimtcache:
        arbeid = _glimt_arbeid.pop(nokkel, None) or _lag_glimt(navn, farge)
        for _ in arbeid:                 # gjør ferdig det som står igjen
            pass
    return _glimtcache[nokkel]


def _bestill_glimt(navn, farge="white"):
    nokkel = (navn, farge)
    if nokkel not in _glimtcache and nokkel not in _glimt_arbeid:
        _glimt_arbeid[nokkel] = _lag_glimt(navn, farge)
        _glimt_ko.append(nokkel)


def _glimt_i_ledig_tid(frist):
    while _glimt_ko and time.perf_counter() < frist:
        nokkel = _glimt_ko[0]
        arbeid = _glimt_arbeid.get(nokkel)
        if arbeid is None:
            _glimt_ko.pop(0)
            continue
        try:
            next(arbeid)
        except StopIteration:
            _glimt_arbeid.pop(nokkel, None)
            _glimt_ko.pop(0)
        except (Spillfeil, tk.TclError):
            _glimt_arbeid.pop(nokkel, None)
            _glimt_ko.pop(0)


def _png(bredde, hoyde, rader):
    """Lager en RGBA-PNG fra rader med bytes (4 per piksel). Tk leser en hel PNG i ett kall, og
    det er mye raskere enn å sette pikslene én og én."""
    def bit(type_, data):
        return (struct.pack(">I", len(data)) + type_ + data
                + struct.pack(">I", zlib.crc32(type_ + data) & 0xFFFFFFFF))
    hode = struct.pack(">IIBBBBB", bredde, hoyde, 8, 6, 0, 0, 0)
    data = zlib.compress(b"".join(b"\x00" + bytes(rad) for rad in rader), 1)
    return b"\x89PNG\r\n\x1a\n" + bit(b"IHDR", hode) + bit(b"IDAT", data) + bit(b"IEND", b"")


def _rgba(farge):
    """Fargen som 4 bytes (rød, grønn, blå, helt dekkende)."""
    r, g, b = (v // 256 for v in _rot.winfo_rgb(farge))
    return bytes((r, g, b, 255))


def _png_en_piksel(r, g, b, a):
    """Lager en PNG-fil med én piksel (brukes til gjennomsiktige skjermtoner)."""
    def bit(type_, data):
        return (struct.pack(">I", len(data)) + type_ + data
                + struct.pack(">I", zlib.crc32(type_ + data) & 0xFFFFFFFF))
    hode = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + bit(b"IHDR", hode)
            + bit(b"IDAT", zlib.compress(bytes([0, r, g, b, a]))) + bit(b"IEND", b""))


# ----------------------------------------------------------------------
# Ting som tegnes
# ----------------------------------------------------------------------

_objekter = []          # alt som tegnes
_teller = [0]           # gir hver ting et nummer, så vi vet hva som kom sist
_stabling = {"forrige": None, "endret": True}


class _Tegnbar:
    _standardlag = 3

    def __init__(self, lag=None):
        self.synlig = True
        self.lag = self._standardlag if lag is None else lag
        self._id = None
        self._tegnet = None
        self._fjernet = False
        _teller[0] += 1
        self._nr = _teller[0]
        _objekter.append(self)

    def fjern(self):
        """Fjerner tingen fra spillet."""
        if self._fjernet:
            return
        self._fjernet = True
        if self in _objekter:
            _objekter.remove(self)
        if _lerret is not None:
            for id_ in self._alle_id():
                _lerret.delete(id_)
        self._id = None

    def legg_overst(self):
        """Tegner tingen over de andre tingene i samme lag."""
        _teller[0] += 1
        self._nr = _teller[0]

    def _alle_id(self):
        return [] if self._id is None else [self._id]

    def _sorteringsnokkel(self):
        if self.lag == 1:
            return (self.lag, self.y + self.hoyde, self._nr)
        return (self.lag, 0, self._nr)

    def _tikk(self):
        pass

    def _synk(self):
        tilstand = self._tilstand()
        if tilstand == self._tegnet:
            return
        if self._id is None:
            self._id = self._lag()
            _stabling["endret"] = True
        self._oppdater_lerret()
        _lerret.itemconfigure(self._id, state="normal" if self._vises() else "hidden")
        self._tegnet = tilstand

    def _vises(self):
        return self.synlig


class Figur(_Tegnbar):
    """En figur med et bilde fra mappen bilder/."""

    _standardlag = 1

    def __init__(self, bilde, x=0, y=0, lag=None, treffboks=None, skygge=False):
        self.bilde = bilde
        self.x = x
        self.y = y
        self.treffboks = treffboks
        self.skygge = skygge
        self._animasjon = None
        self._blink = 0
        self._glimt = 0
        self._glimtfarge = "white"
        self._rist = 0
        self._riststyrke = 0
        self._rist_xy = (0, 0)
        self._skygge_id = None
        super().__init__(lag)

    # --- bilde og størrelse ---

    @property
    def bilde(self):
        return self._bilde

    @bilde.setter
    def bilde(self, navn):
        navn = _bildenavn(navn)
        self.bredde, self.hoyde = _bildestorrelse(navn)
        self._bilde = navn

    @property
    def midt_x(self):
        return self.x + self.bredde / 2

    @property
    def midt_y(self):
        return self.y + self.hoyde / 2

    # --- treff ---

    def boks(self, x=None, y=None):
        """Treffboksen (venstre, topp, bredde, hoyde) hvis figuren sto på x, y."""
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if self.treffboks is None:
            return (x, y, self.bredde, self.hoyde)
        dx, dy, b, h = self.treffboks
        return (x + dx, y + dy, b, h)

    def treffer(self, annen):
        """Gir True hvis treffboksen til denne figuren overlapper med en annen ting."""
        if self._fjernet or getattr(annen, "_fjernet", False):
            return False
        ax, ay, ab, ah = self.boks()
        if hasattr(annen, "boks"):
            bx, by, bb, bh = annen.boks()
        else:
            bx, by, bb, bh = annen.x, annen.y, annen.bredde, annen.hoyde
        return ax < bx + bb and bx < ax + ab and ay < by + bh and by < ay + ah

    # --- effekter på figuren ---

    def animer(self, bilder, fart=10, gjenta=True, fjern_etterpa=False):
        """
        Bytter bilde automatisk. fart er hvor mange bilder i sekundet (av 60)
        hvert bilde vises, så et lavere tall gir raskere animasjon.
        animer(None) stopper animasjonen.
        """
        if bilder is None:
            self._animasjon = None
            return
        if isinstance(bilder, str):
            raise Spillfeil('animer() trenger en liste med bildenavn, f.eks. ["slim_1", "slim_2"].')
        bilder = [_bildenavn(b) for b in bilder]
        for b in bilder:
            _bildestorrelse(b)
        if self._animasjon is not None and self._animasjon["bilder"] == bilder:
            return                          # samme animasjon kjører allerede
        self._animasjon = {"bilder": bilder, "fart": max(1, int(fart)), "teller": 0,
                           "gjenta": gjenta, "fjern": fjern_etterpa}
        self.bilde = bilder[0]

    def blink(self, sekunder=1.0):
        """Figuren blinker en stund, for eksempel etter at den er skadet."""
        self._blink = round(sekunder * _BILDER_PER_SEKUND)

    @property
    def blinker(self):
        """True mens figuren blinker."""
        return self._blink > 0

    def glimt(self, sekunder=0.1, farge="white"):
        """Figuren blir ensfarget et øyeblikk, for eksempel når den blir truffet."""
        self._glimt = max(1, round(sekunder * _BILDER_PER_SEKUND))
        self._glimtfarge = farge

    def rist(self, sekunder=0.3, styrke=2):
        """Figuren rister på stedet."""
        self._rist = round(sekunder * _BILDER_PER_SEKUND)
        self._riststyrke = styrke

    def _tikk(self):
        a = self._animasjon
        if a is not None:
            a["teller"] += 1
            nr = a["teller"] // a["fart"]
            if nr >= len(a["bilder"]):
                if a["gjenta"]:
                    nr %= len(a["bilder"])
                else:
                    self._animasjon = None
                    if a["fjern"]:
                        self.fjern()
                    return
            self.bilde = a["bilder"][nr]
        if self._blink > 0:
            self._blink -= 1
        if self._glimt > 0:
            self._glimt -= 1
        if self._rist > 0:
            self._rist -= 1
            s = self._riststyrke
            self._rist_xy = (random.randint(-s, s), random.randint(-s, s)) if self._rist else (0, 0)

    # --- tegning ---

    def _alle_id(self):
        return [i for i in (self._skygge_id, self._id) if i is not None]

    def _vises(self):
        return self.synlig and not (self._blink > 0 and (self._blink // 4) % 2 == 0)

    def _tilstand(self):
        glimt = self._glimtfarge if self._glimt > 0 else None
        return (round(self.x) + self._rist_xy[0], round(self.y) + self._rist_xy[1],
                self._bilde, self._vises(), glimt, bool(self.skygge))

    def _lag(self):
        return _lerret.create_image(0, 0, anchor="nw")

    def _oppdater_lerret(self):
        x = round(self.x) + self._rist_xy[0]
        y = round(self.y) + self._rist_xy[1]
        _lerret.coords(self._id, x * _skala, y * _skala)
        if self._glimt > 0:
            _lerret.itemconfigure(self._id, image=_hent_glimt(self._bilde, self._glimtfarge))
        else:
            _lerret.itemconfigure(self._id, image=_hent_bilde(self._bilde))
            _bestill_glimt(self._bilde)
        # Skygge under føttene
        if self.skygge:
            sb, sh = _bildestorrelse("skygge")
            if self._skygge_id is None:
                self._skygge_id = _lerret.create_image(0, 0, anchor="nw",
                                                       image=_hent_bilde("skygge"))
                _stabling["endret"] = True
            sx = round(self.x) + (self.bredde - sb) // 2
            sy = round(self.y) + self.hoyde - sh + 1
            _lerret.coords(self._skygge_id, sx * _skala, sy * _skala)
            _lerret.itemconfigure(self._skygge_id, state="normal" if self.synlig else "hidden")
        elif self._skygge_id is not None:
            _lerret.delete(self._skygge_id)
            self._skygge_id = None

    def __repr__(self):
        return f'Figur("{self._bilde}", x={self.x}, y={self.y})'


# ----------------------------------------------------------------------
# Pikselskrift og tekst
# ----------------------------------------------------------------------
# Motorens egen skrift. Store bokstaver er 7 piksler høye og små bokstaver 5.
# g, j, p, q og y går 2 piksler under linja. Alle sifre er like brede, så
# tall står pent under hverandre. Tegn som mangler, vises som □.
# Selve bokstavene ligger helt nederst i denne fila.

def _les_skrift(data):
    linjer = data.strip("\n").split("\n")
    return {linjer[i]: linjer[i + 1:i + 10] for i in range(0, len(linjer), 10)}


_SKRIFT_HOYDE = 9
_LINJEAVSTAND = 12
_MELLOMROM = 3


def _tegnbredde(tegn):
    if tegn == " ":
        return _MELLOMROM
    return len(_SKRIFT.get(tegn, _SKRIFT["□"])[0])


def _linjebredde(linje):
    if not linje:
        return 0
    return sum(_tegnbredde(t) for t in linje) + len(linje) - 1


def _bryt_linjer(tekst, maks_bredde=None):
    linjer = []
    for avsnitt in str(tekst).replace("\t", "    ").split("\n"):
        if maks_bredde is None:
            linjer.append(avsnitt)
            continue
        linje = ""
        for ord_ in avsnitt.split(" "):
            forsok = ord_ if not linje else linje + " " + ord_
            if linje and _linjebredde(forsok) > maks_bredde:
                linjer.append(linje)
                linje = ord_
            else:
                linje = forsok
        linjer.append(linje)
    return linjer


_tekstcache = {}        # (linjer, farge, skygge, storrelse) -> tk-bilde (de siste 64)


def _lag_tekstbilde(linjer, farge, skygge, storrelse):
    """Tekstbildet bygges som én PNG (ett kall til Tk), og de siste 64 tekstene huskes,
    så en replikk eller meny som vises igjen, ikke må lages på nytt."""
    nokkel = (tuple(linjer), farge, skygge, storrelse)
    if nokkel in _tekstcache:
        return _tekstcache[nokkel]
    p = _skala * storrelse
    ekstra = 1 if skygge else 0
    bredde = max(1, max(_linjebredde(l) for l in linjer) + ekstra)
    hoyde = (len(linjer) - 1) * _LINJEAVSTAND + _SKRIFT_HOYDE + ekstra
    try:
        lag = [(_rgba(farge), 0, 0)]
        if skygge:
            sk = _rgba(skygge)
            lag = [(sk, 1, 0), (sk, 0, 1), (sk, 1, 1)] + lag
    except tk.TclError:
        feil = skygge if farge and _er_farge(farge) else farge
        raise Spillfeil(f'Kjenner ikke fargen "{feil}". Bruk et navn som "white" '
                        f'eller en kode som "#f8d048".') from None
    piksler = bytearray(bredde * hoyde * 4)
    for f, dx, dy in lag:
        for nr, linje in enumerate(linjer):
            cx, cy = 0, nr * _LINJEAVSTAND
            for tegn in linje:
                rader = [] if tegn == " " else _SKRIFT.get(tegn, _SKRIFT["□"])
                for ry, rad in enumerate(rader):
                    start = ((cy + ry + dy) * bredde + cx + dx) * 4
                    for rx, c in enumerate(rad):
                        if c == "#":
                            i = start + rx * 4
                            piksler[i:i + 4] = f
                cx += _tegnbredde(tegn) + 1
    rad_lengde = bredde * 4
    rader = [piksler[y * rad_lengde:(y + 1) * rad_lengde] for y in range(hoyde)]
    bilde = tk.PhotoImage(data=base64.b64encode(_png(bredde, hoyde, rader)), format="png")
    if p > 1:
        bilde = bilde.zoom(p, p)
    if len(_tekstcache) >= 64:
        del _tekstcache[next(iter(_tekstcache))]
    _tekstcache[nokkel] = bilde
    return bilde


def _er_farge(farge):
    try:
        _rot.winfo_rgb(farge)
        return True
    except tk.TclError:
        return False


def _sjekk_storrelse(storrelse):
    if not isinstance(storrelse, int) or storrelse < 1:
        raise Spillfeil(f"storrelse må være et helt tall som 1, 2 eller 3, men er {storrelse!r}.")


class Tekst(_Tegnbar):
    """
    Tekst med motorens pikselskrift. x og y er øverste venstre hjørne.

        farge        fargen på bokstavene
        skygge       en farge her gir skygge ned til høyre, som i Pokémon
        storrelse    1 er vanlig, 2 er dobbelt så stor (fint til titler)
        maks_bredde  bryter teksten over flere linjer så den ikke blir bredere

    Linjeskift lager du med \n i teksten.
    """

    def __init__(self, tekst, x=0, y=0, farge="white", skygge=None, storrelse=1,
                 maks_bredde=None, lag=None):
        _sjekk_storrelse(storrelse)
        self.tekst = tekst
        self.x = x
        self.y = y
        self.farge = farge
        self.skygge = skygge
        self.storrelse = storrelse
        self.maks_bredde = maks_bredde
        self._tekstbilde = None
        self._bildenokkel = None
        super().__init__(lag)

    @property
    def linjer(self):
        """Teksten delt opp i linjene slik de vises."""
        maks = None if self.maks_bredde is None else self.maks_bredde / self.storrelse
        return _bryt_linjer(self.tekst, maks)

    @property
    def bredde(self):
        """Hvor bred teksten er i piksler. Fint til å midtstille den."""
        return max(_linjebredde(l) for l in self.linjer) * self.storrelse

    @property
    def hoyde(self):
        """Hvor høy teksten er i piksler."""
        return ((len(self.linjer) - 1) * _LINJEAVSTAND + _SKRIFT_HOYDE) * self.storrelse

    def _tilstand(self):
        return (str(self.tekst), round(self.x), round(self.y), self.farge, self.skygge,
                self.storrelse, self.maks_bredde, self.synlig)

    def _lag(self):
        return _lerret.create_image(0, 0, anchor="nw")

    def _oppdater_lerret(self):
        _lerret.coords(self._id, round(self.x) * _skala, round(self.y) * _skala)
        nokkel = (str(self.tekst), self.farge, self.skygge, self.storrelse, self.maks_bredde)
        if nokkel != self._bildenokkel:
            _sjekk_storrelse(self.storrelse)
            self._tekstbilde = _lag_tekstbilde(self.linjer, self.farge, self.skygge,
                                               self.storrelse)
            _lerret.itemconfigure(self._id, image=self._tekstbilde)
            self._bildenokkel = nokkel


class Rektangel(_Tegnbar):
    """Et fylt rektangel, for eksempel til en tekstboks eller en livsstolpe."""

    def __init__(self, x, y, bredde, hoyde, farge="white", lag=None):
        self.x = x
        self.y = y
        self.bredde = bredde
        self.hoyde = hoyde
        self.farge = farge
        super().__init__(lag)

    def _tilstand(self):
        return (round(self.x), round(self.y), round(self.bredde), round(self.hoyde),
                self.farge, self.synlig)

    def _lag(self):
        return _lerret.create_rectangle(0, 0, 0, 0, width=0)

    def _oppdater_lerret(self):
        x, y = round(self.x) * _skala, round(self.y) * _skala
        b, h = max(0, round(self.bredde)) * _skala, max(0, round(self.hoyde)) * _skala
        _lerret.coords(self._id, x, y, x + b, y + h)
        try:
            _lerret.itemconfigure(self._id, fill=self.farge)
        except tk.TclError:
            raise Spillfeil(f'Kjenner ikke fargen "{self.farge}". Bruk et navn som "white" '
                            f'eller en kode som "#f8d048".') from None


def _stable_om():
    """Legger alt i riktig rekkefølge på skjermen (bare når noe har endret seg)."""
    rekkefolge = sorted(_objekter, key=lambda o: o._sorteringsnokkel())
    ider = []
    for lag in sorted({o.lag for o in rekkefolge} | set(_partikler_per_lag())):
        for o in rekkefolge:
            if o.lag == lag:
                ider.extend(o._alle_id())
        if _partikler_per_lag().get(lag):
            ider.append(f"partikkel{lag}")
    ider.append("overlegg")
    ider.append("feil")
    noekkel = tuple(ider)
    forrige = _stabling["forrige"]
    if noekkel == forrige and not _stabling["endret"]:
        return
    # Alt før første forskjell fra forrige gang ligger allerede riktig, så bare resten løftes.
    # Det sparer mye tegning. Nye ting havner øverst når de lages, så partikler og
    # skjermtoner (som har samme navn i lista hver gang) løftes alltid når noe nytt er laget.
    fra = 0
    if forrige:
        while fra < min(len(noekkel), len(forrige)) and noekkel[fra] == forrige[fra]:
            fra += 1
    if _stabling["endret"]:
        for i, id_ in enumerate(ider):
            if not isinstance(id_, int):
                fra = min(fra, i)
                break
    for id_ in ider[fra:]:
        if isinstance(id_, int) or _lerret.find_withtag(id_):
            _lerret.tag_raise(id_)
    _stabling["forrige"] = noekkel
    _stabling["endret"] = False


# ----------------------------------------------------------------------
# Kart
# ----------------------------------------------------------------------

_kart = {"rader": None, "ruter": None, "kanter": None, "endret": False, "animerte": {},
         "celler": set(), "bilde": None, "bakgrunn": "black", "skjult": False}
_KART_ANIMASJONSFART = 15       # bilder (av 60) mellom hvert bilde i animerte ruter og kanter
_KANTSIDER = (("opp", 0, -1), ("ned", 0, 1), ("venstre", -1, 0), ("hoyre", 1, 0))
_HJORNER = (("ov", -1, -1), ("oh", 1, -1), ("nv", -1, 1), ("nh", 1, 1))
_utsnittcache = {}      # (navn, x, y) -> forstørret 16 × 16-utsnitt av et mønsterbilde
_kantbildecache = {}    # kantbildenavn -> liste med bildenavn (tom hvis bildet mangler)


def _rutebilder(verdi):
    """En rute kan være None, ett bildenavn eller en liste med bildenavn (animert)."""
    if verdi is None:
        return []
    if isinstance(verdi, (list, tuple)):
        return [_bildenavn(v) for v in verdi]
    return [_bildenavn(verdi)]


def _kantbilder(navn):
    """Bildene til ett kant- eller hjørnebilde. Animerte kanter har flere:
    navn, navn_2, navn_3 ...  eller  navn_1, navn_2, navn_3 ...  Mangler bildet: []."""
    if navn not in _kantbildecache:
        if _finnes_bilde(navn + "_1"):
            bilder, nr = [], 1
        elif _finnes_bilde(navn):
            bilder, nr = [navn], 2
        else:
            bilder, nr = [], None
        while nr is not None and _finnes_bilde(f"{navn}_{nr}"):
            bilder.append(f"{navn}_{nr}")
            nr += 1
        _kantbildecache[navn] = bilder
    return _kantbildecache[navn]


def _kantnavn(prefiks):
    """Alle bildene en kant kan ha: fire sider og åtte hjørner."""
    navn = [f"{prefiks}_{side}" for side, _dk, _dr in _KANTSIDER]
    for hjorne, _dk, _dr in _HJORNER:
        navn += [f"{prefiks}_ytre_{hjorne}", f"{prefiks}_indre_{hjorne}"]
    return navn


def tegn_kart(kart, ruter, kanter=None):
    """
    Tegner et kart laget av tekst. Hvert tegn er én rute.

        kart  = ["#####",
                 "#...#",
                 "#####"]
        ruter = {"#": "vegg", ".": "gress"}
        tegn_kart(kart, ruter)

    Et tegn som peker på None, blir ikke tegnet. En liste med bildenavn
    gir en animert rute. Et bilde som er større enn 16 × 16 (f.eks. 32 × 32),
    er et mønster: hver rute viser sin egen 16 × 16-bit av det, så mønsteret
    gjentar seg over kartet uten skjøter.

    kanter legger myke kanter der to slags ruter møtes:

        kanter = {"=": ("stikant", ".,")}

    betyr: på alle =-ruter som har . eller , ved siden av seg, legg bildet
    stikant_opp, stikant_ned, stikant_venstre eller stikant_hoyre oppå.
    Finnes bildene stikant_ytre_ov/oh/nv/nh og stikant_indre_ov/oh/nv/nh,
    brukes de i hjørnene (o = oppe, n = nede, v = venstre, h = høyre).
    En side eller et hjørne som ikke har noe bilde, hoppes over.
    Finnes vannkant_opp_2 (og vannkant_opp_3), er kanten animert i takt
    med de animerte rutene. En rute kan ha flere slags kanter:
    kanter = {"_": [("gulvskygge", "#V"), ("fakkellys", "F")]}.
    """
    for radnr, rad in enumerate(kart):
        for tegn in rad:
            if tegn not in ruter:
                raise Spillfeil(
                    f'Kartet har tegnet "{tegn}" i rad {radnr}, men det står ikke i ruter. '
                    f'Legg til for eksempel  "{tegn}": "gress_1"  i ruter.'
                )
    for verdi in ruter.values():
        for navn in _rutebilder(verdi):
            b, h = _bildestorrelse(navn)
            if b % RUTE or h % RUTE or not b or not h:
                raise Spillfeil(
                    f'Bildet "{navn}" er {b} × {h} piksler. Et bilde i ruter må være '
                    f'16 × 16, eller et mønster der bredden og høyden går opp i 16 (f.eks. 32 × 32).'
                )
    _kantbildecache.clear()
    if kanter:
        for tegn, verdi in kanter.items():
            for prefiks, _naboer in _kantliste(verdi):
                alle = _kantnavn(_bildenavn(prefiks))
                funnet = [b for navn in alle for b in _kantbilder(navn)]
                if not funnet:
                    hint = str(_finnes_ikke("kantbildet", alle[0], _BILDEMAPPE, {".png"}))
                    raise Spillfeil(
                        f'Fant ingen kantbilder for "{prefiks}" (tegnet "{tegn}" i kanter). '
                        f'Lag minst ett av {prefiks}_opp, _ned, _venstre og _hoyre. '
                        + hint.split(". ", 1)[-1])
                for navn in funnet:
                    _bildestorrelse(navn)
    _kart["rader"] = [str(r) for r in kart]
    _kart["ruter"] = dict(ruter)
    _kart["kanter"] = dict(kanter) if kanter else None
    _kart["endret"] = True


def _kantliste(verdi):
    """En kant kan være ("stikant", ".,") eller en liste med flere slike."""
    if isinstance(verdi, list):
        return verdi
    return [verdi]


def rute_ved(x, y):
    """Gir tegnet i kartet som ligger på piksel (x, y), eller None utenfor kartet."""
    rader = _kart["rader"]
    if rader is None:
        raise Spillfeil("rute_ved() virker først etter at du har kalt tegn_kart().")
    kolonne = math.floor(x / RUTE)
    rad = math.floor(y / RUTE)
    if 0 <= rad < len(rader) and 0 <= kolonne < len(rader[rad]):
        return rader[rad][kolonne]
    return None


def endre_rute(kolonne, rad, tegn):
    """Bytter ut én rute i kartet, for eksempel når en dør åpnes."""
    rader = _kart["rader"]
    if rader is None:
        raise Spillfeil("endre_rute() virker først etter at du har kalt tegn_kart().")
    if tegn not in _kart["ruter"]:
        raise Spillfeil(f'Tegnet "{tegn}" står ikke i ruter.')
    if not (0 <= rad < len(rader) and 0 <= kolonne < len(rader[rad])):
        raise Spillfeil(f"Ruten (kolonne {kolonne}, rad {rad}) er utenfor kartet.")
    rader[rad] = rader[rad][:kolonne] + tegn + rader[rad][kolonne + 1:]
    _kart["celler"].update((kolonne + dk, rad + dr) for dk in (-1, 0, 1) for dr in (-1, 0, 1))


def _rutebilde(navn, kolonne, radnr):
    """Bildet som skal vises på ruta. Et mønsterbilde (større enn 16 × 16) gir
    bare 16 × 16-biten som hører til akkurat denne ruta."""
    b, h = _bildestorrelse(navn)
    if (b, h) == (RUTE, RUTE):
        return _hent_bilde(navn)
    x, y = (kolonne * RUTE) % b, (radnr * RUTE) % h
    nokkel = (navn, x, y)
    if nokkel not in _utsnittcache:
        s = _skala
        utsnitt = tk.PhotoImage(width=RUTE * s, height=RUTE * s)
        utsnitt.tk.call(utsnitt, "copy", _hent_bilde(navn),
                        "-from", x * s, y * s, (x + RUTE) * s, (y + RUTE) * s)
        _utsnittcache[nokkel] = utsnitt
    return _utsnittcache[nokkel]


# Ytelse: Tk tegner raskest når det er få bilder på lerretet. Derfor settes hele kartet sammen
# til ETT stort bilde (_kart["bilde"]). Bare animerte ruter og kanter (vann, blomster ...) ligger
# som egne småbilder oppå, og de er få. endre_rute() tegner bare ruta og naboene på nytt.

def _cellelag(kolonne, radnr):
    """Alle lagene på én rute, nederst først. Hvert lag er en liste med tk-bilder (flere = animert)."""
    rader, ruter, kanter = _kart["rader"], _kart["ruter"], _kart["kanter"]
    tegn = rader[radnr][kolonne]
    lag = []
    bilder = _rutebilder(ruter[tegn])
    if bilder:
        lag.append([_rutebilde(b, kolonne, radnr) for b in bilder])
    if kanter and tegn in kanter:
        for prefiks, naboer in _kantliste(kanter[tegn]):
            lag.extend(_kantlag(rader, kolonne, radnr, tegn, _bildenavn(prefiks), naboer))
    return lag


def _tegn_celle(kolonne, radnr):
    """Tegner én rute inn i kartbildet, og legger animerte lag oppå som egne småbilder."""
    merke = f"kartrute{kolonne}_{radnr}"
    for id_ in _lerret.find_withtag(merke):
        _kart["animerte"].pop(id_, None)
    _lerret.delete(merke)
    lag = _cellelag(kolonne, radnr)
    forste_animerte = next((i for i, l in enumerate(lag) if len(l) > 1), len(lag))
    x0, y0 = kolonne * RUTE * _skala, radnr * RUTE * _skala
    bilde = _kart["bilde"]
    bilde.put(_kart["bakgrunn"], to=(x0, y0, x0 + RUTE * _skala, y0 + RUTE * _skala))
    for l in lag[:forste_animerte]:
        bilde.tk.call(bilde, "copy", l[0], "-to", x0, y0)
    nr = _bildenummer[0] // _KART_ANIMASJONSFART           # samme fase som resten
    for l in lag[forste_animerte:]:
        id_ = _lerret.create_image(x0, y0, anchor="nw", image=l[nr % len(l)],
                                   tags=("kart", merke),
                                   state="hidden" if _kart["skjult"] else "normal")
        if len(l) > 1:
            _kart["animerte"][id_] = l


def vis_kart(synlig=True):
    """Skjuler eller viser kartet. Skjul det når en skjerm dekker alt (tittel, kamp),
    så slipper maskinen å tegne et kart ingen ser."""
    _kart["skjult"] = not synlig
    if _lerret is not None:
        _lerret.itemconfigure("kart", state="normal" if synlig else "hidden")


def _bygg_kart():
    """Bygger hele kartet på nytt (etter tegn_kart)."""
    _lerret.delete("kart")
    rader = _kart["rader"]
    hoyde = len(rader)
    bredde = max((len(r) for r in rader), default=0)
    _kart["animerte"] = {}
    _kart["bakgrunn"] = _lerret["background"]
    _kart["bilde"] = tk.PhotoImage(width=max(1, bredde * RUTE * _skala),
                                   height=max(1, hoyde * RUTE * _skala))
    _lerret.create_image(0, 0, anchor="nw", image=_kart["bilde"], tags="kart",
                         state="hidden" if _kart["skjult"] else "normal")
    for radnr, rad in enumerate(rader):
        for kolonne in range(len(rad)):
            _tegn_celle(kolonne, radnr)
    _lerret.tag_lower("kart")           # hele kartet under figurene
    _kart["endret"] = False
    _kart["celler"] = set()


def _oppdater_celler():
    """Tegner rutene som endre_rute() har endret, og naboene deres (kantene kan ha endret seg)."""
    rader = _kart["rader"]
    for kolonne, radnr in sorted(_kart["celler"]):
        if 0 <= radnr < len(rader) and 0 <= kolonne < len(rader[radnr]):
            _tegn_celle(kolonne, radnr)
    _kart["celler"] = set()
    _lerret.tag_lower("kart")


def _kantlag(rader, kolonne, radnr, tegn, prefiks, naboer):
    """Kant- og hjørnebildene på én rute, som lag. Bilder som mangler, hoppes over."""
    def tegn_ved(k, r):
        if 0 <= r < len(rader) and 0 <= k < len(rader[r]):
            return rader[r][k]
        return None

    def er_nabo(dk, dr):
        nabo = tegn_ved(kolonne + dk, radnr + dr)
        return nabo is not None and nabo != tegn and nabo in naboer

    lag = []

    def legg_pa(navn):
        bilder = _kantbilder(navn)
        if bilder:
            lag.append([_hent_bilde(b) for b in bilder])

    for side, dk, dr in _KANTSIDER:
        if er_nabo(dk, dr):
            legg_pa(f"{prefiks}_{side}")
    # Hjørner: <prefiks>_ytre_ov der både «opp» og «venstre» er kant,
    # <prefiks>_indre_ov der bare den skrå naboen oppe til venstre er det. Osv.
    for hjorne, dk, dr in _HJORNER:
        loddrett, vannrett = er_nabo(0, dr), er_nabo(dk, 0)
        if loddrett and vannrett:
            legg_pa(f"{prefiks}_ytre_{hjorne}")
        elif not loddrett and not vannrett and er_nabo(dk, dr):
            legg_pa(f"{prefiks}_indre_{hjorne}")
    return lag


def _animer_kart():
    if _kart["animerte"] and _bildenummer[0] % _KART_ANIMASJONSFART == 0:
        nr = _bildenummer[0] // _KART_ANIMASJONSFART
        for id_, bilder in _kart["animerte"].items():
            _lerret.itemconfigure(id_, image=bilder[nr % len(bilder)])


# ----------------------------------------------------------------------
# Tastatur
# ----------------------------------------------------------------------

_taster_nede = set()
_taster_nye = set()

# tkinter-navn -> norsk navn
_FRA_TKINTER = {
    "left": "venstre", "right": "hoyre", "up": "opp", "down": "ned",
    "space": "mellomrom", "return": "enter", "kp_enter": "enter",
    "escape": "escape", "tab": "tab", "backspace": "backspace",
    "shift_l": "shift", "shift_r": "shift",
    "control_l": "ctrl", "control_r": "ctrl",
    "ae": "æ", "oslash": "ø", "aring": "å",
}
# andre måter å skrive det samme navnet på
_ALIASER = {
    "høyre": "hoyre", "space": "mellomrom", "esc": "escape",
    "left": "venstre", "right": "hoyre", "up": "opp", "down": "ned",
    "return": "enter", "control": "ctrl",
}
_GYLDIGE_TASTER = (
    set(_FRA_TKINTER.values())
    | set("abcdefghijklmnopqrstuvwxyzæøå0123456789")
)


def _tastenavn(navn):
    if not isinstance(navn, str):
        raise Spillfeil(f"Et tastenavn må være tekst, men fikk {navn!r}.")
    navn = _ALIASER.get(navn.lower(), navn.lower())
    if navn not in _GYLDIGE_TASTER:
        raise Spillfeil(
            f'Kjenner ikke tasten "{navn}". Prøv for eksempel "venstre", "hoyre", '
            f'"opp", "ned", "mellomrom", "enter" eller en bokstav.'
        )
    return navn


def _tast_ned(hendelse):
    navn = hendelse.keysym.lower()
    navn = _FRA_TKINTER.get(navn, navn)
    if navn not in _taster_nede:      # Windows gjentar tasten når den holdes nede
        _taster_nye.add(navn)
    _taster_nede.add(navn)


def _tast_opp(hendelse):
    navn = hendelse.keysym.lower()
    _taster_nede.discard(_FRA_TKINTER.get(navn, navn))


def _mistet_fokus(_hendelse):
    _taster_nede.clear()


def tast_holdes(navn):
    """True så lenge tasten holdes nede. Fint til å gå."""
    return _tastenavn(navn) in _taster_nede


def tast_trykket(navn):
    """True bare i det øyeblikket tasten trykkes ned. Fint til å slå eller velge i en meny."""
    return _tastenavn(navn) in _taster_nye


# ----------------------------------------------------------------------
# Effekter: partikler
# ----------------------------------------------------------------------

_partikler = []


def _partikler_per_lag():
    lag = {}
    for p in _partikler:
        lag[p["lag"]] = True
    return lag


def partikler(x, y, antall=8, farger=("white",), fart=1.0, tyngde=0.0, levetid=0.5,
              retning=None, spredning=360, storrelse=1, lag=2):
    """
    Lager en sprut av små piksler fra punktet (x, y).

        antall     hvor mange piksler
        farger     en liste med farger å velge tilfeldig fra
        fart       hvor fort de flyr ut (piksler per bilde)
        tyngde     positiv: faller ned, negativ: stiger opp
        levetid    hvor mange sekunder de lever
        retning    vinkel i grader (0 = høyre, 90 = opp, 180 = venstre, 270 = ned)
        spredning  hvor mange grader de spres over (360 = alle veier)
        storrelse  hvor store pikslene er
    """
    if isinstance(farger, str):
        farger = [farger]
    for _ in range(int(antall)):
        if retning is None:
            vinkel = random.uniform(0, 360)
        else:
            vinkel = retning + random.uniform(-spredning / 2, spredning / 2)
        v = math.radians(vinkel)
        f = fart * random.uniform(0.4, 1.0)
        liv = max(1, round(levetid * _BILDER_PER_SEKUND * random.uniform(0.7, 1.0)))
        _partikler.append({
            "x": float(x), "y": float(y),
            "vx": math.cos(v) * f, "vy": -math.sin(v) * f,
            "tyngde": tyngde, "liv": liv, "maks": liv,
            "farge": random.choice(list(farger)), "storrelse": storrelse,
            "lag": lag, "id": None,
        })


def _oppdater_partikler():
    for p in list(_partikler):
        p["liv"] -= 1
        if p["liv"] <= 0:
            if p["id"] is not None:
                _lerret.delete(p["id"])
            _partikler.remove(p)
            continue
        p["vy"] += p["tyngde"]
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        s = p["storrelse"]
        x0, y0 = round(p["x"] - s / 2) * _skala, round(p["y"] - s / 2) * _skala
        if p["id"] is None:
            try:
                p["id"] = _lerret.create_rectangle(
                    x0, y0, x0 + s * _skala, y0 + s * _skala, width=0, fill=p["farge"],
                    tags=("partikkel", f"partikkel{p['lag']}"))
            except tk.TclError:
                _partikler.remove(p)
                raise Spillfeil(f'Kjenner ikke fargen "{p["farge"]}".') from None
            _stabling["endret"] = True
        else:
            _lerret.coords(p["id"], x0, y0, x0 + s * _skala, y0 + s * _skala)
        # Blinker mot slutten av livet
        if p["liv"] < p["maks"] * 0.3:
            _lerret.itemconfigure(p["id"], state="hidden" if p["liv"] % 4 < 2 else "normal")


# ----------------------------------------------------------------------
# Effekter: ferdige effekter
# ----------------------------------------------------------------------

# Hver effekt kan ha
#   "bilder":    starten på bildenavnene, f.eks. "fx_poff" for fx_poff_1, fx_poff_2, ...
#   "fart":      hvor mange bilder (av 60) hvert effektbilde vises
#   "partikler": innstillinger til partikler()
#   "rist":      rister skjermen så mye
#   "blink":     skjermen blinker i denne fargen
# Du kan lage dine egne: EFFEKTER["regnbue"] = {"partikler": {...}}
EFFEKTER = {
    "poff":    {"bilder": "fx_poff", "fart": 5,
                "partikler": {"antall": 6, "farger": ["#f8f8f8", "#b0b0c0"], "fart": 0.7,
                              "levetid": 0.4}},
    "treff":   {"bilder": "fx_treff", "fart": 3,
                "partikler": {"antall": 8, "farger": ["#f8f8f8", "#f8e070"], "fart": 1.8,
                              "levetid": 0.25}},
    "glitter": {"bilder": "fx_glitter", "fart": 6,
                "partikler": {"antall": 6, "farger": ["#f8f8c0", "#f8e070", "#f8f8f8"],
                              "fart": 0.5, "tyngde": -0.02, "levetid": 0.7}},
    "plask":   {"bilder": "fx_plask", "fart": 5,
                "partikler": {"antall": 8, "farger": ["#b8e8f8", "#68a8f0"], "fart": 1.4,
                              "tyngde": 0.1, "levetid": 0.5, "retning": 90, "spredning": 120}},
    "stov":    {"bilder": "fx_stov", "fart": 5},
    "blader":  {"partikler": {"antall": 10, "farger": ["#70b040", "#488c38", "#a8d058"],
                              "fart": 1.2, "tyngde": 0.04, "levetid": 0.7,
                              "retning": 90, "spredning": 160}},
    "gnister": {"partikler": {"antall": 10, "farger": ["#f8f8c0", "#f8e070", "#f8a040"],
                              "fart": 2.0, "tyngde": 0.08, "levetid": 0.35}},
    "hjerte":  {"bilder": "fx_hjerte", "fart": 8,
                "partikler": {"antall": 6, "farger": ["#f87858", "#f8b890"], "fart": 0.4,
                              "tyngde": -0.03, "levetid": 0.8}},
    "ild":     {"bilder": "fx_ild", "fart": 5, "rist": 2,
                "partikler": {"antall": 14, "farger": ["#f8d880", "#f8a040", "#e86820"],
                              "fart": 1.2, "tyngde": -0.05, "levetid": 0.6}},
    "vann":    {"bilder": "fx_vann", "fart": 5,
                "partikler": {"antall": 14, "farger": ["#b8e8f8", "#68a8f0", "#3878d0"],
                              "fart": 1.6, "tyngde": 0.1, "levetid": 0.6}},
    "blad":    {"bilder": "fx_blad", "fart": 5,
                "partikler": {"antall": 12, "farger": ["#88c860", "#50a048", "#a8d058"],
                              "fart": 1.3, "tyngde": 0.03, "levetid": 0.8}},
    "lyn":     {"bilder": "fx_lyn", "fart": 4, "rist": 3, "blink": "#f8f8c0",
                "partikler": {"antall": 10, "farger": ["#f8f8c0", "#f8e070"], "fart": 2.2,
                              "levetid": 0.3}},
    "stein":   {"bilder": "fx_stein", "fart": 6, "rist": 4,
                "partikler": {"antall": 12, "farger": ["#a8b0c8", "#7880a0", "#b88858"],
                              "fart": 1.6, "tyngde": 0.12, "levetid": 0.6,
                              "retning": 90, "spredning": 140}},
    "slag":    {"bilder": "fx_slag", "fart": 4, "rist": 2,
                "partikler": {"antall": 8, "farger": ["#f8f8f8", "#e0e8f0"], "fart": 1.8,
                              "levetid": 0.25}},
}


def _fx_bilder(prefiks):
    bilder = []
    nr = 1
    while os.path.isfile(os.path.join(_BILDEMAPPE, f"{prefiks}_{nr}.png")):
        bilder.append(f"{prefiks}_{nr}")
        nr += 1
    if not bilder:
        raise _finnes_ikke("effektbildene", f"{prefiks}_1", _BILDEMAPPE, {".png"})
    return bilder


def effekt(navn, x, y, lag=2):
    """Spiller av en ferdig effekt med midtpunkt i (x, y). Se EFFEKTER for navnene."""
    nokkel = _filnavn(navn) if isinstance(navn, str) else navn
    if nokkel not in EFFEKTER:
        import difflib
        lignende = difflib.get_close_matches(str(nokkel), list(EFFEKTER), n=3)
        hint = ("Mente du " + " eller ".join(f'"{n}"' for n in lignende) + "?") if lignende \
            else "Disse finnes: " + ", ".join(f'"{n}"' for n in EFFEKTER)
        raise Spillfeil(f'Kjenner ikke effekten "{navn}". {hint}')
    oppskrift = EFFEKTER[nokkel]
    if "bilder" in oppskrift:
        bilder = _fx_bilder(oppskrift["bilder"])
        b, h = _bildestorrelse(bilder[0])
        fx = Figur(bilder[0], x - b // 2, y - h // 2, lag=lag)
        fx.animer(bilder, fart=oppskrift.get("fart", 5), gjenta=False, fjern_etterpa=True)
    if "partikler" in oppskrift:
        partikler(x, y, lag=lag, **oppskrift["partikler"])
    if oppskrift.get("rist"):
        rist_skjerm(0.25, oppskrift["rist"])
    if oppskrift.get("blink"):
        blink_skjerm(oppskrift["blink"], 0.15)


class _FlytendeTekst(Tekst):
    def __init__(self, tekst, x, y, farge, skygge, sekunder):
        super().__init__(str(tekst), 0, y, farge=farge, skygge=skygge, lag=3)
        self.x = round(x - self.bredde / 2)
        self._liv = round(sekunder * _BILDER_PER_SEKUND)
        self._maks = self._liv

    def _tikk(self):
        self._liv -= 1
        alder = self._maks - self._liv
        if alder < 20:
            self.y -= 0.6 if alder < 10 else 0.25
        if self._liv < self._maks * 0.3:
            self.synlig = self._liv % 4 >= 2
        if self._liv <= 0:
            self.fjern()


def flytende_tekst(tekst, x, y, farge="white", skygge="#181820", sekunder=0.9):
    """Tekst som stiger litt opp og forsvinner, for eksempel skade: flytende_tekst("-3", x, y)."""
    _FlytendeTekst(tekst, x, y, farge, skygge, sekunder)


# ----------------------------------------------------------------------
# Effekter: hele skjermen
# ----------------------------------------------------------------------

_skjerm = {
    "rist": 0, "riststyrke": 0, "forskyvning": (0, 0),
    "tone": None,       # {"farge", "fra", "til", "tid", "t", "ferdig"}
    "tone_alfa": 0.0, "tone_farge": "black",
    "blink": None,      # {"farge", "tid", "t"}
    "overgang": None,   # {"stil", "fase", "t", "funksjon", ...}
}
_overleggcache = {}
_overlegg_id = {"tone": None, "blink": None}
_ALFA_TRINN = 16


# Ytelse: et halvgjennomsiktig bilde over hele skjermen er tungt for Tk (ca. 20 ms per tegning på
# en vanlig PC, mer på en svak). Motoren bruker derfor bare 8 trinn i toningen, og mister spillet
# bilder mens skjermen toner, bytter den til en «gardin»: to helt dekkende felt som vokser inn fra
# toppen og bunnen. De er vanlige rektangler og koster nesten ingenting å tegne.
_overlegg_modus = {"modus": "alfa", "trege": 0, "delvis": False}
_overlegg_gardin = {"tone": None, "blink": None}


def _overleggbilde(farge, trinn):
    nokkel = (farge, trinn)
    if nokkel not in _overleggcache:
        try:
            r, g, b = (v // 256 for v in _rot.winfo_rgb(farge))
        except tk.TclError:
            raise Spillfeil(f'Kjenner ikke fargen "{farge}".') from None
        alfa = round(255 * trinn / _ALFA_TRINN)
        data = base64.b64encode(_png_en_piksel(r, g, b, alfa))
        en = tk.PhotoImage(data=data, format="png")
        _overleggcache[nokkel] = en.zoom(int(_lerret["width"]), int(_lerret["height"]))
    return _overleggcache[nokkel]


def _vis_gardin(hvilket, farge, alfa):
    """Toning for trege maskiner: to dekkende felt fra toppen og bunnen (andel alfa av skjermen)."""
    ider = _overlegg_gardin[hvilket]
    if ider is None:
        ider = (_lerret.create_rectangle(0, 0, 0, 0, width=0, tags="overlegg"),
                _lerret.create_rectangle(0, 0, 0, 0, width=0, tags="overlegg"))
        _overlegg_gardin[hvilket] = ider
        _stabling["endret"] = True
    bredde, hoyde = int(_lerret["width"]), int(_lerret["height"])
    if hvilket == "blink":                   # et blink blir et kort, helt dekkende glimt
        alfa = 1.0 if alfa > 0.5 else 0.0
    halv = round(hoyde / _skala * alfa / 2) * _skala           # hele spillpiksler
    if alfa >= 0.999:
        halv = hoyde
    try:
        _lerret.itemconfigure(ider[0], fill=farge, state="normal" if halv else "hidden")
        _lerret.itemconfigure(ider[1], fill=farge, state="normal" if halv else "hidden")
    except tk.TclError:
        raise Spillfeil(f'Kjenner ikke fargen "{farge}".') from None
    _lerret.coords(ider[0], 0, 0, bredde, halv)
    _lerret.coords(ider[1], 0, hoyde - halv, bredde, hoyde)


def _vis_overlegg(hvilket, farge, alfa):
    if _overlegg_modus["modus"] == "gardin":
        _vis_gardin(hvilket, farge, alfa)
        return
    trinn = max(0, min(_ALFA_TRINN, 2 * round(alfa * _ALFA_TRINN / 2)))     # 8 trinn
    id_ = _overlegg_id[hvilket]
    if trinn == 0:
        if id_ is not None:
            _lerret.itemconfigure(id_, state="hidden")
        return
    if trinn < _ALFA_TRINN:
        _overlegg_modus["delvis"] = True
    bilde = _overleggbilde(farge, trinn)
    if id_ is None:
        id_ = _lerret.create_image(0, 0, anchor="nw", image=bilde, tags="overlegg")
        _overlegg_id[hvilket] = id_
        _stabling["endret"] = True
    _lerret.itemconfigure(id_, image=bilde, state="normal")


def _sjekk_overleggfart():
    """Mistet spillet bilder tre ganger mens skjermen tonet, bytter motoren til gardin-toning."""
    if _overlegg_modus["delvis"] and _overlegg_modus["modus"] == "alfa" and len(_maletider) > 1:
        if _maletider[-1] - _maletider[-2] > 0.022:      # et bilde gikk tapt
            _overlegg_modus["trege"] += 1
            if _overlegg_modus["trege"] >= 3:
                _overlegg_modus["modus"] = "gardin"
                for id_ in _overlegg_id.values():
                    if id_ is not None:
                        _lerret.itemconfigure(id_, state="hidden")
    _overlegg_modus["delvis"] = False


def rist_skjerm(sekunder=0.3, styrke=3):
    """Rister hele skjermen, for eksempel når noe tungt treffer bakken."""
    _skjerm["rist"] = round(sekunder * _BILDER_PER_SEKUND)
    _skjerm["riststyrke"] = styrke


def blink_skjerm(farge="white", sekunder=0.15):
    """Skjermen blinker kort i en farge."""
    _skjerm["blink"] = {"farge": farge, "tid": max(1, round(sekunder * _BILDER_PER_SEKUND)), "t": 0}


def tone_ut(sekunder=0.5, farge="black", ferdig=None):
    """Skjermen toner ut til en farge og blir værende slik til du kaller tone_inn()."""
    _skjerm["tone"] = {"farge": farge, "fra": _skjerm["tone_alfa"], "til": 1.0,
                       "tid": max(1, round(sekunder * _BILDER_PER_SEKUND)), "t": 0,
                       "ferdig": ferdig}
    _skjerm["tone_farge"] = farge


def tone_inn(sekunder=0.5, ferdig=None):
    """Skjermen toner inn igjen etter tone_ut()."""
    _skjerm["tone"] = {"farge": _skjerm["tone_farge"], "fra": _skjerm["tone_alfa"], "til": 0.0,
                       "tid": max(1, round(sekunder * _BILDER_PER_SEKUND)), "t": 0,
                       "ferdig": ferdig}


def overgang(funksjon, stil="tone", sekunder=0.8):
    """
    Toner ut, kaller funksjon() mens skjermen er svart, og toner inn igjen.
    Fint til å bytte rom eller gå til kampskjermen.

        stil="tone"   vanlig toning til svart
        stil="kamp"   skjermen blinker og svarte striper feier inn (som før en kamp)
    """
    if stil not in ("tone", "kamp"):
        raise Spillfeil(f'Kjenner ikke overgangen "{stil}". Bruk "tone" eller "kamp".')
    if not callable(funksjon):
        raise Spillfeil("overgang() trenger en funksjon, for eksempel overgang(gaa_til_kamp). "
                        "Husk: uten parenteser bak navnet.")
    halv = sekunder / 2
    if stil == "tone":
        _skjerm["overgang"] = {"stil": stil}
        tone_ut(halv, "black", ferdig=lambda: (funksjon(), tone_inn(halv, ferdig=_overgang_ferdig)))
    else:
        _skjerm["overgang"] = {"stil": stil, "fase": "blink", "t": 0, "funksjon": funksjon,
                               "halv": halv, "striper": []}


def _overgang_ferdig():
    _skjerm["overgang"] = None


def i_overgang():
    """True mens en overgang pågår."""
    return _skjerm["overgang"] is not None


def _oppdater_kampovergang(o):
    o["t"] += 1
    if o["fase"] == "blink":
        # Tre raske hvite blink
        blink_paa = (o["t"] // 5) % 2 == 0
        _vis_overlegg("blink", "white", 0.75 if blink_paa else 0.0)
        if o["t"] >= 30:
            _vis_overlegg("blink", "white", 0.0)
            o["fase"], o["t"] = "striper", 0
    elif o["fase"] == "striper":
        bredde = int(_lerret["width"])
        stripehoyde = 8 * _skala
        antall = int(_lerret["height"]) // stripehoyde + 1
        if not o["striper"]:
            for i in range(antall):
                o["striper"].append(_lerret.create_rectangle(
                    0, 0, 0, 0, fill="black", width=0, tags="overlegg"))
            _stabling["endret"] = True
        varighet = max(1, round(o["halv"] * _BILDER_PER_SEKUND))
        andel = min(1.0, o["t"] / varighet)
        lengde = andel * bredde
        for i, id_ in enumerate(o["striper"]):
            y0 = i * stripehoyde
            if i % 2 == 0:
                _lerret.coords(id_, 0, y0, lengde, y0 + stripehoyde)
            else:
                _lerret.coords(id_, bredde - lengde, y0, bredde, y0 + stripehoyde)
        if andel >= 1.0:
            # Helt svart: bytt til svart tone, fjern stripene og kall funksjonen
            _skjerm["tone_alfa"] = 1.0
            _skjerm["tone_farge"] = "black"
            _vis_overlegg("tone", "black", 1.0)
            for id_ in o["striper"]:
                _lerret.delete(id_)
            o["striper"] = []
            o["fase"] = "inn"
            o["funksjon"]()
            tone_inn(o["halv"], ferdig=_overgang_ferdig)


def _oppdater_skjerm():
    # Toning
    tone = _skjerm["tone"]
    if tone is not None:
        tone["t"] += 1
        andel = min(1.0, tone["t"] / tone["tid"])
        _skjerm["tone_alfa"] = tone["fra"] + (tone["til"] - tone["fra"]) * andel
        _vis_overlegg("tone", tone["farge"], _skjerm["tone_alfa"])
        if andel >= 1.0:
            _skjerm["tone"] = None
            if tone["ferdig"] is not None:
                tone["ferdig"]()
    # Blink
    blink = _skjerm["blink"]
    if blink is not None:
        blink["t"] += 1
        alfa = 0.8 * (1 - blink["t"] / blink["tid"])
        _vis_overlegg("blink", blink["farge"], alfa)
        if blink["t"] >= blink["tid"]:
            _skjerm["blink"] = None
            _vis_overlegg("blink", blink["farge"], 0)
    # Kampovergang
    o = _skjerm["overgang"]
    if o is not None and o["stil"] == "kamp" and o.get("fase") in ("blink", "striper"):
        _oppdater_kampovergang(o)


def _flytt_skjerm():
    """Flytter alt på skjermen litt når den rister."""
    gammel = _skjerm["forskyvning"]
    if _skjerm["rist"] > 0:
        _skjerm["rist"] -= 1
        s = _skjerm["riststyrke"]
        ny = (random.randint(-s, s), random.randint(-s, s)) if _skjerm["rist"] else (0, 0)
    else:
        ny = (0, 0)
    if ny != gammel:
        _lerret.move("all", (ny[0] - gammel[0]) * _skala, (ny[1] - gammel[1]) * _skala)
        _skjerm["forskyvning"] = ny


def _tilbakestill_skjermflytt():
    dx, dy = _skjerm["forskyvning"]
    if (dx, dy) != (0, 0):
        _lerret.move("all", -dx * _skala, -dy * _skala)
        _skjerm["forskyvning"] = (0, 0)


# ----------------------------------------------------------------------
# Lyd (Windows)
# ----------------------------------------------------------------------

try:
    import ctypes
    _winmm = ctypes.windll.winmm
except (ImportError, AttributeError):
    _winmm = None           # ikke Windows: spillet virker, men er stille

_lyder = {}             # navn -> MCI-alias
_musikk = {"navn": None}
_lyd_advart = set()


def _mci(kommando):
    if _winmm is None:
        return ""
    svar = ctypes.create_unicode_buffer(256)
    feilkode = _winmm.mciSendStringW(kommando, svar, 255, None)
    if feilkode:
        melding = ctypes.create_unicode_buffer(256)
        _winmm.mciGetErrorStringW(feilkode, melding, 255)
        raise Spillfeil(f"Lydfeil: {melding.value}")
    return svar.value


def _lydsti(mappe, navn, hva):
    for endelse in (".wav", ".mp3"):
        sti = os.path.join(mappe, navn + endelse)
        if os.path.isfile(sti):
            return sti
    raise _finnes_ikke(hva, navn, mappe, {".wav", ".mp3"})


def _rent_navn(navn):
    if not isinstance(navn, str):
        raise Spillfeil(f"Et lydnavn må være tekst, men fikk {navn!r}.")
    return _filnavn(os.path.splitext(navn)[0])


def _last_lyd(navn):
    sti = _lydsti(_LYDMAPPE, navn, "lyden")
    alias = f"lyd{len(_lyder)}"
    _mci(f'open "{sti}" type mpegvideo alias {alias}')
    _lyder[navn] = alias


def spill_lyd(navn):
    """Spiller en lyd fra mappen lyder/. Flere lyder kan spilles samtidig."""
    navn = _rent_navn(navn)
    if navn not in _lyder:
        _last_lyd(navn)
    try:
        _mci(f"play {_lyder[navn]} from 0")
    except Spillfeil as feil:
        if navn not in _lyd_advart:
            _lyd_advart.add(navn)
            print(f'Klarte ikke å spille lyden "{navn}": {feil}', file=sys.stderr)


def spill_musikk(navn, volum=60):
    """Spiller musikk fra mappen musikk/ om og om igjen. volum er fra 0 til 100."""
    navn = _rent_navn(navn)
    try:
        if _musikk["navn"] != navn:
            sti = _lydsti(_MUSIKKMAPPE, navn, "musikken")
            stopp_musikk()
            _musikk["navn"] = navn
            _mci(f'open "{sti}" type mpegvideo alias musikk')
            _mci("play musikk repeat")
        volum = max(0, min(100, volum))
        _mci(f"setaudio musikk volume to {round(volum * 10)}")
    except Spillfeil as feil:
        if str(feil).startswith("Fant ikke"):
            raise                       # feil navn: det skal eleven få vite
        # Ingen lydenhet eller lignende: spillet går videre uten musikk
        if "musikk:" + navn not in _lyd_advart:
            _lyd_advart.add("musikk:" + navn)
            print(f'Klarte ikke å spille musikken "{navn}": {feil}', file=sys.stderr)


def stopp_musikk():
    """Stopper musikken."""
    if _musikk["navn"] is not None:
        _musikk["navn"] = None
        try:
            _mci("close musikk")
        except Spillfeil:
            pass


def _forhandslast_lyder():
    if _winmm is None or not os.path.isdir(_LYDMAPPE):
        return
    for fil in sorted(os.listdir(_LYDMAPPE)):
        navn, endelse = os.path.splitext(fil)
        if endelse.lower() in (".wav", ".mp3") and navn not in _lyder:
            try:
                _last_lyd(navn)
            except Spillfeil as feil:
                print(f'Klarte ikke å laste lyden "{navn}": {feil}', file=sys.stderr)


# ----------------------------------------------------------------------
# Tid
# ----------------------------------------------------------------------

_bildenummer = [0]
_tidtakere = []         # (bildenummer, funksjon)
_pause = [False]
_frys = [0]             # hvor mange bilder til spillet er fryst (frys())


def etter(sekunder, funksjon):
    """Kaller funksjonen om et visst antall sekunder. Husk: uten parenteser bak navnet."""
    if not callable(funksjon):
        raise Spillfeil("etter() trenger en funksjon, for eksempel etter(2, ny_runde). "
                        "Husk: uten parenteser bak navnet.")
    _tidtakere.append((_bildenummer[0] + max(1, round(sekunder * _BILDER_PER_SEKUND)), funksjon))


def tid():
    """Antall sekunder siden spillet startet."""
    return _bildenummer[0] / _BILDER_PER_SEKUND


def pause(paa=True):
    """pause(True) fryser spillet, pause(False) setter det i gang igjen.
    Under pause står animasjoner, effekter, etter() og tid() stille,
    men oppdater() kjøres fortsatt (for pausemenyen) og tastene virker."""
    _pause[0] = bool(paa)


def er_pause():
    """True mens spillet står på pause."""
    return _pause[0]


def frys(sekunder=0.05):
    """Fryser hele spillet et lite øyeblikk, for eksempel når et slag treffer
    (det kalles «hitstop» og får slaget til å føles tungt).
    Mens spillet er fryst, kjøres ikke oppdater(), og animasjoner, effekter,
    etter() og tid() står stille. Skjermen vises fortsatt, så glimt synes,
    og tastene du trykker, blir husket til spillet går igjen.

        fiende.glimt(0.1)
        frys(0.06)              # ca. 4 bilder
    """
    if isinstance(sekunder, bool) or not isinstance(sekunder, (int, float)) or sekunder < 0:
        raise Spillfeil(f"frys() trenger et antall sekunder, f.eks. frys(0.05), men fikk {sekunder!r}.")
    _frys[0] = max(_frys[0], max(1, round(sekunder * _BILDER_PER_SEKUND)))


def _kjor_tidtakere():
    klare = [t for t in _tidtakere if t[0] <= _bildenummer[0]]
    for t in klare:
        _tidtakere.remove(t)
    for _, funksjon in klare:
        funksjon()


# ----------------------------------------------------------------------
# Spill-løkka
# ----------------------------------------------------------------------

_rot = None
_lerret = None
_skala = 3
_oppdater = None
_kjorer = False
_neste_bilde = 0.0
_maletider = []


def bilder_per_sekund():
    """Hvor mange bilder i sekundet spillet faktisk klarer akkurat nå."""
    if len(_maletider) < 2:
        return 0
    return round((len(_maletider) - 1) / (_maletider[-1] - _maletider[0]))


def tregeste_bilde():
    """Hvor mange millisekunder det tregeste av de siste 60 bildene tok. Over 17 ms betyr
    at spillet mistet et bilde, og over 25 ms merkes det som et hakk."""
    if len(_maletider) < 2:
        return 0
    return round(max(b - a for a, b in zip(_maletider, _maletider[1:])) * 1000)


def avslutt():
    """Lukker spillet."""
    global _kjorer, _rot
    _kjorer = False
    if _rot is None:
        return
    try:
        _mci("close all")
    except Spillfeil:
        pass
    if _winmm is not None:
        _winmm.timeEndPeriod(1)
    rot, _rot = _rot, None
    rot.destroy()


def _feil_i_spillet():
    global _kjorer
    _kjorer = False
    type_, feil, tb = sys.exc_info()

    # Finn den siste linjen i elevens egen kode, ikke i spillmotoren.
    linje = None
    for ramme in reversed(traceback.extract_tb(tb)):
        if os.path.abspath(ramme.filename) != os.path.abspath(__file__):
            linje = ramme
            break

    print("\n" + "=" * 60, file=sys.stderr)
    print("Spillet stoppet på grunn av en feil:", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    if isinstance(feil, Spillfeil) and linje is not None:
        print(f'  Fil "{linje.filename}", linje {linje.lineno}\n    {linje.line}',
              file=sys.stderr)
        print(f"\n{feil}", file=sys.stderr)
    else:
        traceback.print_exception(type_, feil, tb)

    hvor = f"Linje {linje.lineno}: {linje.line}" if linje else ""
    if isinstance(feil, Spillfeil):
        hva = str(feil)
    else:
        hva = f"{type_.__name__}: {feil}"
    try:
        _tilbakestill_skjermflytt()
        bredde = int(_lerret["width"])
        _lerret.create_rectangle(0, 0, bredde, 200, fill="#7a1020", width=0, tags="feil")
        _lerret.create_text(
            12, 12, anchor="nw", fill="white", width=bredde - 24,
            font=("Consolas", -16, "bold"),
            text=f"Feil i spillet!\n\n{hvor}\n\n{hva}\n\n(Se terminalen for mer.)",
            tags="feil",
        )
        _lerret.tag_raise("feil")
    except tk.TclError:
        pass


def _steg():
    global _neste_bilde
    if not _kjorer:
        return
    try:
        frosset = _frys[0] > 0              # frys(): heller ikke oppdater() kjøres
        if frosset:
            _frys[0] -= 1
        fryst = _pause[0] or frosset
        if not fryst:
            _bildenummer[0] += 1
            _kjor_tidtakere()
        if _oppdater is not None and not frosset:
            _oppdater()
        if not _kjorer:                 # oppdater() kalte avslutt()
            return
        if not fryst:
            for objekt in list(_objekter):
                objekt._tikk()
        _oppdater_skjerm()
        _tilbakestill_skjermflytt()
        if _kart["endret"]:
            _bygg_kart()
            _stabling["endret"] = True
        elif _kart["celler"]:
            _oppdater_celler()
            _stabling["endret"] = True
        if not fryst:
            _animer_kart()
        for objekt in list(_objekter):
            objekt._synk()
        if not fryst:
            _oppdater_partikler()
        _stable_om()
        _flytt_skjerm()
    except Exception:
        _feil_i_spillet()
        return
    if not frosset:                     # tastetrykk under frys() går ikke tapt
        _taster_nye.clear()

    naa = time.perf_counter()
    _maletider.append(naa)
    if len(_maletider) > 60:
        del _maletider[0]
    _sjekk_overleggfart()

    _neste_bilde += 1 / _BILDER_PER_SEKUND
    if _neste_bilde < naa - 0.1:        # spillet henger etter: ikke prøv å ta det igjen
        _neste_bilde = naa
    if _neste_bilde - naa > 0.006:        # god tid til neste bilde: gjør forarbeid
        frist = min(_neste_bilde - 0.004, naa + 0.004)
        _glimt_i_ledig_tid(frist)
        _forhandslast_bilder(frist)
        naa = time.perf_counter()
    ventetid = round((_neste_bilde - naa) * 1000)
    _rot.after(max(1, ventetid), _steg)


def start(bredde=15, hoyde=10, tittel="Spill", skala=None, bakgrunn="black"):
    """
    Åpner vinduet og starter spillet. Kall start() helt nederst i programmet.

    bredde og hoyde måles i ruter (15 × 10 er samme størrelse som en Game Boy Advance).
    skala er hvor mye pikslene forstørres; hvis du ikke velger, blir vinduet
    så stort som skjermen tillater.
    """
    global _rot, _lerret, _skala, _oppdater, _kjorer, _neste_bilde

    import __main__
    _oppdater = getattr(__main__, "oppdater", None)

    if _winmm is not None:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)   # skarpe piksler
        except (AttributeError, OSError):
            pass
        _winmm.timeBeginPeriod(1)                           # jevnere tidtaking

    _rot = tk.Tk()
    _rot.title(tittel)
    _rot.resizable(False, False)

    if skala is None:
        skjerm_b = _rot.winfo_screenwidth()
        skjerm_h = _rot.winfo_screenheight()
        skala = min(skjerm_b * 0.9 // (bredde * RUTE), skjerm_h * 0.8 // (hoyde * RUTE))
    _skala = max(1, int(skala))

    vindu_b = bredde * RUTE * _skala
    vindu_h = hoyde * RUTE * _skala
    _lerret = tk.Canvas(_rot, width=vindu_b, height=vindu_h, bg=bakgrunn,
                        highlightthickness=0)
    _lerret.pack()
    x = (_rot.winfo_screenwidth() - vindu_b) // 2
    y = (_rot.winfo_screenheight() - vindu_h) // 3
    _rot.geometry(f"+{x}+{y}")

    _rot.bind("<KeyPress>", _tast_ned)
    _rot.bind("<KeyRelease>", _tast_opp)
    _rot.bind("<FocusOut>", _mistet_fokus)
    _rot.protocol("WM_DELETE_WINDOW", avslutt)

    _forhandslast_lyder()

    _kjorer = True
    _neste_bilde = time.perf_counter()
    _rot.after(1, _steg)
    _rot.focus_force()
    try:
        _rot.mainloop()
    except KeyboardInterrupt:
        avslutt()


# ----------------------------------------------------------------------
# Bokstavene i pikselskrifta
# ----------------------------------------------------------------------
# Hvert tegn er 9 rader med # (piksel) og . (tomt). De 7 øverste radene er
# vanlig høyde, de 2 nederste er for g, j, p, q og y. Du kan endre en bokstav
# eller legge til nye tegn her.

_SKRIFT_DATA = r"""
A
.###.
#...#
#...#
#####
#...#
#...#
#...#
.....
.....
B
####.
#...#
#...#
####.
#...#
#...#
####.
.....
.....
C
.###.
#...#
#....
#....
#....
#...#
.###.
.....
.....
D
####.
#...#
#...#
#...#
#...#
#...#
####.
.....
.....
E
#####
#....
#....
####.
#....
#....
#####
.....
.....
F
#####
#....
#....
####.
#....
#....
#....
.....
.....
G
.###.
#...#
#....
#.###
#...#
#...#
.####
.....
.....
H
#...#
#...#
#...#
#####
#...#
#...#
#...#
.....
.....
I
###
.#.
.#.
.#.
.#.
.#.
###
...
...
J
..###
...#.
...#.
...#.
#..#.
#..#.
.##..
.....
.....
K
#...#
#..#.
#.#..
##...
#.#..
#..#.
#...#
.....
.....
L
#....
#....
#....
#....
#....
#....
#####
.....
.....
M
#...#
##.##
#.#.#
#.#.#
#...#
#...#
#...#
.....
.....
N
#...#
##..#
#.#.#
#..##
#...#
#...#
#...#
.....
.....
O
.###.
#...#
#...#
#...#
#...#
#...#
.###.
.....
.....
P
####.
#...#
#...#
####.
#....
#....
#....
.....
.....
Q
.###.
#...#
#...#
#...#
#.#.#
#..#.
.##.#
.....
.....
R
####.
#...#
#...#
####.
#.#..
#..#.
#...#
.....
.....
S
.###.
#...#
#....
.###.
....#
#...#
.###.
.....
.....
T
#####
..#..
..#..
..#..
..#..
..#..
..#..
.....
.....
U
#...#
#...#
#...#
#...#
#...#
#...#
.###.
.....
.....
V
#...#
#...#
#...#
#...#
.#.#.
.#.#.
..#..
.....
.....
W
#...#
#...#
#...#
#.#.#
#.#.#
##.##
#...#
.....
.....
X
#...#
#...#
.#.#.
..#..
.#.#.
#...#
#...#
.....
.....
Y
#...#
#...#
.#.#.
..#..
..#..
..#..
..#..
.....
.....
Z
#####
....#
...#.
..#..
.#...
#....
#####
.....
.....
Æ
.####
#.#..
#.#..
####.
#.#..
#.#..
#.###
.....
.....
Ø
.###.
#..##
#.#.#
#.#.#
#.#.#
##..#
.###.
.....
.....
Å
..#..
.#.#.
..#..
.....
.###.
#####
#...#
.....
.....
Ä
.#.#.
.....
.###.
#...#
#####
#...#
#...#
.....
.....
Ö
.#.#.
.....
.###.
#...#
#...#
#...#
.###.
.....
.....
Ü
.#.#.
.....
#...#
#...#
#...#
#...#
.###.
.....
.....
É
...#.
..#..
#####
#....
####.
#....
#####
.....
.....
a
....
....
.##.
...#
.###
#..#
.###
....
....
b
#...
#...
###.
#..#
#..#
#..#
###.
....
....
c
....
....
.##.
#..#
#...
#..#
.##.
....
....
d
...#
...#
.###
#..#
#..#
#..#
.###
....
....
e
....
....
.##.
#..#
####
#...
.###
....
....
f
..#
.#.
###
.#.
.#.
.#.
.#.
...
...
g
....
....
.###
#..#
#..#
.###
...#
#..#
.##.
h
#...
#...
###.
#..#
#..#
#..#
#..#
....
....
i
#
.
#
#
#
#
#
.
.
j
..#
...
..#
..#
..#
..#
..#
#.#
.#.
k
#...
#...
#..#
#.#.
##..
#.#.
#..#
....
....
l
#.
#.
#.
#.
#.
#.
.#
..
..
m
.....
.....
####.
#.#.#
#.#.#
#.#.#
#.#.#
.....
.....
n
....
....
###.
#..#
#..#
#..#
#..#
....
....
o
....
....
.##.
#..#
#..#
#..#
.##.
....
....
p
....
....
###.
#..#
#..#
#..#
###.
#...
#...
q
....
....
.###
#..#
#..#
#..#
.###
...#
...#
r
...
...
#.#
##.
#..
#..
#..
...
...
s
....
....
.###
#...
.##.
...#
###.
....
....
t
.#.
.#.
###
.#.
.#.
.#.
..#
...
...
u
....
....
#..#
#..#
#..#
#..#
.###
....
....
v
.....
.....
#...#
#...#
.#.#.
.#.#.
..#..
.....
.....
w
.....
.....
#...#
#...#
#.#.#
#.#.#
.#.#.
.....
.....
x
....
....
#..#
#..#
.##.
#..#
#..#
....
....
y
....
....
#..#
#..#
#..#
.###
...#
#..#
.##.
z
....
....
####
..#.
.#..
#...
####
....
....
æ
......
......
.####.
...#.#
.#####
#..#..
.##.##
......
......
ø
.....
.....
.###.
#..##
#.#.#
##..#
.###.
.....
.....
å
.##.
....
.##.
...#
.###
#..#
.###
....
....
ä
#..#
....
.##.
...#
.###
#..#
.###
....
....
ö
#..#
....
.##.
#..#
#..#
#..#
.##.
....
....
ü
#..#
....
#..#
#..#
#..#
#..#
.###
....
....
é
..#.
.#..
.##.
#..#
####
#...
.###
....
....
0
.###.
#...#
#...#
#.#.#
#...#
#...#
.###.
.....
.....
1
..#..
.##..
..#..
..#..
..#..
..#..
.###.
.....
.....
2
.###.
#...#
....#
...#.
..#..
.#...
#####
.....
.....
3
.###.
#...#
....#
..##.
....#
#...#
.###.
.....
.....
4
...#.
..##.
.#.#.
#..#.
#####
...#.
...#.
.....
.....
5
#####
#....
####.
....#
....#
#...#
.###.
.....
.....
6
.###.
#....
#....
####.
#...#
#...#
.###.
.....
.....
7
#####
....#
...#.
..#..
.#...
.#...
.#...
.....
.....
8
.###.
#...#
#...#
.###.
#...#
#...#
.###.
.....
.....
9
.###.
#...#
#...#
.####
....#
....#
.###.
.....
.....
.
.
.
.
.
.
.
#
.
.
,
..
..
..
..
..
..
.#
#.
..
:
.
.
#
.
.
.
#
.
.
;
..
..
.#
..
..
..
.#
#.
..
!
#
#
#
#
#
.
#
.
.
?
.###.
#...#
....#
...#.
..#..
.....
..#..
.....
.....
-
....
....
....
####
....
....
....
....
....
_
.....
.....
.....
.....
.....
.....
.....
#####
.....
+
.....
.....
..#..
..#..
#####
..#..
..#..
.....
.....
=
....
....
####
....
####
....
....
....
....
*
.....
#.#.#
.###.
#####
.###.
#.#.#
.....
.....
.....
/
...#
...#
..#.
.#..
#...
#...
#...
....
....
\
#...
#...
.#..
..#.
...#
...#
...#
....
....
%
##..#
##..#
...#.
..#..
.#...
#..##
#..##
.....
.....
'
#
#
.
.
.
.
.
.
.
"
#.#
#.#
...
...
...
...
...
...
...
(
.#
#.
#.
#.
#.
#.
.#
..
..
)
#.
.#
.#
.#
.#
.#
#.
..
..
[
##
#.
#.
#.
#.
#.
##
..
..
]
##
.#
.#
.#
.#
.#
##
..
..
<
...#
..#.
.#..
#...
.#..
..#.
...#
....
....
>
#...
.#..
..#.
...#
..#.
.#..
#...
....
....
#
.#.#.
.#.#.
#####
.#.#.
#####
.#.#.
.#.#.
.....
.....
&
.##..
#..#.
#.#..
.#...
#.#.#
#..#.
.##.#
.....
.....
@
.###.
#...#
#.###
#.#.#
#.###
#....
.###.
.....
.....
~
.....
.....
.....
.##.#
#..#.
.....
.....
.....
.....
♥
.....
.#.#.
#####
#####
.###.
..#..
.....
.....
.....
…
.....
.....
.....
.....
.....
.....
#.#.#
.....
.....
→
.....
..#..
...#.
#####
...#.
..#..
.....
.....
.....
←
.....
..#..
.#...
#####
.#...
..#..
.....
.....
.....
□
####
#..#
#..#
#..#
#..#
#..#
####
....
....
"""

_SKRIFT = _les_skrift(_SKRIFT_DATA)

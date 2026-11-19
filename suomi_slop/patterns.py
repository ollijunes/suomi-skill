"""Säännöt: tekoälytekstin ja käännössuomen tunnusmerkit suomenkielisessä asiatekstissä.

Kolme tasoa:
- VAKAVA: lukija tunnistaa heti (emoji, "tässä artikkelissa käsittelemme").
- VALTETTAVA: täytesanat, tyhjät metaforat, käännöskukkaset.
- EPAILYTTAVA: sallittu harvakseltaan, toistuessaan maneeri.
"""

import re
from dataclasses import dataclass

VAKAVA = "vakava"
VALTETTAVA = "vältettävä"
EPAILYTTAVA = "epäilyttävä"

PENALTY = {VAKAVA: 2.0, VALTETTAVA: 0.5, EPAILYTTAVA: 0.2}


@dataclass(frozen=True)
class Rule:
    name: str
    level: str
    regex: re.Pattern
    example: str
    advice: str


def _rule(name, level, pattern, example, advice, flags=re.IGNORECASE):
    return Rule(name, level, re.compile(pattern, flags), example, advice)


RULES = (
    _rule(
        "geneerinen-johdanto",
        VAKAVA,
        r"\b(Tässä (artikkelissa|oppaassa|kirjoituksessa) "
        r"(käsittelemme|kerromme|tarkastelemme|perehdymme|tutustumme|opit|näytämme|käymme läpi)|"
        r"Olet varmasti (miettinyt|pohtinut|ihmetellyt|kuullut|huomannut)|"
        r"Tervetuloa lukemaan|"
        r"Tämä (artikkeli|opas|kirjoitus) (käsittelee|tarjoaa|antaa|kertoo))",
        "Tässä artikkelissa käsittelemme ruisleivän leipomista.",
        "Aloita asialla: kerro ensimmäisessä virkkeessä se, mitä lukija tuli hakemaan.",
    ),
    _rule(
        "emoji",
        VAKAVA,
        "["
        "\U0001f300-\U0001f9ff"
        "\U0001fa70-\U0001faff"
        "\U00002600-\U000026ff"
        "\U00002700-\U000027bf"
        "⬅-⬇⭐⤴⤵"
        "]",
        "Näin teet sen ✅ helposti 🚀",
        "Poista emojit asiatekstistä.",
        flags=0,
    ),
    _rule(
        "huutomerkki",
        VAKAVA,
        r"[^\W\d_]+!(?=\s|$)",
        "Tämä on tärkeää! Muista myös kuitit.",
        "Vaihda piste. Asiateksti ei huuda.",
        flags=0,
    ),
    _rule(
        "metakommentti",
        VAKAVA,
        r"\b(toivottavasti (tämä|tästä) (auttaa|selvensi|oli apua|on hyötyä)|"
        r"olen tekoäly|tekoälynä en|AI-?assistenttina|kielimallina)\b",
        "Toivottavasti tästä oli apua.",
        "Poista koko virke. Lukija ei tarvitse kirjoittajan kommenttia tekstistä.",
    ),
    _rule(
        "taytesana",
        VALTETTAVA,
        r"\b(kannattaa muistaa|on tärkeää muistaa|on tärkeää huomata|tärkeä huomio|"
        r"näin ollen|yhteenvetona voidaan todeta|yhteenvetona|lopuksi voidaan todeta|"
        r"on syytä huomata|on hyvä muistaa|ei pidä unohtaa|on hyvä tiedostaa|"
        r"kuten aiemmin mainittiin|kuten todettua)\b",
        "Kannattaa muistaa, että taikina lepää yön yli.",
        "Poista täyte ja sano asia: ”Anna taikinan levätä yön yli.”",
    ),
    _rule(
        "tyhja-metafora",
        VALTETTAVA,
        r"\b((sukeltaa|sukellamme|sukelletaan|sukella) (syvälle|syvemmälle|aiheeseen|maailmaan)|"
        r"uppoutu(a|kaa|kaamme)|maailmassa,? jossa|aikakaudella,? jolloin|"
        r"kivijalka|kynnyskysymys|punainen lanka|pelin henki|uusi normaali)\b",
        "Sukelletaan syvälle hapanjuuren maailmaan.",
        "Poista metafora ja kerro, mitä tapahtuu, kenelle ja milloin.",
    ),
    _rule(
        "superlatiivi",
        VALTETTAVA,
        r"\b(erinomai(nen|sen|sta|sia)|loistav(a|aa|an|in|ia)|huipputärkeä\w*|"
        r"äärimmäisen (tärkeä|hyödyllinen)\w*|uskomattoman|käänteentekev\w+|"
        r"mullistav\w+|vallankumoukselli\w+|ainutlaatui\w+)\b",
        "Tämä on erinomainen tapa säästää sähköä.",
        "Poista adjektiivi tai korvaa se luvulla tai esimerkillä.",
    ),
    _rule(
        "kaannoskukkanen",
        VALTETTAVA,
        r"\b(pitkässä juoksussa|päivän päätteeksi|tekee järkeä|tehdä järkeä|"
        r"ottaa seuraava(n)? askel(een)?|viedä seuraavalle tasolle|"
        r"seuraavalle tasolle|olla samalla sivulla)\b",
        "Pitkässä juoksussa tämä tekee järkeä.",
        "Sano suomeksi: ”pitkällä aikavälillä”, ”kannattaa”, ”on järkevää”.",
    ),
    _rule(
        "yhdyssana",
        VALTETTAVA,
        r"\b(alunperin|kokoajan|jokatapauksessa|ennenkaikkea|niinkuin|kiitos paljon etukäteen)\b",
        "Palvelu tehtiin alunperin omaan käyttöön.",
        "Kirjoita erikseen: alun perin, koko ajan, joka tapauksessa, ennen kaikkea, niin kuin.",
    ),
    _rule(
        "siirtymalause",
        VALTETTAVA,
        r"\b(seuraavassa (käsittelemme|tarkastelemme)|seuraavaksi (käsittelemme|tarkastelemme)|"
        r"perehdytään (seuraavaksi|tarkemmin)|keskitymme nyt|katsotaanpa (tarkemmin|lähemmin))\b",
        "Seuraavassa käsittelemme taikinan nostatusta.",
        "Poista. Väliotsikko kertoo jo, mitä seuraavaksi tulee.",
    ),
    _rule(
        "konsulttisana",
        VALTETTAVA,
        r"\b(toiminnallisuuksi\w+|päätöksentekokelpoi\w+|konsolidoin\w+|"
        r"holisti\w+|saumat(on|toman|tonta|tomasti)|agentti(nen|sen|sta|sia|set)|"
        r"synergi\w+|arvolupau\w+)\b",
        "Sovelluksen toiminnallisuuksien kehittäminen.",
        "Kerro, mitä tehdään: ”Lisäämme sovellukseen haun.”",
    ),
    _rule(
        "ei-x-vaan-y",
        EPAILYTTAVA,
        r"\bei\s+(ole\s+)?(vain|pelkästään|ainoastaan|pelkkä)\b[^.!?\n]{1,80}?\bvaan\b",
        "Tämä ei ole vain laskuri, vaan strateginen työkalu.",
        "Sano suoraan, mikä asia on. Enintään kerran tekstissä.",
    ),
    _rule(
        "vastakkainasettelu",
        EPAILYTTAVA,
        r"\b(Se|Tämä|Siitä|Kyse|Kyseessä) ei (ole|synny|tarkoita)\b[^.!?\n]{1,60}\.\s+"
        r"(Se|Tämä|Siitä|Kyse|Kyseessä) (on|syntyy|tarkoittaa)\b",
        "Siitä ei synny säästöä. Siitä syntyy kulu.",
        "Yhdistä yhdeksi väitteeksi: ”Se on kulu, ei säästö.”",
        flags=0,
    ),
    _rule(
        "kolmoisrytmi",
        EPAILYTTAVA,
        r"\b([a-zäöå]{4,}),\s+([a-zäöå]{4,})\s+ja\s+([a-zäöå]{4,})\b",
        "selkeä, johdonmukainen ja tehokas",
        "Jos kolmikko on rytmin vuoksi, valitse sanoista tarkin. Oikea luettelo saa jäädä.",
        flags=0,
    ),
    _rule(
        "passiivitayte",
        EPAILYTTAVA,
        r"\b(voidaan (todeta|sanoa|ajatella|nähdä)|on hyvä (huomioida|tietää)|"
        r"on syytä (huomioida|miettiä|pohtia)|on mahdollista,? että)\b",
        "Voidaan todeta, että hapanjuuri on vaativa.",
        "Sano väite ilman kehystä: ”Hapanjuuri on vaativa.”",
    ),
    _rule(
        "strategiasana",
        EPAILYTTAVA,
        r"\b(strategi(nen|sen|sta|sesti)|kokonaisvaltai\w+|optimoi\w+|tehosta\w+|"
        r"skaalautuv\w+|innovatiivi\w+|ketterä\w*)\b",
        "Kokonaisvaltainen ja skaalautuva ratkaisu.",
        "Konkretisoi: mitä se tekee, kenelle ja paljonko.",
    ),
)

RULES_BY_NAME = {rule.name: rule for rule in RULES}

# Rakenteelliset mittarit lasketaan koko tekstistä.
DASH = re.compile(r"\s[—–]\s")
TARKEA = re.compile(r"\btärkeä\w*\b", re.IGNORECASE)
KRIITTINEN = re.compile(r"\bkriitti(nen|sen|stä|sesti|siä|set)\b", re.IGNORECASE)
HEADING = re.compile(r"^#{2,3}\s+(.+)$|<h[23][^>]*>(.+?)</h[23]>", re.MULTILINE | re.IGNORECASE)
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

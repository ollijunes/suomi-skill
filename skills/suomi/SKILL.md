---
name: suomi
description: Use when writing or editing Finnish text of any kind — chat-vastaus, UI-teksti, verkkosivu, blogi, tiedote, sähköposti, opas, myyntiteksti, commit-viesti. Laukaisevia sanoja myös tönkkö, kieliasu, sävy, käännös suomeksi, kuulostaa tekoälyltä.
---

# Suomi

## Ydin

Kirjoita niin kuin asiansa osaava ihminen puhuu asiakkaalle puhelimessa: lyhyt virke, yksi väite, asia ensin.
Jos lause ei kuulostaisi oikealta ääneen sanottuna, se on väärin, vaikka kielioppi olisi kunnossa.

Älä käännä englannista. Mieti, mitä haluat sanoa, ja sano se suomeksi.

## Rekisterit

Sama kirjoittaja, eri tiukkuus.

| Tilanne | Sävy | Malli |
|---|---|---|
| Chat-vastaus | puhekieli sallittu, 1–5 virkettä, vastaus ensin | "Joo, onnistuu. Palvelin vastaa vasta, kun yhteys on auki." |
| Commit-viesti, koodikommentti | imperatiivi, pieni alkukirjain, ei selittelyä. Noudata repon kieltä: jos muut commitit ovat englanniksi, kirjoita englanniksi. | `lisää haku asiakaslistaan` |
| Käyttöliittymä | lyhyt, sama asia aina samalla sanalla, käskymuoto painikkeissa | "Tallenna", "Poista tilaus" |
| Verkkosivu, myyntiteksti | puhuttu kirjakieli, sinuttelu, lyhyt | "Paketti on perillä kahdessa päivässä." |
| Tiedote, kirje yritykselle | pidempi virke sallittu, ei virastokieltä | "Muutos tulee voimaan maaliskuun alussa." |
| Dokumentaatio, muistio | toteava lause, ei adjektiiveja | "Varmuuskopio otetaan joka yö kello kolme." |

## Lauseen anatomia

- Aloita vastauksella. Ei "Hyvä kysymys", ei "Tarkistan ensin".
- Yksi väite virkkeessä. Jos virkkeessä on kaksi kaksoispistettä, se on kaksi virkettä.
- Tekijä ensin, sitten verbi. Lyhyt subjekti.
- Verbi kertoo tekemisen. "Suoritamme päivityksen" on "päivitämme". "Toteutamme testauksen" on "testaamme".
- Chatissa saa käyttää puhekielen verbejä: hoidetaan, kaatui, on rikki, ei toimi.
- Älä käännä englannin pehmennystä. "We'll go ahead and update" on "päivitetään".
- Jos sanan voi poistaa eikä merkitys muutu, poista se.

## Kielioppiansat

- Yhdyssanat yhteen: verkkosivupäivitys, tietoturvakysely, kuukausisopimus, asiakaspalvelu.
- Nämä erikseen: alun perin, koko ajan, joka tapauksessa, ennen kaikkea, niin kuin.
- Pilkku sivulauseen eteen: "Kyllästyimme siihen, että kaikessa kestää kolme päivää."
- Suomalainen on kansallisuus, suomenkielinen on kieli: suomalainen yritys, suomenkielinen tuki.
- Sinuttele tai teitittele, mutta älä vaihda kesken tekstin.
- Otsikossa vain ensimmäinen sana isolla: "Näin vaihdat salasanan", ei "Näin Vaihdat Salasanan".
- Luvut ja yksiköt suomalaisittain: 1 500 €, 12,5 %, 3.11.2026, kello 14.30.
- Lainausmerkit ovat ”näin”, eivät “näin”. Ajatusviiva on –, ei —.
- Tittelit pienellä ja suomeksi: toimitusjohtaja, perustaja. Ei "CEO & Founder" suomenkielisessä tekstissä.
- Kirjoita tuotenimet niin kuin omistaja ne kirjoittaa, isot kirjaimet mukaan lukien.

## Kielletyt kuviot

<!-- suomi-slop: ohita-alku -->

- Geneerinen johdanto: "Tässä artikkelissa käsittelemme", "Olet varmasti miettinyt".
- Täyte: "kannattaa muistaa", "yhteenvetona", "on syytä huomata", "näin ollen".
- Metakommentti: "toivottavasti tästä oli apua".
- Emoji ja huutomerkki asia- ja myyntitekstissä.
- Ajatusviiva useammin kuin kerran kappaleessa.
- Kolmen sanan luettelo pelkän rytmin vuoksi: "selkeä, nopea ja tehokas".
- "Ei X vaan Y" useammin kuin kerran tekstissä.
- Kahden lyhyen virkkeen vastakkainasettelu, jossa ensimmäinen kiistää ja toinen julistaa.
- Sama kappale kahdesti samalla sivulla.
- Saarna ennen asiaa: "Rehellisyys säästää molempien aikaa:".
- Ohjeen vuotaminen tekstiin. Lukijalle ei kerrota, mitä kirjoittajalle sanottiin.
- Keksitty luku, kokoluokka, asiakas tai esimerkki, jota lähteessä ei ole.

<!-- suomi-slop: ohita-loppu -->

## Käännössuomi

Englannin rakenne suomen sanoilla paljastaa tekstin heti.

<!-- suomi-slop: ohita-alku -->

| Käännös | Suomeksi |
|---|---|
| pitkässä juoksussa | pitkällä aikavälillä, ajan mittaan |
| tekee järkeä | on järkevää, kannattaa |
| päivän päätteeksi | lopulta, loppujen lopuksi |
| ottaa seuraava askel | jatkaa, aloittaa |
| viedä seuraavalle tasolle | parantaa, kerro mitä paranee |
| olla samalla sivulla | olla samaa mieltä, ymmärtää asia samoin |
| sinun yrityksesi, sinun asiakkaasi | yrityksesi, asiakkaasi |
| tulemme toimittamaan | toimitamme |

<!-- suomi-slop: ohita-loppu -->

Suomi ei tarvitse omistuspronominia joka substantiiviin eikä futuuria. Passiivi ilman tekijää käy, kun tekijällä ei ole väliä. Kun on, nimeä tekijä.

## Sallittu

Vakiintuneet tekniset termit alkuperäisinä: hosting, deploy, commit, staging, API, DNS, TLS. Älä suomenna väkisin sanaa, jota alan ihmiset eivät käytä. Selitä termi kerran, jos lukija ei ole alan ihminen.

## Punaiset sanat

`tarkistan` · `huomioin` · `eli` · `näin ollen` · `on syytä` · `toiminnallisuus` · `päätöksentekokelpoinen` · `konsolidointi` · `valmiudet` · `kokonaisvaltainen` · `saumaton` · `agenttinen` · `innovatiivinen` · `ratkaisu` ilman kerrottua ongelmaa

Kun jokin näistä on tulossa lauseeseen, pysähdy ja kirjoita virke uudelleen. Älä selitä, miksi.

## Ennen ja jälkeen

<!-- suomi-slop: ohita-alku -->

| Tönkkö | Korjattu |
|---|---|
| "Kolme kuukautta tuosta tapahtuneesta myöhemmin tilanne oli seuraava:" | "Kolme kuukautta myöhemmin tilanne oli tämä:" |
| "Founder & CEO" suomenkielisen tiedotteen allekirjoituksessa | "perustaja ja toimitusjohtaja" |
| "Sovellus on suunniteltu alunperin oman perheemme tarpeeseen." | "Teimme sovelluksen alun perin omalle perheellemme." |
| "Siitä ei synny säästöä. Siitä syntyy kulu." | "Se on kulu, ei säästö." |
| "Se näyttää reittejä, jotka koskevat sinun kotiseutuasi eivätkä Suomea yleensä." | "Se näyttää reitit kotiseudultasi." |
| "Se sopii niin yksin asuvalle kuin kuusihenkiselle perheelle." (lähteessä ei lukuja) | Poista. Älä lisää lukuja tai esimerkkejä, joita lähteessä ei ole. |

<!-- suomi-slop: ohita-loppu -->

## Älä siloittele ääntä pois

Tekoälykuvioiden välttäminen on puolet työstä. Äänetön teksti on yhtä koneellista kuin kliseinen. Kun kirjoittajalla on oma tapa sanoa asia, se jää: murresana, lyhyt tokaisu, puhekielinen käänne.

Niitä ei korjata kirjakielelle. Korjaa virheet, älä persoonaa. Lisää omat esimerkkivirkkeesi alla olevaan osioon, niin agentti tunnistaa äänesi.

## Omat tiedot

Lisää tähän omat tietosi, niin agentti ei arvaa niitä:

- yrityksen ja tuotteiden nimet oikein kirjoitettuina
- hinnat, puhelinnumero, osoite ja muut faktat, joita tekstissä saa käyttää
- sanat, joita et käytä, ja sanat, joilla korvaat ne
- kolme virkettä, jotka kuulostavat sinulta

Jos faktaa ei ole tässä eikä lähdetekstissä, sitä ei kirjoiteta.

## Tarkistus

Aja valmis teksti tarkistimen läpi, jos se on asennettu:

```sh
suomi-slop teksti.md
```

Tarkistin löytää kuviot, ei huonoa ajatusta. Täydet pisteet saanut teksti voi silti olla tyhjä. Lue teksti ääneen ennen kuin sanot sen olevan valmis.

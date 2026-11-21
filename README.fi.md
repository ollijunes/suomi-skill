# suomi-skill

Kirjoitusohje, jolla tekoälyagentti kirjoittaa luontevaa suomea, ja
`suomi-slop`, tarkistin, joka löytää tekstistä tekoälyn ja käännössuomen
kuviot.

[Read in English](README.md)

Kielimalli kirjoittaa suomea, jossa kielioppi on kunnossa ja kaikki muu
pielessä. Lauseet ovat englantia suomen sanoilla: omistuspronomini joka
substantiivissa, sanasta sanaan käännetty sanonta, kolme adjektiivia
peräkkäin ja huutomerkki pisteen paikalla. Suomalainen lukija huomaa sen
yhdestä virkkeestä eikä sen jälkeen luota sivuun.

Repossa on kaksi osaa. Ne toimivat yksin ja yhdessä.

- **[`skills/suomi/SKILL.md`](skills/suomi/SKILL.md)** kertoo agentille,
  miten suomea kirjoitetaan: rekisterit chatista tiedotteeseen, lauseen
  rakenne, kielioppiansat, kielletyt kuviot, käännössuomen vastineet ja
  korjausesimerkit.
- **`suomi-slop`** lukee Markdown-, MDX-, Astro-, HTML- ja tekstitiedostot,
  listaa osumat rivinumeroineen ja antaa tiedostolle pisteet nollasta
  kymmeneen. Sen voi ajaa terminaalissa, commit-hookissa tai CI:ssä.

Tausta ja syntytarina: [suomeksi](https://ollijunes.com/fi/suomi-skill-luontevaa-suomea-koodausagentilta/) · [in English](https://ollijunes.com/suomi-skill-making-coding-agents-write-natural-finnish/).

## Kenelle

Sinulle, jos annat agentin kirjoittaa tai muokata suomenkielistä tekstiä:
verkkosivuja, blogia, käyttöliittymää, ohjeita tai sähköposteja. Myös
sinulle, jos tarkistat tekstiä, jonka jonkun muun agentti on kirjoittanut.

## Kirjoitusohjeen käyttö

Claude Codessa kopioi kansio omiin skilleihisi:

```sh
git clone https://github.com/ollijunes/suomi-skill
cp -R suomi-skill/skills/suomi ~/.claude/skills/suomi
```

Claude Code ottaa ohjeen käyttöön, kun pyydät suomenkielistä tekstiä.
Muissa agenteissa viittaa ohjeeseen agentin omasta ohjetiedostosta,
esimerkiksi `AGENTS.md`:stä:

```markdown
Kun kirjoitat tai muokkaat suomea, lue ensin skills/suomi/SKILL.md ja noudata sitä.
```

Täytä ohjeen lopusta kohta "Omat tiedot": nimet, faktat ja sanat, joita et
käytä. Jos agentille ei kerrota faktaa, se keksii sen.

## Tarkistimen käyttö

Tarvitset Python 3.11:n tai uudemman. Muita riippuvuuksia ei ole.

```sh
uv tool install git+https://github.com/ollijunes/suomi-skill
suomi-slop content/
```

```text
examples/slop.md: 0,0/10, kirjoita uudelleen (104 sanaa)
  rivi 5: emoji (vakava): 🚲
    Poista emojit asiatekstistä.
  rivi 7: geneerinen-johdanto (vakava): Tässä artikkelissa käsittelemme
    Aloita asialla: kerro ensimmäisessä virkkeessä se, mitä lukija tuli hakemaan.
  ...
examples/hyva.md: 10,0/10, julkaisukelpoinen (98 sanaa)
2 tiedostoa, keskiarvo 5,0/10
```

Kansion [`examples/`](examples) kaksi tiedostoa kertovat saman asian
polkupyörän ketjun öljyämisestä.

| Komento | Mitä tekee |
|---|---|
| `suomi-slop TIEDOSTO_TAI_KANSIO...` | Raportti, huonoin tiedosto ensin |
| `suomi-slop -` | Lukee tekstin vakiosyötteestä |
| `--min-score 8` | Lopettaa virhekoodilla 1, jos jokin tiedosto jää alle 8 pisteen |
| `--below 6` | Näyttää vain alle 6 pisteen tiedostot |
| `--all` | Näyttää kaikki osumat, ei vain kahtatoista ensimmäistä |
| `--json` | Koneluettava raportti |
| `--rules` | Listaa säännöt esimerkkeineen |

## Mitä tarkistin etsii

Sääntöjä on kuusitoista kolmella tasolla.

| Taso | Vähennys | Esimerkkejä |
|---|---|---|
| vakava | 2,0 | geneerinen johdanto, emoji, huutomerkki leipätekstissä, metakommentti |
| vältettävä | 0,5 | täytesanat, tyhjät metaforat, paisutellut adjektiivit, käännöskukkaset, yhdyssanavirheet, konsulttisanat |
| epäilyttävä | 0,2 | toistuva kiisto ja julistus, kolmen sanan rytmilista, passiivitäyte |

<!-- suomi-slop: ohita-alku -->

Koko tekstistä lasketaan lisäksi ajatusviivojen tiheys, sanojen "tärkeä"
ja "kriittinen" määrä ja se, alkavatko väliotsikot samalla sanalla.

<!-- suomi-slop: ohita-loppu -->

Tarkistin ohittaa front matterin, koodin, HTML-kommentit, linkkien
osoitteet ja lainaukset. Jos haluat näyttää huonon esimerkin tahallasi,
lisää rivin loppuun `<!-- suomi-slop: ohita -->` tai rajaa osio
merkeillä `ohita-alku` ja `ohita-loppu`.

## Rajoitukset

- Tarkistin ei tunnista tekoälyä. Ihmiset kirjoittivat näitä kuvioita
  kauan ennen kielimalleja. Huonot pisteet kertovat, että teksti kuulostaa
  täytteeltä. Ne eivät kerro, kuka sen kirjoitti.
- Se vertaa tekstiä kuvioihin eikä jäsennä suomea. Osa taivutusmuodoista
  jää huomaamatta, ja osa rehellisistä lauseista saa osuman.
- Kymmenen pistettä tarkoittaa, että kuvioita ei löytynyt. Teksti voi
  silti olla tyhjä, väärä tai tylsä.
- Faktoja, oikeinkirjoitusta ja kielioppia se ei tarkista muutamaa
  yleistä yhdyssanavirhettä lukuun ottamatta.
- Säännöt sopivat asia- ja myyntitekstiin. Kaunokirjallisuus ja
  chat-lokit saavat outoja pisteitä.
- Kirjoitusohje on yhden kirjoittajan näkemys selkeästä suomesta. Muokkaa
  sitä omaksesi.

## Lisenssi

[MIT](LICENSE). Tekijä [Olli Junes](https://ollijunes.com). Powered by [ResaHost](https://resahost.net/).

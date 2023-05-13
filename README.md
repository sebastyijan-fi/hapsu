# Hapsu Discord-botti

Hapsu on avustaja Discord-botti, joka hyödyntää OpenAI:n tekstigenerointipalvelua vastatakseen käyttäjän viesteihin. Botti tarjoaa avustavaa tekoälyä erilaisiin keskusteluihin ja kysymyksiin.

## Miksi käyttää Hapsu-bottia?

- Automaattiset vastaukset: Hapsu-botti pystyy antamaan automaattisia vastauksia käyttäjien viesteihin. Voit määrittää asetukset eri kanaville ja antaa botille omat vastausviestit.
- Kustomoitava avustaja: Voit säätää Hapsu-botin avustajaviestien sisältöä ja luoda oman persoonallisen avustajan käyttäjien keskusteluihin.
- Helppo integraatio: Hapsu-botti on helppo integroida Discord-palveluun ja se toimii reaaliajassa vastaten käyttäjien viesteihin.

## Esimerkkejä käytöstä

1. Keskusteluavustaja: Käyttäjä voi aloittaa keskustelun kirjoittamalla viestin, ja Hapsu-botti vastaa automaattisesti.
   Käyttö: `.kysy Mikä on elämän tarkoitus?`

2. Asetusten muokkaus: Käyttäjä voi muokata botin asetuksia, kuten avustajaviestin sisältöä.
   Käyttö: `.ohje Vastaa aina aloittaen sanoilla Cha-Cha-Cha`

3. Kustomoitu avustaja: Käyttäjä voi muokata botin avustajaviestin sisältöä kanavakohtaisesti.
   Käyttö: `.hahmo Olet mukava, kohtelias avustaja!`

## Huomioita

- Hapsu-botti käyttää OpenAI:n tekstigenerointipalvelua, joten varmista, että sinulla on tarvittava API-avain.
- Hapsu-botti voi vaatia mukauttamista ja laajentamista riippuen käyttötapauksista ja vaatimuksista.
- Muista noudattaa Discordin käyttöehtoja ja ohjeita käyttäessäsi bottia.

## Hapsu-bottin asennus ja käyttöönotto

Hapsu-bottin asentaminen ja käyttöönotto on helppoa seuraavien ohjeiden avulla:

1. **Suorita asennusskripti**: Suorita `run_bot.sh`-skripti. Tämä skripti hoitaa kaiken tarvittavan asennuksen, kuten riippuvuuksien asennuksen ja palvelimen konfiguroinnin.

2. **Anna API-avaimet**: Skripti pyytää sinua syöttämään OpenAI:n ja Discordin API-avaimet. Avaimet tallennetaan `.env`-tiedostoon.

3. **Käynnistä botti**: Skripti käynnistää botin automaattisesti. Voit tarkistaa botin tilan PM2:n avulla komennolla `pm2 status`.

Huomaa: Skripti päivittää palvelimen ja tekee git-pullin päivittäin keskiyöllä.



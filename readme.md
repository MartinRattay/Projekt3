#### Popis

Tento projekt slouží ke stažení a uložení výsledků voleb do Poslanecké sněmovny ČR z roku 2017 pro jeden zvolený územní celek.\
Na základě odkazu na konkrétní okresní stránku na webu [volby.cz](https://www.volby.cz/) stáhne data pro všechny obce v daném okrese a uloží je do CSV souboru, který je kompatibilní s Microsoft Excelem.

---

#### Ukázka spuštění

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102" "vysledky_kolin.csv"
```

---

#### Vstupní argumenty

1. **URL adresa** – odkaz na stránku s výběrem obcí daného okresu\
   (např. Kolín: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102`)
2. **Výstupní soubor** – název výstupního `.csv` souboru (např. `vysledky_kolin.csv`)

Pokud nejsou zadány oba argumenty správně, program se ukončí s upozorněním.

---

#### Výstupní CSV obsahuje:

- kód obce
- název obce
- počet voličů v seznamu
- počet vydaných obálek
- počet platných hlasů
- počet hlasů pro každou politickou stranu (každá strana = samostatný sloupec)

---

#### Instalace knihoven

Nainstaluj požadované knihovny pomocí `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

#### Požadované knihovny (`requirements.txt`)

```
requests==2.31.0
beautifulsoup4==4.12.2
```

---

#### Struktura projektu

```
projekt/
│
├── main.py               # hlavní skript
├── requirements.txt      # potřebné knihovny
├── README.md             # dokumentace
└── vysledky_kolin.csv    # výstupní soubor (příklad)
```


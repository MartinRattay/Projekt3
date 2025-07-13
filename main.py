"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Martin Rattay
email: rattyy@seznam.cz
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup

def ziskej_html(url):
    try:
        r = requests.get(url)
        r.encoding = "utf-8"
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"Chyba při načítání stránky: {e}")
        sys.exit(1)

def najdi_odkazy_na_obce(soup):
    odkazy = []
    for tr in soup.find_all("tr"):
        td = tr.find("td", class_="cislo")
        if td and td.find("a"):
            href = td.find("a")["href"]
            plna_url = "https://www.volby.cz/pls/ps2017nss/" + href
            odkazy.append(plna_url)
    return odkazy

def ziskej_data_z_obce(obec_url):
    soup = ziskej_html(obec_url)

    # Správné získání názvu obce z <h3> obsahujícího "Obec:"
    nazev = "Neznámá obec"
    h3_tags = soup.find_all("h3")
    for h3 in h3_tags:
        if "Obec:" in h3.text:
            nazev = h3.text.split("Obec:")[1].strip()
            break

    # Tabulky
    tabulky = soup.find_all("table")
    if len(tabulky) < 2:
        return None

    # 1. tabulka: Počet voličů
    volici_radek = tabulky[0].find_all("tr")[-1]
    volici_data = [td.text.strip().replace("\xa0", "") for td in volici_radek.find_all("td")]
    volici_v_seznamu = volici_data[3]
    vydane_obalky = volici_data[4]
    platne_hlasy = volici_data[7]

    # 2. tabulka: Hlasy pro strany
    strany = {}
    for tab in tabulky[1:]:
        for tr in tab.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 5:
                jmeno_strany = tds[1].text.strip()
                hlasy = tds[2].text.strip().replace("\xa0", "")
                strany[jmeno_strany] = hlasy

    return {
        "kodo": obec_url.split("xobec=")[1].split("&")[0],
        "nazev": nazev,
        "volici": volici_v_seznamu,
        "obalky": vydane_obalky,
        "platne": platne_hlasy,
        "strany": strany
    }

def uloz_do_csv(data, jmeno_souboru):
    if not data:
        print("Chyba: Žádná data ke zpracování.")
        return

    # Všechny názvy stran
    vsechny_strany = sorted(set.union(*(set(d["strany"].keys()) for d in data)))

    with open(jmeno_souboru, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")  # Středník pro Excel + BOM
        hlavicka = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + vsechny_strany
        writer.writerow(hlavicka)

        for obec in data:
            radek = [
                obec["kodo"],
                obec["nazev"],
                obec["volici"],
                obec["obalky"],
                obec["platne"]
            ] + [obec["strany"].get(s, "0") for s in vsechny_strany]
            writer.writerow(radek)

def main():
    if len(sys.argv) != 3:
        print("\nChyba: Tento program vyžaduje 2 argumenty: <URL> <vystup.csv>")
        print("Příklad: python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102' 'vysledky_kolin.csv'\n")
        sys.exit(1)

    url = sys.argv[1]
    vystup = sys.argv[2]

    print(f"Načítám seznam obcí z: {url}")
    soup_okres = ziskej_html(url)
    obecni_odkazy = najdi_odkazy_na_obce(soup_okres)

    print(f"Nalezeno {len(obecni_odkazy)} obcí. Stahuji data z vybraného územního celku...")
    vysledky = []
    for odkaz in obecni_odkazy:
        data = ziskej_data_z_obce(odkaz)
        if data:
            vysledky.append(data)

    uloz_do_csv(vysledky, vystup)
    print(f"Hotovo! Výsledky uloženy do {vystup}")
    print("Ukončuji Election scraper.")

if __name__ == "__main__":
    main()









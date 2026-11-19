import requests
from bs4 import BeautifulSoup
import traceback

from nordrest_scraper import HEADERS

ENDPOINT = "https://www.gtc.com/provschema/kalender.asp?klass=T1cs"
MONTHS = ["Januari", "Februari", "Mars", "April", "Maj", "Juni",
          "Juli", "Augusti", "September", "Oktober", "November", "December"]

def rm_reg(l: list[str]):
    res = []
    flg = False
    for item in l:
        if item == "Registreringstidpunkt:":
            flg = True
            continue
        if flg:
            flg = False
            continue
        res.append(item)

    return res

def get_prov():
    resp = requests.get(ENDPOINT, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    table_f = soup.body.find("table", attrs={"class": "normal"})
    rows = table_f.find_all("tr")
    output = ""
    for row in rows:
        children = list(row.children)
        if len(children) == 1: # är ett spacing-element
            continue

        # week = row.find("a").text
        days = list(row.find_all("td", attrs={"valign": "top"}))[1:]
        for day in days:
            if not (day.find_all("span", attrs={"class": "normalröd"})
                    or day.find_all("span", attrs={"class": "normalblå"})
                    or day.find_all("b")):
                continue

            text_lines = day.get_text("\n").splitlines()

            if text_lines[0].strip() in MONTHS:
                text_lines = text_lines[1:]

            day, content_l = text_lines[0], text_lines[1:]
            content_l = rm_reg(content_l)
            content = "\n".join(x.strip() for x in content_l)
            output = output + day + "\n" + content + "\n"

    return output



if __name__ == '__main__':
    print(get_prov())




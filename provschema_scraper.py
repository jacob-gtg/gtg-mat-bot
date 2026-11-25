import requests
from bs4 import BeautifulSoup
from datetime import datetime
import discord
from helpers import CachedEndpoint

ENDPOINT = CachedEndpoint("https://www.gtc.com/provschema/kalender.asp?klass=T1cs")
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
    now = datetime.now()

    resp = ENDPOINT.request()
    soup = BeautifulSoup(resp.text, 'html.parser')

    table_f = soup.body.find("table", attrs={"class": "normal"})
    rows = table_f.find_all("tr")

    embed = discord.Embed(
        title="Kommande prov",
        url="https://www.gtc.com/provschema/kalender.asp?klass=T1cs",
        color=discord.Color.blue(),
    )

    cnt = 0
    for row in rows:
        children = list(row.children)
        if len(children) == 1: # är ett spacing-element
            continue

        week = int(row.find("a").text.strip().lstrip("v."))

        if week != now.isocalendar().week:
            if cnt <= 0:
                continue

        days = list(row.find_all("td", attrs={"valign": "top"}))[1:]
        day_idx = 0
        for day in days:
            day_idx += 1
            if (week == now.isocalendar().week) and (day_idx == now.isocalendar().weekday):
                cnt = 3

            if cnt <= 0: continue

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
            embed.add_field(
                name=day,
                value=content,
                inline=False
            )

            cnt -= 1


    return embed


if __name__ == '__main__':
    print(get_prov())




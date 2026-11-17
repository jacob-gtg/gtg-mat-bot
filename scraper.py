import requests
from bs4 import BeautifulSoup

ENDPOINT = "https://www.nordrest.se/restaurang/restaurang-traffpunkten/"
USER_AGENT = "gtg-mat-bot-(jacob.borstell@gtg.se)"
HEADERS = {"User-Agent": USER_AGENT}

def get_food() -> str:
    resp = requests.get(ENDPOINT, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    info = soup.body.find('section', attrs={"class": "castit-day current"})
    day = info.find("h3", attrs={"class": "castit-day__title"}).span.text.strip()
    dishes = info.find_all("div", attrs={"class": "castit-dish-wrap"})

    text = f"# Mat på träffpunkten idag ({day}):\n\n"

    for dish in dishes:
        type_ = (dish.find("div", attrs={"class": "castit-dish-header castit-dish-header--day"})
                 .span.text.strip())
        name = dish.find("div", attrs={"class": "castit-dish__title"}).span.text.strip()
        desc = dish.find("div", attrs={"class": "castit-dish__desc"}).span.text.strip()
        text = text + "## " + type_ + "\n" + "**" + name + "**\n" + desc + "\n\n"

    return text

import requests
from bs4 import BeautifulSoup
import traceback

ENDPOINTS = {
    "träffpunkten": "https://www.nordrest.se/restaurang/restaurang-traffpunkten/",
    "höjden": "https://www.nordrest.se/restaurang/restaurang-hojden/",
    "backyard": "https://www.nordrest.se/restaurang/backyard/",
    "balansen": "https://www.nordrest.se/restaurang/restaurang-balansen/",
}
USER_AGENT = "gtg-mat-bot-(jacob.borstell@gtg.se)"
HEADERS = {"User-Agent": USER_AGENT}

def get_food(resturang: str | None=None) -> str:
    rest = resturang.lower() if (resturang is not None) else "träffpunkten"
    if not (rest in ENDPOINTS):
        return "Välj en giltig resturang (`träffpunkten`, `höjden`, `backyard`, `balansen`)"
    resp = requests.get(ENDPOINTS[rest], headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        info = soup.body.find('section', attrs={"class": "castit-day current"})
        day = info.find("h3", attrs={"class": "castit-day__title"}).span.text.strip()
        dishes = info.find_all("div", attrs={"class": "castit-dish-wrap"})

        text = f"# Mat på {rest} idag ({day}):\n\n"

        for dish in dishes:
            type_ = (dish.find("div", attrs={"class": "castit-dish-header castit-dish-header--day"})
                     .span.text.strip())
            name = dish.find("div", attrs={"class": "castit-dish__title"}).span.text.strip()
            try:
                desc = dish.find("div", attrs={"class": "castit-dish__desc"}).span.text.strip()
            except AttributeError as e:
                desc = ""
            text = text + "## " + type_ + "\n" + "**" + name + "**\n" + desc + "\n\n"

        return text
    except AttributeError as e:
        print(traceback.format_exc())
        return "Ett fel inträffade när nordrests hemsida skulle tolkas"


if __name__ == "__main__":
    print(get_food("balansen"))

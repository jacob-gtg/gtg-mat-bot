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

def get_food(resturang: str | None=None, meny: bool=False) -> str:
    rest = resturang.lower() if (resturang is not None) else "träffpunkten"
    if not (rest in ENDPOINTS):
        return "Välj en giltig resturang (`träffpunkten`, `höjden`, `backyard`, `balansen`)"
    resp = requests.get(ENDPOINTS[rest], headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        days_elements = (
            soup.body.find('div',
                           attrs={"class": "castit-menu-grid__days castit-menu-grid__days--with-week"}))
        dagar = []
        if meny:
            text = f"# Meny på {rest} denna vecka:\n"
            fake_dagar = list(days_elements.children)
            for fake_dag in fake_dagar:
                if fake_dag.name == "section":
                    dagar.append(fake_dag)
        else:
            text = f"# Mat på {rest} idag:\n"
            dagar.append(days_elements.find('section', attrs={"class": "castit-day current"}))

        for dag in dagar:
            day = dag.find("h3", attrs={"class": "castit-day__title"}).span.text.strip()
            dishes = dag.find_all("div", attrs={"class": "castit-dish-wrap"})

            text = text + "\n## " + day + "\n"

            for dish in dishes:
                type_ = (dish.find("div", attrs={"class": "castit-dish-header castit-dish-header--day"})
                         .span.text.strip())
                name = dish.find("div", attrs={"class": "castit-dish__title"}).span.text.strip()
                try:
                    desc = dish.find("div", attrs={"class": "castit-dish__desc"}).span.text.strip() + "\n"
                except AttributeError as e:
                    desc = ""
                text = text + "## " + type_ + "\n" + "**" + name + "**\n" + desc

        return text
    except AttributeError as e:
        print(traceback.format_exc())
        return "Ett fel inträffade när nordrests hemsida skulle tolkas"


if __name__ == "__main__":
    print(get_food("träffpunkten", True))

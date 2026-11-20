from bs4 import BeautifulSoup
import traceback
import discord
from helpers import error, CachedEndpoint

ENDPOINTS = {
    "träffpunkten": CachedEndpoint("https://www.nordrest.se/restaurang/restaurang-traffpunkten/"),
    "höjden": CachedEndpoint("https://www.nordrest.se/restaurang/restaurang-hojden/"),
}

def get_food(resturang: str | None=None, dag_idx: int | None=None) -> discord.Embed:
    print(dag_idx)

    rest = resturang.lower() if (resturang is not None) else "träffpunkten"
    if not (rest in ENDPOINTS):
        return error("Välj en giltig resturang (`träffpunkten`, `höjden`)")

    endpoint = ENDPOINTS[rest]
    resp = endpoint.request()
    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        days_elements = (soup.body.find('div',
                           attrs={"class": "castit-menu-grid__days castit-menu-grid__days--with-week"}))

        dag = None
        if not (dag_idx is None):
            fake_dagar = list(days_elements.children)
            cc = 0
            for fake_dag in fake_dagar:
                if fake_dag.name == "section":
                    if cc == dag_idx:
                        dag = fake_dag
                        break
                    else:
                        cc += 1
        else:
            dag = days_elements.find('section', attrs={"class": "castit-day current"})

        if dag is None:
            return error("Dagen kunde inte hittas")

        dag_namn = dag.find("h3", attrs={"class": "castit-day__title"}).span.text.strip()
        dishes = dag.find_all("div", attrs={"class": "castit-dish-wrap"})

        embed = discord.Embed(
            title=dag_namn + " (" + rest + ")",
            url=endpoint.url,
            color=discord.Color.blue(),
        )

        for dish in dishes:
            type_ = (dish.find("div", attrs={"class": "castit-dish-header castit-dish-header--day"})
                     .span.text.strip())
            name = dish.find("div", attrs={"class": "castit-dish__title"}).span.text.strip()
            try:
                desc = dish.find("div", attrs={"class": "castit-dish__desc"}).span.text.strip() + "\n"
            except AttributeError as e:
                desc = ""
            embed.add_field(name=type_ + ": " + name, value=desc, inline=False)

        return embed

    except AttributeError as e:
        print(traceback.format_exc())
        return error("Ett fel inträffade när hemsidan skulle tolkas")


if __name__ == "__main__":
    print(get_food("träffpunkten", True))

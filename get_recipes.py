from cookidoo_scrapper import CookidooScrapper
from recipes import Recipe

data_file = 'recipes.txt'
meals_list_url = 'https://cookidoo.es/organize/es-ES/my-recipes'
dinners_list_url = 'https://cookidoo.es/organize/es-ES/custom-list/01F4PXQKYQ0W4X0WT6Q8PB0J7M'


def save_cookidoo_recipes():
    lines = []
    cs = CookidooScrapper()
    cs.login()

    try:
        for r in [*cs.get_all_recipes(meals_list_url, 'meals'), *cs.get_all_recipes(dinners_list_url, 'dinners')]:
            lines.append(','.join([r.name, r.url, r.list, *r.ingredients]))
            lines.append('\n')

        f = open(data_file, 'w')
        f.writelines(lines)
        f.close()
    finally:
        cs.driver.close()


def load_recipes():
    f = open(data_file, 'r')
    recipes = []
    for line in f.readlines():
        data = line.split(',')
        recipes.append(Recipe(name=data[0], url=data[1], list=data[2], ingredients=data[3:]))

    f.close()
    return recipes


if __name__ == '__main__':
    save_cookidoo_recipes()

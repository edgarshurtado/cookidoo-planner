import random

from cookidoo_scrapper import CookidooScrapper
from get_recipes import load_recipes


if __name__ == '__main__':
    key_ingredients = input('Ingredients to prioritize: ')
    key_ingredients = list(map(lambda x: x.strip(), key_ingredients.split(','))) if key_ingredients != '' else []
    print(key_ingredients)

    recipes = load_recipes()

    my_meals = [recipe for recipe in recipes if recipe.list == 'meals']
    my_dinners = [recipe for recipe in recipes if recipe.list == 'dinners']

    selected_recipes = []

    week_days = ['martes', 'jueves', 'sábado', 'lunes']

    while len(selected_recipes) < len(week_days):
        meal_candidate_idx, dinner_candidate_idx = (random.randrange(len(my_meals)), random.randrange(len(my_dinners)))

        meal_candidate = my_meals[meal_candidate_idx]
        dinner_candidate = my_dinners[dinner_candidate_idx]

        if len(key_ingredients) > 0:
            meal_key_ingredients = meal_candidate.ingredients_satisfied(key_ingredients)
            dinner_key_ingredients = dinner_candidate.ingredients_satisfied(key_ingredients)

            key_ingredients_satisfied = meal_key_ingredients + dinner_key_ingredients
            print(key_ingredients_satisfied)

            if len(key_ingredients_satisfied) > 0:
                key_ingredients = [ki for ki in key_ingredients if ki not in key_ingredients_satisfied]
            else:
                continue
        else:
            # Recover discarded recipes
            pass

        meal, dinner = (my_meals.pop(meal_candidate_idx), my_dinners.pop(dinner_candidate_idx))

        cs = CookidooScrapper
        cs.CookidooScrapper.login()
        cs.add_recipe_to_shopping_list(meal)
        cs.add_recipe_to_shopping_list(dinner)

        selected_recipes.append((meal, dinner))

    for idx, day in enumerate(week_days):
        meal, dinner = selected_recipes[idx]
        print('{:>12} ☀️ {}'.format(day, meal))
        print('{:>12}️ 🌚 {}'.format('', dinner))

    cs.driver.close()

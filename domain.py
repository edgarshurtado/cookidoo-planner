import random

from recipes import Recipe


def create_menu(week_days, my_meals: [Recipe], my_dinners: [Recipe], ingredients=[]) -> list[tuple]:
    selected_recipes = []
    no_selected_meals_idx_list = [idx for idx, _ in enumerate(my_meals)]
    no_selected_dinners_idx_list = [idx for idx, _ in enumerate(my_dinners)]
    while len(selected_recipes) < len(week_days):

        if len(no_selected_dinners_idx_list) == 0 or len(no_selected_meals_idx_list) == 0:
            break

        meal_candidate_idx, dinner_candidate_idx = (
            random.randrange(len(no_selected_meals_idx_list)), random.randrange(len(no_selected_dinners_idx_list)))

        meal, dinner = (my_meals[no_selected_meals_idx_list.pop(meal_candidate_idx)],
                        my_dinners[no_selected_dinners_idx_list.pop(dinner_candidate_idx)])

        candidate_recipe_ingredients = meal.ingredients + dinner.ingredients
        if len(ingredients_left_to_satisfy) == 0:
            selected_recipes.append((meal, dinner))
        else:
            satisfied_ingredients = set(meal.ingredients_satisfied(candidate_recipe_ingredients) + dinner.ingredients_satisfied(candidate_recipe_ingredients))
            if len(satisfied_ingredients) > 0:
                ingredients_left_to_satisfy -= satisfied_ingredients
                selected_recipes.append((meal, dinner))
            else:
                no_selected_meals_idx_list.append(meal_candidate_idx)
                no_selected_dinners_idx_list.append(dinner_candidate_idx)

    return selected_recipes

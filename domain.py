import random


def create_menu(week_days, my_meals, my_dinners, ingredients=[]) -> list[tuple]:
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

        selected_recipes.append((meal, dinner))

    return selected_recipes

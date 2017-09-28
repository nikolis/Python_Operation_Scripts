from src.impl.htmlproc import *


def test_find_combined_quantity_math_multiplication():
    result = find_combined_quantity("4 x 300g aged")
    assert(result[0] == 1200)
    assert(result[1] == 'g')
    assert(result[2] == 'aged')


def test_find_combined_quantity_number_mo_comment_1():
    result = find_combined_quantity("3 tbsp chopped")
    assert(result[0] == 3)
    assert(result[1] == 'tbsp')
    assert(result[2] == 'chopped')


def test_find_combined_quantity_number_mo_comment_2():
    result = find_combined_quantity('400g fresh')
    assert (result[0] == 400)
    assert (result[1] == 'g')
    assert (result[2] == 'fresh')


def test_get_recipe_from_url():
    url = "http://www.bbc.co.uk/food/recipes/aged_sirloin_steak_with_62354"
    recipe = get_recipe_from_url(url)
    assert(len(recipe.ingredientEntrySets) == 4)
    ingredient_entry_sets_list = sorted(recipe.ingredientEntrySets, key=lambda x: x.title, reverse=False)
    assert(ingredient_entry_sets_list[2].title == 'Ingredients')
    ingredient_list = sorted(ingredient_entry_sets_list[2].ingredientEntries, key=lambda x: x.name, reverse=False)
    assert (ingredient_list[0].name == 'black pepper')
    assert (ingredient_list[1].name == 'olive oil')
    assert (ingredient_list[1].quantity == 4)
    assert (ingredient_list[1].measurementUnit == 'tbsp')
    assert (ingredient_list[2].name == 'sirloin')
    assert (ingredient_list[2].quantity == 1200)
    assert (ingredient_list[2].measurementUnit == 'g')
    assert (ingredient_list[2].postComment.strip(', ') == 'steaks')
    assert (ingredient_list[2].preComment.strip(', ') == 'aged')




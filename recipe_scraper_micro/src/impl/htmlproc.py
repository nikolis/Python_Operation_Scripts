# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re 
import nltk 
from src.impl.utils import *

multiplyer = 'x'
rangeOperator = '-'
measurement_units=["small","big","leaves","clove","cloves","oz","tsp","tbsp","kg","fl","ml","bunch","slices","rashers","g","lb","jar"]


def list_ingredients(ingredients_tag):
    """This method gets as a parameter the complete Div object that found to belong 
    in the 'recipe-ingredients' class"""
    recipe_ingredients = {}
    string_ingredients_tag = str(ingredients_tag)
    soap_temp = BeautifulSoup(string_ingredients_tag, 'html.parser')
    header_tags = soap_temp.find_all(re.compile('h\d'))
    list_tags = soap_temp.find_all("ul")
    loop_counter = 0
    for listTag in list_tags:
        ingredient_entries = extract_ingredients_from_list(str(listTag))
        recipe_ingredients.update({header_tags[loop_counter].text: ingredient_entries})
        loop_counter += 1
    return recipe_ingredients


def extract_ingredients_from_list(u_list):
    """This method gets as a parameter a <ul> html object whis should contain the
    ingredients we need to parse and save"""
    ingredient_entries = []
    u_list = encode_escape_chars(u_list)
    soap_temp = BeautifulSoup(u_list, 'html.parser')
    list_items = soap_temp.find_all('li')
    for item in list_items:
        children = item.children 
        ingredient_entry = get_ingredient_from_children(children)
        ingredient_entries.append(ingredient_entry)
    return ingredient_entries


def get_ingredient_from_children(children):
    childNum = 1
    measurementUnit =None
    pre_object_description =None
    post_object_description = None
    ingredient = None
    quant =-1
    for child in children:
        child = get_rid_of_backslashes(child.string)        
        if childNum == 1:
            result = handle_first_child(child)
            quant, measurementUnit, pre_object_description = result[0],result[1],result[2]
        elif childNum == 2:
            ingredient = str(child)
        elif childNum == 3:
            post_object_description = decode_escape_chars(str(child))
        childNum += 1
        if post_object_description is not None:
            post_object_description = post_object_description.lstrip(' ,')
    return quant, measurementUnit, pre_object_description, ingredient, post_object_description


def handle_first_child(first_child):
    measurement_unit = None
    further_description = None
    ingredient_entry = find_combined_quantity(first_child)
    quantity = ingredient_entry[0]
    if ingredient_entry[1] is None and ingredient_entry[2]:
        for mo in measurement_units:
            loop_counter = 0
            description_tokens = ingredient_entry[2].split(" ")
            for token in description_tokens:
                if token == mo:
                    measurement_unit = mo
                    further_description = " ".join(description_tokens[0:loop_counter] + description_tokens[loop_counter+1:])
                    loop_counter+=1
            if measurement_unit:
                further_description = ingredient_entry[2].replace(measurement_unit, "")
            else :
                further_description = ingredient_entry[2]
    else:
        measurement_unit = ingredient_entry[1]
        further_description = ingredient_entry[2]
    return quantity, measurement_unit, further_description


def find_combined_quantity(raw):
    """ Return a tuple that has 3 members the 
    0) should be a number representing quantity
    1) Should be a measurement Unit for the quantity
    2) Should have remaining descriptions
    if any of this parts is not found it's place should be None in the tuple"""
    combined_number = 0
    temp_container = 0
    remaining_description = ['']
    multiplier = False
    nrange = False
    loop_counter =0
    measurement_unit = None
    raw_array = raw.split(" ")
    print(raw)
    for token in raw_array:
        result = is_number(token)
        # if result contains number
        if result:
            # if result contains number and measurement unit
            if result[0] and result[1]:
                measurement_unit = result[1]
                if combined_number != 0:
                    if multiplier and temp_container != 0:
                        combined_number -= temp_container
                        combined_number += temp_container * result[0]
                        multiplier = False
                        combined_number = combined_number
                else:
                    combined_number = result[0]
            elif result[0]:
                temp_container = result[0]
                combined_number += result[0]
        else:
            if token == "x" or token == "*" or token == "X":
                multiplier = True
            elif token == "-":
                nrange = True
            elif token in measurement_units:
                measurement_unit = token
            else:
                remaining_description.append(token)
                loop_counter += 1
    return combined_number, measurement_unit, " ".join(remaining_description).lstrip()


recipe_urls = ['http://www.bbc.co.uk/food/recipes/aged_sirloin_steak_with_62354',
               'http://www.bbc.co.uk/food/recipes/sirloin_steak_with_new_91595',
               'http://www.bbc.co.uk/food/recipes/roast_chicken_thigh_41789',
               'http://www.bbc.co.uk/food/recipes/crown_of_chicken_with_00717',
               'http://www.bbc.co.uk/food/recipes/roastbabychickenwith_91388',
               'http://www.bbc.co.uk/food/recipes/xxxxx_36916']


class Recipe:
    def __init__(self, title=None, original_url=None, author=None, prep_time=None, cooking_time=None, servings=None):
        self.title = title
        self.ingredientEntrySets = []
        self.original_url = original_url
        self.author = author
        self.prep_time = prep_time
        self.cooking_time = cooking_time
        self.serving = servings

    def reprJSON(self):
        return dict(title=self.title, ingredientEntrySets=self.ingredientEntrySets)


class IngredientEntrySet:
    def __init__(self, title):
        self.title=title
        self.ingredientEntries = []
    
    def reprJSON(self):
        return dict(title=self.title, ingredientEntries=self.ingredientEntries)


class IngredientEntry:
    def __init__(self, quantity, measurement_unit, pre_comment, name, post_comment):
        self.quantity = quantity
        self.measurementUnit=measurement_unit
        self.preComment = pre_comment
        self.name = name
        self.postComment = post_comment

    def reprJSON(self):
        return dict(quantity=self.quantity, measurementUnit=self.measurementUnit, preComment=self.preComment, name=self.name, postComment=self.postComment)


def get_recipe_from_url(recipe_url):
    html_document = urlopen(recipe_url).read()
    ingredient_tag = find_tag(html_document, 'div', 'recipe-ingredients')
    prep_time = find_tag(html_document, 'p', 'recipe-metadata__prep-time')
    cooking_time = find_tag(html_document, 'p', 'recipe-metadata__cook-time')
    servings = find_tag(html_document, 'p', 'recipe-metadata__serving')
    author = find_tag(html_document, 'a', 'chef__link')
    ingredient_list = list_ingredients(ingredient_tag)
    title = parse_recipe_title(html_document)
    recipe = Recipe(title, recipe_url, author, prep_time, cooking_time, servings)
    for name in ingredient_list:
        ingredient_entry_set = IngredientEntrySet(name)
        for entry in ingredient_list[name]:
            ingredient_entry = IngredientEntry(entry[0], entry[1], entry[2], entry[3], entry[4])
            ingredient_entry_set.ingredientEntries.append(ingredient_entry)
        recipe.ingredientEntrySets.append(ingredient_entry_set)
    method_parts = parse_recipe_method(html_document)
    return recipe 


def get_next():
    return get_recipe_from_url(recipe_urls[4])

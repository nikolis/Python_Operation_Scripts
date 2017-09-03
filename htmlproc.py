# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import urlopen
import re 
import base64 

escapeCharacters =['½','¼','¾','','','','','','']
base64encoded_points =[]


def _findIngredientsTag(soup):
    tags = soup.find_all('div')
    for tag in tags:
        retTags =[]
        attributes = tag.attrs 
        if((not attributes is None) and('class' in attributes.keys()) and (tag['class']==['recipe-ingredients'])):
            return tag

def _listIngredients(ingredientsTag):
    stringIngredientsTag = str(ingredientsTag) 
    soapTemp = BeautifulSoup(stringIngredientsTag,'html.parser')
    header_tags =soapTemp.find_all(re.compile('h\d'))
    list_tags =soapTemp.find_all("ul")
    for listTag in list_tags:
        _extract_ingredients_from_list(str(listTag))

def _extract_ingredients_from_list(ulist):
    print("-----------------------------------------")

    soapTemp = BeautifulSoup(ulist,'html.parser')
    print(ulist)
    #print(soapTemp)
    listItems = soapTemp.find_all('li')
    for item in listItems:
        stringItem = str(item)
        print(stringItem.decode('utf-8'))
        print("---->")



def encode_escape_chars(string):
    tempString = string
    for ch in escapeCharacters:
        index = tempString.find(ch)
        if(index != -1):
            newString = tempString[:index]+base64.b64encode(tempString[index:index+len(ch)])+tempString[index+len(ch):]
            base64encoded_points.append(base64.b64encode(tempString[index:index+len(ch)]))
            tempString = newString 
    return tempString


def decode_escape_chars(string):
    for ch in base64encoded_points:
        index = string.find(ch)
        if(index != -1):
            newString = string[:index]+base64.b64decode(string[index:index+len(ch)])+string[index+len(ch):]
            string = newString
    return string




recipe_urls = ['http://www.bbc.co.uk/food/recipes/aged_sirloin_steak_with_62354',
                            'http://www.bbc.co.uk/food/recipes/sirloin_steak_with_new_91595',
                            'http://www.bbc.co.uk/food/recipes/roast_chicken_thigh_41789',
                            'http://www.bbc.co.uk/food/recipes/crown_of_chicken_with_00717',
                            'http://www.bbc.co.uk/food/recipes/roastbabychickenwith_91388',
                            'http://www.bbc.co.uk/food/recipes/xxxxx_36916']
url = recipe_urls[0];
htmlDoc = urlopen(url).read()
soup = BeautifulSoup(htmlDoc, 'html.parser')
#soup = BeautifulSoup(markup, 'html.parser')
#script_tag = soup.script

#while(script_tag):
#script_tag.decompose()
#script_tag = soup.script

#soup.head.decompose()
#print (soup.prettify())
ingredient_tag = _findIngredientsTag(soup)
ingredientList = _listIngredients(ingredient_tag)

print ingredientList


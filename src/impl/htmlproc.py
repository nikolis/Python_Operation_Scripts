# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re 
import nltk 
import base64 

escapeCharacters =['½','¼','¾','¼']
escapeCharsMatcher ={'½':0.5, '¼':0.25, '¾':0.75}

base64encoded_points =set()
multiplyer = 'x'
rangeOperator = '-'
measurement_units=["small","big","leaves","clove","cloves","oz","tsp","tbsp","kg","fl","ml","bunch","slices","rashers","g","lb","jar"]

def _find_ingredients_tag(htmlDoc):
    """This method is responsible for geting an html Document and finding the div object
    that belongs to the CSS class 'recipe-ingredients'"""
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    tags = soup.find_all('div')
    for tag in tags:
        retTags =[]
        attributes = tag.attrs 
        if((not attributes is None) and('class' in attributes.keys()) and (tag['class']==['recipe-ingredients'])):
            return tag

def _list_ingredients(ingredientsTag):
    """This method gets as a parameter the complete Div object that found to belong 
    in the 'recipe-ingredients' class"""
    recipeIngredients = {}
    stringIngredientsTag = str(ingredientsTag) 
    soapTemp = BeautifulSoup(stringIngredientsTag,'html.parser')
    header_tags =soapTemp.find_all(re.compile('h\d'))
    list_tags =soapTemp.find_all("ul")
    loopCounter = 0 
    for listTag in list_tags:
        ingredientEntries =  _extract_ingredients_from_list(str(listTag))
        recipeIngredients.update({header_tags[loopCounter].text:ingredientEntries})
        loopCounter+=1
    return recipeIngredients

def _extract_ingredients_from_list(ulist):
    """This method gets as a parameter a <ul> html object whis should contain the
    ingredients we need to parse and save"""
    ingredientEntries = []
    ulist = __encode_escape_chars(ulist)
    soapTemp = BeautifulSoup(ulist,'html.parser')
    listItems = soapTemp.find_all('li')
    for item in listItems:
        children = item.children 
        ingredientEntry = get_ingredient_from_children(children)
        ingredientEntries.append(ingredientEntry)
    return ingredientEntries 

def get_ingredient_from_children(children):
    childNum = 1
    measurementUnit =None
    pre_object_description =None
    quant =-1
    for child in children:
        child = _get_rid_of_backslashes(child.string)        
        if (childNum ==1):
            result = handle_first_child(child)
            quant, measurementUnit, pre_object_description = result[0],result[1],result[2]
        childNum+=1
    return (quant,measurementUnit,pre_object_description)


def handle_first_child(firstChild):
    measurementUnit =None
    furtherDesc =None
    quant =-1
    
    ingredientEntry = find_combined_quantity(firstChild)
    quant = ingredientEntry[0]
    if(ingredientEntry[1]==None and ingredientEntry[2]):
        for mo in measurement_units:
            loopCount =0
            descrTokens = ingredientEntry[2].split(" ")
            for token in descrTokens:
                if (token == mo):
                    measurementUnit=mo
                    furtherDesc = " ".join(descrTokens[0:loopCount] + descrTokens[loopCount+1:])
                loopCount+=1
            if(measurementUnit):
                furtherDesc = ingredientEntry[2].replace(measurementUnit,"")
            else :
                furtherDesc = ingredientEntry[2]
    else:
        measurementUnit = ingredientEntry[1]
        furtherDesc = ingredientEntry[2]
    return (quant,measurementUnit,furtherDesc)

def handle_second_child:

 """
def handle_third_child:
    """

def find_combined_quantity(raw):
    """ Return a tuple that has 3 members the 
    0) should be a number representing quantity
    1) Should be a measurement Unit for the quantity
    2) Should have remaining descriptions
    if any of this parts is not found it's place should be None in the tuple"""

    combinedNumber = 0
    tempContainer = 0
    remainingDescriptions = ['']
    multiplier = False ;
    nrange = False ;
    loopCounter =0
    rawArray = raw.split(" ")
    for token in rawArray:
        result = is_number(token)
        if(result):
            if(result[0] and result[1]):
                if combinedNumber != 0:
                    if multiplier and tempContainer != 0:
                        combinedNumber -= tempContainer 
                        combinedNumber += tempContainer * result[0]
                        multiplier = False ;
                        if(loopCounter != len(rawArray)):
                            return (combinedNumber, result[1], " ".join(rawArray[loopCounter+1:]))
                        return (combinedNumber, result[1], remainingDescriptions)
                    return (combinedNumber+result[0], result[1], remainingDescriptions)
                else:
                    return (result[0], result[1], None)
            elif(result[0]):
                tempContainer = result[0]
                combinedNumber+=result[0]
        else :
            if token == "x" or token == "*" or token =="X":
                multiplier = True
            elif token == "-":
                nrange = True
            else :
                remainingDescriptions.append(token)
        loopCounter+=1
    return (combinedNumber,None, " ".join(remainingDescriptions))   





def is_number(token):
    """String:input, Tuple:output this function gets a string token as parameter
    and return a tuple containing either a number and and None if there is nothing more
    in the token or the tuple containing a number and a string that remained which
    is speculated to be the measurement Unit"""
    result = re.match(r'\d+',token)
    if(result):
        if(result.start() == 0 and result.end() == token):
            return (int(token), None)
        else:
            if (result.start()==0):
                return (int(token[result.start():result.end()]), token[result.end():])
            elif (result.start()>0):
                (int(token[result.start():result.end()]), token[:result.start])
    else : 
        if token in base64encoded_points:
            if(type(token) != str):
                token = token.decode('utf-8')
            else:
                token = bytes(token,'utf-8')
                token = token.decode('utf-8')
            decodedToken = __decode_escape_chars(str(token))
            return (escapeCharsMatcher.get(decodedToken), None)


def __encode_escape_chars(string):
    """Encodes base64 string parameter and returns it 
    and als appends the encoded form in base64encoded_points for decoding"""
    tempString = string
    for ch in escapeCharacters:
        index = tempString.find(ch)
        while(index != -1):
            newString = tempString[:index]+str(base64.b64encode(bytes(tempString[index:index+len(ch)],'utf-8')))+tempString[index+len(ch):]
            base64encoded_points.add(str(base64.b64encode(bytes(tempString[index:index+len(ch)], 'utf-8'))))
            tempString = newString
            index = tempString.find(ch)
    return tempString

def __decode_escape_chars(string):
    """This method only decodes base64 encoded strings that exist in base64encoded_points 
    the only reason for that is not to decode any data not encoded by this script"""
    string = str(string.encode('utf-8'))
    for ch in base64encoded_points: 
        index = string.find(ch)
        if(index != -1 and index == 0 and len(string)==len(ch)  ):
            newString = base64.b64decode(string[index:index+len(ch)])
            string = newString
    return string


def _get_rid_of_backslashes(string):
    """The backslashes in our context gives as an alternative
    but four our purpuse of quantifying the ingredients for the recipes
    it's just make things a bit more complicated so this method removes completly the
    second alternative"""
    index = string.find('/')
    counter =0
    if(index != -1):
        spaceIndex = string[index+1:].find(r' ')
        return string[:index]+string[spaceIndex+index+1:]
    return string




recipe_urls = ['http://www.bbc.co.uk/food/recipes/aged_sirloin_steak_with_62354',
        'http://www.bbc.co.uk/food/recipes/sirloin_steak_with_new_91595',
        'http://www.bbc.co.uk/food/recipes/roast_chicken_thigh_41789',
        'http://www.bbc.co.uk/food/recipes/crown_of_chicken_with_00717',
        'http://www.bbc.co.uk/food/recipes/roastbabychickenwith_91388',
        'http://www.bbc.co.uk/food/recipes/xxxxx_36916']

url = recipe_urls[0];
htmlDoc = urlopen(url).read()
ingredient_tag = _find_ingredients_tag(htmlDoc)
ingredientList = _list_ingredients(ingredient_tag)
for entity in ingredientList:
    print(entity," : ",ingredientList.get(entity))

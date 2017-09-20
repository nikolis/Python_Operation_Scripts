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

def _find_tag(htmlDoc,object_type, class_of_tag):
    """This method is responsible for geting an html Document and finding the div object
    that belongs to the CSS class 'recipe-ingredients'"""
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    tags = soup.find_all(object_type)
    for tag in tags:
        retTags =[]
        attributes = tag.attrs 
        if((not attributes is None) and('class' in attributes.keys()) and (tag['class']==[class_of_tag])):
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
    post_object_description = None
    ingredient = None
    quant =-1
    for child in children:
        child = _get_rid_of_backslashes(child.string)        
        if (childNum ==1):
            result = handle_first_child(child)
            quant, measurementUnit, pre_object_description = result[0],result[1],result[2]
        elif(childNum ==2):
            ingredient = str(child)
        elif(childNum == 3):
            post_object_description = __decode_escape_chars(str(child))
        childNum+=1
    return (quant,measurementUnit,pre_object_description, ingredient, post_object_description)

def handle_first_child(first_child):
    measurementUnit =None
    furtherDesc =None
    quant =-1
    ingredientEntry = find_combined_quantity(first_child)
    quant = ingredientEntry[0]
    if(ingredientEntry[1]==None and ingredientEntry[2]):
        for mo in measurement_units:
            loopCount =0
            descrTokens = ingredientEntry[2].split(" ")
            for token in descrTokens:
                if (token == mo):
                    measurementUnit=mo
                    furtherDesc = " ".join(descrTokens[0:loopCount] + descrTokens[loopCount+1:])
                    #print(furtherDesc)
                loopCount+=1
            if(measurementUnit):
                furtherDesc = ingredientEntry[2].replace(measurementUnit,"")
            else :
                furtherDesc = ingredientEntry[2]
    else:
        measurementUnit = ingredientEntry[1]
        furtherDesc = ingredientEntry[2]
    #print(quant,measurementUnit,furtherDesc)
    return (quant,measurementUnit,furtherDesc)




def find_combined_quantity(raw):
    """ Return a tuple that has 3 members the 
    0) should be a number representing quantity
    1) Should be a measurement Unit for the quantity
    2) Should have remaining descriptions
    if any of this parts is not found it's place should be None in the tuple"""
    #print(raw)
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

                        #if(loopCounter != len(rawArray)):
                            #return (combinedNumber, result[1], " ".join(rawArray[loopCounter+1:]))
                        #return (combinedNumber, result[1], remainingDescriptions)
                    #return (combinedNumber+result[0], result[1], remainingDescriptions)
                combinedNumber = combinedNumber+result[0]
                remainingDescriptions.append(result[1])
                #else:
                    #return (result[0], result[1], None)
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
    #print(combinedNumber,None, " ".join(remainingDescriptions))
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
            decodedToken = __decode_escape_chars(token)
            return (escapeCharsMatcher.get(decodedToken), None)


def __encode_escape_chars(string):
    """Encodes base64 string parameter and returns it 
    and als appends the encoded form in base64encoded_points for decoding"""
    tempString = string
    for ch in escapeCharacters:
        index = tempString.find(ch)
        while(index != -1):
            encodedBytes =  base64.b64encode(tempString[index:index+len(ch)].encode('utf-8'))
            newString = tempString[:index]+ encodedBytes.decode('utf-8')+tempString[index+len(ch):]
            base64encoded_points.add(encodedBytes.decode('utf-8'))
            tempString = newString
            index = tempString.find(ch)
    return tempString

def __decode_escape_chars(string):
    """This method only decodes base64 encoded strings that exist in base64encoded_points 
    the only reason for that is not to decode any data not encoded by this script"""
    repeatFlag = False
    for ch in base64encoded_points:
        repeatFlag = True ;
        while(repeatFlag):
            ch = str(ch)
            index = string.find(ch)
            if(index != -1 and index == 0 and len(string)==len(ch)  ):
                newString = base64.b64decode(string[index:index+len(ch)]).decode('utf-8')
                return newString
            elif(index != -1):
                string = string[0:index]+base64.b64decode(string[index:index+len(ch)]).decode('utf-8')+ string[index+len(ch):]   
                repeatFlag = True
            else :
                repeatFlag = False 
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

def _parse_recipe_method(htmlDoc):
    recipe_method_tag = _find_tag(htmlDoc,'div','recipe-method-wrapper')
    soup = BeautifulSoup(str(recipe_method_tag), 'html.parser')
    tags = soup.find_all('li')
    method_parts =[]
    for tag in tags:
        method_parts.append(tag.text)
    return method_parts

def _parse_recipe_title(htmlDoc):
    recipe_title_tag = _find_tag(htmlDoc,'h1','content-title__text')
    return(recipe_title_tag.text)


def get_next_recipe(recipe_url):
    recipe_list = []
    htmlDoc = urlopen(recipe_url).read()
    ingredient_tag = _find_tag(htmlDoc, 'div','recipe-ingredients')
    prep_time = _find_tag(htmlDoc,'p','recipe-metadata__prep-time')
    cooking_time = _find_tag(htmlDoc,'p','recipe-metadata__cook-time')
    servings = _find_tag(htmlDoc,'p','recipe-metadata__serving')
    author = _find_tag(htmlDoc,'a','chef__link')
    ingredientList = _list_ingredients(ingredient_tag)
    method_parts = _parse_recipe_method(htmlDoc)
    title = _parse_recipe_title(htmlDoc)
    recipe_list.append((title, recipe_url, ingredientList, method_parts,prep_time.text, cooking_time.text,servings.text, author.text))
    return recipe_list   

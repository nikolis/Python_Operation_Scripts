import re
import base64
from bs4 import BeautifulSoup

base64encoded_points = set()
escapeCharacters = ['½', '¼', '¾', '¼']
escapeCharsMatcher = {'½': 0.5, '¼': 0.25, '¾': 0.75}


def is_number(token):
    """String:input, Tuple:output this function gets a string token as parameter
    and return a tuple containing either a number and and None if there is nothing more
    in the token or the tuple containing a number and a string that remained which
    is speculated to be the measurement Unit if No digit is detected in the string
    then only None is Returned and not a Tuple"""
    return_result = [None, None]
    token = token.split('/')[0]
    result = re.match(r'\d+', token)
    if result:
        # result matched from start to end
        if result.start() == 0 and result.end() == len(token):
            return_result[0] = int(token)
        else:
            if result.start() == 0:
                return_result[0] = int(token[result.start():result.end()])
                return_result[1] = token[result.end():]
            elif result.start() > 0:
                (int(token[result.start():result.end()]), token[:result.start])
    else:
        if token in base64encoded_points:
            decoded_token = decode_escape_chars(token)
            return_result[0] = escapeCharsMatcher.get(decoded_token)
    if return_result[0] is None and return_result[1] is None:
        return None
    if return_result[1] is not None:
        return_result[1] = return_result[1].lstrip()
    return return_result[0], return_result[1]


def encode_escape_chars(string):
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


def decode_escape_chars(string):
    """This method only decodes base64 encoded strings that exist in base64encoded_points 
    the only reason for that is not to decode any data not encoded by this script"""
    repeat_flag = False
    for ch in base64encoded_points:
        repeat_flag = True
        while repeat_flag:
            ch = str(ch)
            index = string.find(ch)
            if index != -1 and index == 0 and len(string)==len(ch):
                new_string = base64.b64decode(string[index:index+len(ch)]).decode('utf-8')
                return new_string
            elif index != -1:
                string = string[0:index]+base64.b64decode(string[index:index+len(ch)]).decode('utf-8') + \
                         string[index + len(ch):]
                repeat_flag = True
            else:
                repeat_flag = False
    return string


def get_rid_of_backslashes(string):
    """The backslashes in our context gives as an alternative
    but four our purpose of quantifying the ingredients for the recipes
    it's just make things a bit more complicated so this method removes completly the
    second alternative"""
    index = string.find('/')
    if index != -1:
        space_index = string[index+1:].find(r' ')
        return string[:index]+string[space_index+index+1:]
    return string


def find_tag(html_doc,object_type, class_of_tag):
    """This method is responsible for getting an html Document and finding the div object
    that belongs to the CSS class 'recipe-ingredients'"""
    soup = BeautifulSoup(html_doc, 'html.parser')
    tags = soup.find_all(object_type)
    for tag in tags:
        attributes = tag.attrs
        if (not attributes is None) and('class' in attributes.keys()) and (tag['class']==[class_of_tag]):
            return tag


def parse_recipe_method(html_doc):
    recipe_method_tag = find_tag(html_doc, 'div', 'recipe-method-wrapper')
    soup = BeautifulSoup(str(recipe_method_tag), 'html.parser')
    tags = soup.find_all('li')
    method_parts =[]
    for tag in tags:
        method_parts.append(tag.text)
    return method_parts


def parse_recipe_title(html_doc):
    recipe_title_tag = find_tag(html_doc, 'h1', 'content-title__text')
    return recipe_title_tag.text




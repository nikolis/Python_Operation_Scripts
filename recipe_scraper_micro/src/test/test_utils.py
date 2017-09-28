from src.impl.utils import *
    
def test_is_number_300g():
    result = is_number('300g')
    assert(result[0] == 300)
    assert(result[1] == 'g')


def test_is_number_x():
    result = is_number('x')
    assert(result == None)


def test_is_number_simple_number():
    result = is_number('5')
    assert(result[0] == 5)
    assert(result[1] is None)


def test_is_number_only_measurement_unit_tbsp():
    result = is_number('tbsp')
    assert(result is None)


def test_is_number_number_with_mo_space():
    result = is_number('4 tbsp')
    assert(result[0] == 4)
    assert(result[1] == 'tbsp')


def test_is_number_slash_separated_choices():
    result = is_number('400g/14oz')
    assert (result[0] == 400)
    assert (result[1] == 'g')


    



from  src.impl.htmlproc import *

def test_find_combined_quantity_math_multiplication():
    result = find_combined_quantity("4 x 300g aged");
    assert(result[0]==1200)
    assert(result[1]=='g')
    assert(result[2]=='aged')


def test_find_combined_quantity_number_mo_comment_1():
    result = find_combined_quantity("3 tbsp chopped")
    assert(result[0]==3)
    assert(result[1]=='tbsp')
    assert(result[2]=='chopped')

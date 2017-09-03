from nltk.corpus import wordnet as wn 

def test():
    food = wn.synset('food.n.01')
    types_of_food =food.hyponyms()
    for snset in types_of_food:
        print snset.lemmas()


index = []

def _index_ingredients():
    food = wn.synset('foodstuff.n.02')
    _find_leaves(food)    
    food = wn.synset('vegetable.n.01')
    _find_leaves(food) 
    food = wn.synset('vegetable.n.02')
    _find_leaves(food)
    food = wn.synset('food.n.01')
    _find_leaves(food)
    food = wn.synset('food.n.02')
    _find_leaves(food)
    food = wn.synset('food.n.03')
    _find_leaves(food)
    food = wn.synset('meat.n.01')
    _find_leaves(food) 
    food = wn.synset('root_vegetable.n.01')
    _find_leaves(food) 
    food = wn.synset('food_fish.n.01')
    _find_leaves(food)
    food = wn.synset('edible_fat.n.01')
    _find_leaves(food) 

def _find_leaves(originSynset):
    hyponyms = originSynset.hyponyms()
    if(hyponyms):
        for hyponym in hyponyms:
            _find_leaves(hyponym)
    lemma_names =  originSynset.lemma_names()
    for lemma_name in lemma_names:
        strLemma = lemma_name.encode('utf8')
        index.append(strLemma)


def search(word):
    if not index:
        _index_ingredients()
    sortedIndexSet = set(sorted(index, key=str.lower))
    count =0; 
    for sth in sortedIndexSet:
        print sth
        count+= len(sth)
    if word in index:
        print "Found"
    else:
        print "Not Found"
    print len(sortedIndexSet)
    print count 


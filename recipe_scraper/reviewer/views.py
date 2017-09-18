from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recipe,Ingredient
from .models import RecipeForm, IngredientEntryForm
from django.forms import  modelformset_factory, inlineformset_factory


def detail(request, recipe_id):
   recipe = get_object_or_404(Recipe, pk=recipe_id)
   print(recipe)
   return render(request, 'reviewer/detail.html', {'recipe' : recipe})

def result(request, recipe_id):
    response = "You're loking at the results of question %s"
    return HttpResponse(response % question_id)

def parse(request, index):
    recipe=Recipe.getRecipe(index)
    print(recipe)
    for ingredient in recipe.ingredient_list:
        print(ingredient.name)
    FormSet = inlineformset_factory(Recipe, IngredientEntry, fields=('part','quantity','measurement_unit','pre_comment','name','post_comment'))
    formSet = FormSet(instance = recipe)
    print(formSet.is_bound)
    return render(request, 'reviewer/parse.html', {'form': formSet})

def validate(request, recipe_title):
    return HttpResponse("You just approved")

def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:5]
    context= {
        'latest_recipe_list': latest_recipe_list, 
    }
    return render(request, 'polls/index.html', context)
     

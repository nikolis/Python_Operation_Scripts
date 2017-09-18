from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recipe,IngredientEntry
from .models import RecipeForm, IngredientEntryForm
from django.forms import  modelformset_factory


def detail(request, recipe_id):
   recipe = get_object_or_404(Recipe, pk=recipe_id)
   print(recipe)
   return render(request, 'reviewer/detail.html', {'recipe' : recipe})

def result(request, recipe_id):
    response = "You're loking at the results of question %s"
    return HttpResponse(response % question_id)

def parse(request, index):
    recipe=Recipe.getRecipe(index)
    recipeForm = RecipeForm(instance=recipe)
    return render(request, 'reviewer/parse.html', {'form': recipeForm})

def validate(request, recipe_title):
    return HttpResponse("You just approved")

def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:5]
    context= {
        'latest_recipe_list': latest_recipe_list,        
    }
    return render(request, 'polls/index.html', context)
     

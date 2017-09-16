from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recipe

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'reviewer/detail.html', {'recipe' : recipe})

def result(request, recipe_id):
    response = "You're loking at the results of question %s"
    return HttpResponse(response % question_id)

def approve(request, recipe_id):
    return HttpResponse("You just approved")

def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:5]
    context= {
        'latest_recipe_list': latest_recipe_list,        
    }
    return render(request, 'polls/index.html', context)
     

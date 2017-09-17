from django.conf.urls import url

from . import views

app_name = 'reviewer'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),        
    url(r'^(?P<recipe_id>[0-9]+)/result/$', views.result, name='result'),   
    url(r'^/validate/$', views.validate, name='validate'),   
    url(r'^([0-9]+)/parse/$', views.parse, name='parse'),
]

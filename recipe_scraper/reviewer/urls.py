from django.conf.urls import url

from . import views

app_name = 'reviewer'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),        
    url(r'^(?P<recipe_id>[0-9]+)/result/$', views.result, name='result'),   
    url(r'^(?P<recipe_id>[0-9]+)/approve/$', views.approve, name='approve'),   
	url(r'^([0-9]+)/parse/$', views.parse, name='parse'),
]

from django.conf.urls import patterns, url

from lists import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^getlist/(?P<sender_name>\w+)/$', views.get_list, name='get_list')
)

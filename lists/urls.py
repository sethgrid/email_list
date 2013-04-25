from django.conf.urls import patterns, url

from lists import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^getlist/(?P<sender_name>\w+)/update_subscription/(?P<email_address>\w+)/subscribed/(?P<yes_no>\w+)/$', views.update_subscription, name='update_subscription'),
    url(r'^getlist/(?P<sender_name>\w+)/update_subscription/(?P<email_address>\w+)/subscribed/$', views.show_subscription, name='show_subscription'),
    url(r'^getlist/(?P<sender_name>\w+)/delete/(?P<email_address>\w+)/$', views.delete_email, name='delete_email'),
    url(r'^getlist/(?P<sender_name>\w+)/add/(?P<email_address>\w+)/$', views.add_email, name='add_email'),
    url(r'^getlist/(?P<sender_name>\w+)/unsubscribes/$', views.get_unsubscribed, name='get_unsubscribed'),
    url(r'^getlist/(?P<sender_name>\w+)/subscribes/$', views.get_subscribed, name='get_subscribed'),
    url(r'^getlist/(?P<sender_name>\w+)/$', views.get_list, name='get_list'),
)

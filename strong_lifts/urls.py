from django.conf.urls import url

from . import views

app_name = 'strong_lifts'

# set urls for strong_lifts app
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.login, name='login')
]
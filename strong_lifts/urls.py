from django.conf.urls import url

from . import views

app_name = 'strong_lifts'

# set urls for strong_lifts app
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register_user, name='register_user'),
        url(r'^login/', views.login_user, name='login_user')
]
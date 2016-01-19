from django.conf.urls import url
from . import views

# set urls for strong_lifts app
urlpatterns = [
        url(r'^$', views.index, name='index'),
]
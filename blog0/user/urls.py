from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^test', views.reg),
    url(r'^login$', views.login),
    url(r'^atest$', views.test),
]
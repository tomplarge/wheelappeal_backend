from django.conf.urls import url
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', views.api, name='api'),
    url(r'^submit/', views.submit, name='submit'),
]

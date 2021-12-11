from django.urls import path

from .import views


urlpatterns = [
    path('search', views.search_stock, name = 'search_stock'),
    path('login',views.login, name = "login"),
    path('',views.index, name = "index")
]

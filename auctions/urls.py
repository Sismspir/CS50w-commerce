from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auctions/<str:title>", views.display, name="title"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("delete", views.delete, name="delete"),
    path("add", views.add, name="add"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.categories, name="categories"),
]

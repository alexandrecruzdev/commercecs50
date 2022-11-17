from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list/",views.create_list,name="create_list"),
    path("list_details/<int:id_auction>",views.list_details, name="list_details"),
    path("addWatchList/<int:id_auction>",views.addWatchList, name="addWatchList"),
    path("deleteWatchList/<int:id_auction>",views.deleteWatchList, name="deleteWatchList"),
    path("watchlist/",views.watchlist, name="watchlist"),
    path("showQtdWatchlist/",views.showQtdWatchlist, name="showQtdWatchlist")



]


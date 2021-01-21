from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("<int:listing_id>", views.addcomment, name="addcomment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("newList", views.newList, name="newList"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("mylisting/<int:listing_id>", views.mylisting, name="mylisting"),
    path("mylisting/<int:listing_id>", views.changestatus, name="changestatus"),
    path("closedlisting/", views.closedlisting, name="closedlisting"),
    path("categorieslisting/", views.categorieslisting, name="categorieslisting"),
    path("categorydetail/<str:category>", views.categoriesdetail, name="categorydetail")

]
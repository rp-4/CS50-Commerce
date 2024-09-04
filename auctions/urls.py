from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #path("listings", views.listings, name="listings"),
    path("<int:listing_id>", views.listing_view, name="listing_view"),
    path("edit/<int:listing_id>", views.listing_edit, name="listing_edit"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("listing_new", views.listing_new, name="listing_new"),
]

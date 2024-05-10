from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('add_auction_listing', views.add_auction_listing, name='add_auction_listing'),
    path('wishlist_view', views.wishlist_view, name='wishlist_view'),
    path('categories', views.categories, name='categories'),
    path('<int:Listing_id>', views.Listing_Page, name='listing_page'),
    path('<str:Listing_id>', views.invalid_listing_id, name='invalid_listing_id'),
    path('<int:Listing_id>/place_bid', views.place_bid, name='place_bid'),
    path('<int:Listing_id>/Add_Wishlist', views.Add_Wishlist, name='Add_Wishlist'),
    path('<int:Listing_id>/rem_Wishlist', views.rem_Wishlist, name='rem_Wishlist'),
    path('<int:Listing_id>/close_bidding', views.close_bidding, name='close_bidding'),
    path('<int:Listing_id>/add_comment', views.add_comment, name='add_comment'),
    path('unauthorized', views.unauthorized_access, name='unauthorized'),
]

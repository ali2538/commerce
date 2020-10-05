from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>', views.listing, name='listing'),
    path('categories', views.categories, name='categories'),
    path('categories/<str:category>', views.category, name='category'),
    path('add_to_watchlist/<int:listing_id>',
         views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:listing_id>',
         views.remove_from_watchlist, name='remove_from_watchlist')
]

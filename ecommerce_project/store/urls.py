from django.urls import path, include
from . import views

# For media management :-
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("register/", views.user_register, name="user_register"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("product-view/<int:productid>/update_item/", views.update_item_by_view, name="product_view_update_item"),
    path("product-view/<productid>/", views.view_product, name="product_view"),
    path("update_item/", views.update_item, name="update_item"),
    path("cart/update_item/", views.update_item, name="cart_update_item"),
    path("search/", views.product_search, name="searching_product"),
    path("search/product-view/<productid>/", views.view_product, name="search_product_view"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)























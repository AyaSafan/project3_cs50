from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("main", views.main, name="main"),
    path("logout", views.logout, name="logout"),
    path("edit", views.edit, name="edit"),
    path("menu", views.menu, name="menu"),
    path("order_item", views.order_item, name="order_item"),
    path("cart", views.cart, name="cart"),
    path("place_order", views.place_order, name="place_order"),
    path("<int:order_id>/delete", views.delete, name="delete"),
    path("myorders", views.myorders, name="myorders"),
    path("allorders", views.allorders, name="allorders"),
    path("<int:order_id>/done", views.done, name="done")
]

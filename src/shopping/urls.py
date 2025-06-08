from django.urls import path

from shopping import views

urlpatterns = [
    path("", views.splash, name="splash"),
    path("lists/", views.lists, name="lists"),
    path(
        "shopping-list/<int:pk>/",
        views.shopping_list_detail,
        name="shopping_list_detail",
    ),
    path(
        "shopping-list/<int:pk>/send/",
        views.send_shopping_list,
        name="send_shopping_list",
    ),
    path(
        "shopping-list/<int:list_pk>/delete/<int:item_pk>/",
        views.delete_item,
        name="delete_item",
    ),
    path(
        "shopping-list/<int:pk>/delete/",
        views.delete_shopping_list,
        name="delete_shopping_list",
    ),
    path(
        "shopping-list/<int:list_pk>/edit/<int:item_pk>/",
        views.edit_item,
        name="edit_item",
    ),
]

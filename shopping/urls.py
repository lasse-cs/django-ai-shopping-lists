from django.urls import path

from shopping import views

urlpatterns = [
    path("", views.home, name="home"),
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
        "shopping-list/<int:list_pk>/delete-item/<int:item_pk>/",
        views.delete_item,
        name="delete_item",
    ),
]

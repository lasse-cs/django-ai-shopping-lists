from django.urls import path

from shopping import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "shopping-list/<int:pk>/",
        views.shopping_list_detail,
        name="shopping_list_detail",
    ),
]

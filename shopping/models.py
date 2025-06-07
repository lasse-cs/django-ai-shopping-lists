from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class ShoppingList(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        related_name="shopping_lists",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} - owned by {self.user.username}"

    def get_absolute_url(self):
        return reverse("shopping_list_detail", args=(self.pk,))


class ShoppingItem(models.Model):
    shopping_list = models.ForeignKey(
        ShoppingList,
        related_name="items",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"

from django import forms

from shopping.models import ShoppingItem, ShoppingList


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = [
            "name",
        ]


class ShoppingItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = [
            "name",
            "notes",
        ]

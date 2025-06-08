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


class SendShoppingListForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        help_text="Enter the email address to send the shopping list to.",
    )
    subject = forms.CharField(
        label="Subject",
        max_length=100,
        help_text="Enter the subject of the email.",
    )

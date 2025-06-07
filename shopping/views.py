from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from shopping.forms import ShoppingItemForm, ShoppingListForm
from shopping.models import ShoppingList


@login_required
def home(request):
    if request.method == "POST":
        shopping_form = ShoppingListForm(request.POST)
        if shopping_form.is_valid():
            shopping_list = shopping_form.save(commit=False)
            shopping_list.owner = request.user
            shopping_list.save()
            return redirect(shopping_list)
    else:
        shopping_form = ShoppingListForm()
    context = {
        "shopping_form": shopping_form,
    }
    return render(
        request,
        "shopping/home.html",
        context,
    )


@login_required
def shopping_list_detail(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    if request.method == "POST":
        item_form = ShoppingItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.shopping_list = shopping_list
            item.save()
            return redirect(shopping_list)
    else:
        item_form = ShoppingItemForm()
    context = {
        "shopping_list": shopping_list,
        "item_form": item_form,
    }
    return render(
        request,
        "shopping/shopping_list/detail.html",
        context,
    )

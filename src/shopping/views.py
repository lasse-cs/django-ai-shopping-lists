from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shopping.forms import ShoppingItemForm, ShoppingListForm, SendShoppingListForm
from shopping.models import ShoppingList
from shopping.tasks import send_shopping_list_email


def splash(request):
    return render(request, "shopping/splash.html")


@login_required
def lists(request):
    if request.method == "POST":
        shopping_form = ShoppingListForm(request.POST)
        if shopping_form.is_valid():
            shopping_list = shopping_form.save(commit=False)
            shopping_list.owner = request.user
            shopping_list.save()
            return redirect(shopping_list)
    else:
        shopping_form = ShoppingListForm()
    shopping_lists = ShoppingList.objects.filter(owner=request.user).order_by(
        "-created_at"
    )
    context = {
        "shopping_form": shopping_form,
        "shopping_lists": shopping_lists,
    }
    return render(
        request,
        "shopping/shopping_list/index.html",
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
            messages.success(request, 'Added item "%s".' % item.name)
            return redirect(shopping_list)
    else:
        item_form = ShoppingItemForm()
    context = {
        "shopping_list": shopping_list,
        "item_form": item_form,
        "send_list_form": SendShoppingListForm(),
    }
    return render(
        request,
        "shopping/shopping_list/detail.html",
        context,
    )


@login_required
@require_POST
def send_shopping_list(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    form = SendShoppingListForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = f"Shopping List: {shopping_list.name}\n\n"
        for item in shopping_list.items.all():
            message += f"- {item.name}: {item.notes}\n"
        send_shopping_list_email.enqueue(message, email, subject)
        messages.info(request, 'Sent shopping list to "%s".' % email)
    return redirect(shopping_list)


@login_required
@require_POST
def delete_item(request, list_pk, item_pk):
    shopping_list = get_object_or_404(ShoppingList, pk=list_pk, owner=request.user)
    item = get_object_or_404(
        shopping_list.items,
        pk=item_pk,
    )
    item.delete()
    messages.success(request, 'Deleted item "%s".' % item.name)
    return redirect(shopping_list)


@login_required
@require_POST
def delete_shopping_list(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    shopping_list.delete()
    messages.success(request, 'Deleted list "%s".' % shopping_list.name)
    return redirect("lists")


@login_required
def edit_item(request, list_pk, item_pk):
    shopping_list = get_object_or_404(ShoppingList, pk=list_pk, owner=request.user)
    item = get_object_or_404(shopping_list.items, pk=item_pk)

    if request.method == "POST":
        form = ShoppingItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(shopping_list)
    else:
        form = ShoppingItemForm(instance=item)

    context = {
        "item": item,
        "shopping_list": shopping_list,
        "item_form": form,
    }
    return render(request, "shopping/shopping_list/item_edit.html", context)

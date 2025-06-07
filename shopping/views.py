from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from langchain_openai import OpenAI
from shopping.forms import ShoppingItemForm, ShoppingListForm, SendShoppingListForm
from shopping.models import ShoppingList
from langchain.prompts import PromptTemplate


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
    shopping_lists = ShoppingList.objects.filter(owner=request.user).order_by(
        "-created_at"
    )
    context = {
        "shopping_form": shopping_form,
        "shopping_lists": shopping_lists,
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

        prompt_template = PromptTemplate.from_template(
            """
            Tell a delightful short commentary about the items in this shopping list: {message}.\n
            Do not include any personal information. Do not add any items that are not in the shopping list into the list.
            Keep the response short, under 100 words.
            """
        )
        prompt = prompt_template.invoke({"message": message})
        model = OpenAI(model="gpt-4o-mini", temperature=0.8)
        story = model.invoke(prompt)

        message += f"\n\nStory: {story}\n\n"

        send_mail(
            subject,
            message,
            from_email="shopping@hipposaur.co.uk",
            recipient_list=[email],
        )
    return redirect(shopping_list)


@login_required
@require_POST
def delete_item(request, list_pk, item_pk):
    shopping_list = get_object_or_404(ShoppingList, pk=list_pk, owner=request.user)
    get_object_or_404(
        shopping_list.items,
        pk=item_pk,
    ).delete()
    return redirect(shopping_list)

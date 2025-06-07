from django_tasks import task
from django.core.mail import send_mail
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    """
    Tell a delightful short commentary about the items in this shopping list: {message}.\n
    Do not include any personal information. Do not add any items that are not in the shopping list into the list.
    Keep the response short, under 100 words.
    """
)


def generate_story(message):
    prompt = prompt_template.invoke({"message": message})
    model = OpenAI(model="gpt-4o-mini", temperature=0.8)
    return model.invoke(prompt)


@task
def send_shopping_list_email(message, email, subject):
    story = generate_story(message)
    message_with_story = f"{message}\n\nStory: {story}\n\n"
    send_mail(
        subject,
        message_with_story,
        from_email="shopping@hipposaur.co.uk",
        recipient_list=[email],
    )

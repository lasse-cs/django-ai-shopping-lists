from django.template import Library

register = Library()


@register.filter
def bootstrap_class_for_message(message):
    match message.level_tag:
        case "info":
            return "info"
        case "success":
            return "success"
        case "warning":
            return "warning"
        case "error":
            return "danger"
        case _:
            return "secondary"

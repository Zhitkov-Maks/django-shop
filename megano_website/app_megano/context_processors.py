from .models import Tags


def load_tag(request):
    """Функция для вывода тегов в catalog.html. Сделал так как уже минимум в трех местах был повторяющийся код."""
    return {'tag_list': Tags.objects.all()}

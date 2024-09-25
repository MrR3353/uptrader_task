from django import template
from menu.models import MenuItem
from django.urls import resolve

register = template.Library()

@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = resolve(request.path_info).url_name

    # Запрашиваем все пункты меню по имени меню
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    def find_key_in_nested_dict(d, target_key):
        if target_key in d:
            return d[target_key]
        for key, value in d.items():
            if isinstance(value, dict):  # Если значение - это вложенный словарь
                result = find_key_in_nested_dict(value, target_key)
                if result is not None:
                    return result
        return None

    # Преобразуем список в дерево
    menu_tree = {}
    for item in menu_items:
        if not item.parent:
            menu_tree[item] = {}
        else:
            parent = find_key_in_nested_dict(menu_tree, item.parent)
            if parent is not None:
                parent[item] = {}
            else:
                # TODO: если дочерний элемент встретится раньше родительского
                pass

    # Определяем активный пункт
    active_item = None
    for item in menu_items:
        if item.get_url() == request.path or item.named_url == current_url:
            active_item = item
            break

    return {
        'menu_tree': menu_tree,
        'active_item': active_item,
        'menu_name': menu_name,
        'path': request.path,
    }


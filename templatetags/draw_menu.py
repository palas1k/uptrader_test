from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from tree_menu.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name: str):
    current_url = context.request.path
    menu_items = MenuItem.objects.filter(menu_name=menu_name).prefetch_related('menuitem_set')
    data = []
    for item in menu_items:
        data.append([item.id, item.url, item.named_url, item.parent_id, item.name])
        for child in item.menuitem_set.all():
            data.append([child.id, child.url, child.named_url, child.parent_id, child.name])

    def render_menu_item(item):
        active = False
        if menu_name in current_url:
            active = True
        children = [i for i in data if i[3] == item[0]]
        has_children = True if children else False
        html = '<li class="dropdown' + (' active' if active else '') + (' has-children' if has_children else '') + '">'
        if item[2]:
            html += f'<a href="/{item[2] if item[2] else item[1]}">{item[4]}</a>'
        if has_children:
            html += '<ul class="dropdown-menu">'
            for child in children:
                html += render_menu_item(child)
            html += '</ul>'
        html += '</li>'
        return html

    menu_html = ''
    for item in data:
        if not item[3]:
            menu_html += render_menu_item(item)
    return mark_safe(menu_html)

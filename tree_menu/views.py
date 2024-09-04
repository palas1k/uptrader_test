from django.shortcuts import render


def draw_menu_view(request, menu_name):
    context = {'menu_name': menu_name}
    return render(request, 'menu.html', context)

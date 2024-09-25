from django.shortcuts import render


def dynamic_view(request, url=None):
    return render(request, 'menu/base.html', {})

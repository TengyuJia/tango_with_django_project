from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
def index(request):
    #return HttpResponse("Rango says hey there partner!<a href=\"http://127.0.0.1:8000/rango/about\">About</a>")
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context=context_dict)
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context = context_dict)

def about(request):
    #return HttpResponse("Rango says this is about the page!<a href = \"http://127.0.0.1:8000/rango\">Index</a>")
    return render(request, 'rango/about.html')
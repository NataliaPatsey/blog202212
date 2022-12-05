from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<H1>hello from Django app</H1>")

def page1(request):
    return render(request, 'blog_app/page1.html')


def page2(request):
    return render(request, 'blog_app/page2.html')


def page(request, page_num):
    if page_num == 1:
        return render(request, 'blog_app/page1.html')
    elif page_num == 2:
        return render(request, 'blog_app/page2.html')

from django.shortcuts import render
from django.http import HttpResponse
from  blog_app.models import Article, Category

# Create your views here.
def index(request):
    data_all = Category.objects.all()
    return render(request, 'blog_app/index.html', {'all': data_all})


def category_item(request, cat_id):
    data = Article.objects.filter(category_id=cat_id)
    one = Category.objects.get(id=cat_id)
    return render(request, 'blog_app/category_item.html', {'data': data,
                                                           'one' : one})



def page1(request):

    data = {'page_num': 1,
            'text': 'Интеллектуальная транспортная система Sitronics Group основана на современных информационных, коммуникационных и телематических технологиях. Решение предназначено для автоматизированного поиска и принятия максимально эффективных сценариев управления транспортно-дорожным комплексом региона.'
            }

    data_list = [1, 'Интеллектуальная транспортная система Sitronics Group основана на современных информационных, коммуникационных и телематических технологиях. Решение предназначено для автоматизированного поиска и принятия максимально эффективных сценариев управления транспортно-дорожным комплексом региона.'
           ]

    return render(request, 'blog_app/page1.html', {'data_list': data_list} )


def page2(request):
    return render(request, 'blog_app/page2.html')


def page(request, page_num):
    if page_num == 1:
        return render(request, 'blog_app/page1.html')
    elif page_num == 2:
        return render(request, 'blog_app/page2.html')

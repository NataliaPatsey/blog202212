from django.shortcuts import render, redirect
from django.http import HttpResponse
from  blog_app.models import Article, Category, Favorite
from blog_app.forms import ArticleForm, ChoiceForm

# Create your views here.
def delete_item(request, item_id):
    article = Article.objects.get(pk=item_id).delete()
    return redirect('all_item')


def delete_item_care(request, item_id):
    if request.method == 'POST':
        article = Article.objects.get(pk=request.POST['item_id'])
        if request.POST['mychoice'] == '1' and article.user == request.user:
            article.delete()
            return redirect('my_item')
        return redirect('all_item')
    else:
        data = Article.objects.get(pk=item_id)
        menu2 = Category.objects.all()
        form = ChoiceForm()
        return render(request, 'blog_app/delete_item_care.html', {'menu2': menu2,
                                                                  'data': data,
                                                                  'form':form})


def update_item(request, item_id):
    article = Article.objects.get(pk=item_id)
    form = ArticleForm(instance=article)
    menu2 = Category.objects.all()
    if request.method == 'POST':
        article.edit_count += 1
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('one_item',item_id)
    return render(request, 'blog_app/add_item.html', {'menu2': menu2,
                                                      'form': form})


def add_item(request):
    form = ArticleForm()
    menu2 = Category.objects.all()
    if request.method == 'POST':
        # cat = Category.objects.get(id=request.POST['category'])
        # article = Article.objects.create(text=request.POST['text'],
        #                                  title=request.POST['title'],
        #                                  summary=request.POST['summary'],
        #                                  user=request.user,
        #                                  category=cat)

        article = ArticleForm(request.POST, request.FILES)
        if article.is_valid():
                article.save()

        return redirect('all_item')
    return render(request, 'blog_app/add_item.html', {'menu2': menu2,
                                                         'form': form})


def index(request):
    menu2 = Category.objects.all()
    data = Article.objects.all()
    return render(request, 'blog_app/index.html', {'menu2': menu2,
                                                   'data': data})


def favorite_item(request):
    menu2 = Category.objects.all()
    data = Favorite.objects.filter(user=request.user)
    return render(request, 'blog_app/favorite.html', {'menu2': menu2,
                                                   'data': data})

def one_item(request, item_id):
    menu2 = Category.objects.all()
    item = Article.objects.get(id=item_id)
    return render(request, 'blog_app/one_item.html', {'item': item,
                                                      'menu2': menu2})

def my_item(request):
    menu2 = Category.objects.all()
    data = Article.objects.filter(user=request.user)
    one = {'short_name': 'My articles'}
    return render(request, 'blog_app/my_item.html', {'data': data,
                                                           'one':one,
                                                     'menu2': menu2})


def category_item(request, cat_id):
    menu2 = Category.objects.all()
    data = Article.objects.filter(category_id=cat_id)
    one = Category.objects.get(id=cat_id)
    return render(request, 'blog_app/category_item.html', {'data': data,
                                                           'one' : one,
                                                           'menu2' : menu2})


def category_item_by_name(request, cat_name):
    data = Article.objects.filter(category__short_name=cat_name)
    one = {'short_name':cat_name}
    return render(request, 'blog_app/category_item.html', {'data': data,
                                                           'one' : one})


def all_item(request):
    data = Article.objects.all()
    one = 'Все статьи'
    return render(request, 'blog_app/all_item.html', {'data': data,
                                                           'one': one})


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

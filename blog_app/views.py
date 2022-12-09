from django.shortcuts import render, redirect
from django.http import HttpResponse
from  blog_app.models import Article, Category, Favorite
from blog_app.forms import ArticleForm, ChoiceForm, SearchForm

from django.core.files.storage import FileSystemStorage


from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required, permission_required
#
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.views.generic.base import View

#
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.views.generic.base import View

# Create your views here.

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "blog_app/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user=form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "blog_app/registration.html"
    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


def adm_get_group(request):
    group_lst = Group.objects.all()
    return render(request, 'blog_app/adm_get_group.html', {'group_lst': group_lst})

@login_required
@permission_required('auth.group.can_change_group',raise_exception=True)
def adm_compound_group(request, id):
    group = Group.objects.get(id=id)
    user_dellst = list()
    user_addlst = list()
    for user in User.objects.all():
        if user.groups.filter(name=group.name).exists():
            user_dellst.append(user)
        else:
            user_addlst.append(user)
    return render(request, 'blog_app/adm_compound_group.html', {'group': group,
                                                                'user_dellst': user_dellst,
                                                                'user_addlst': user_addlst})


@login_required
@permission_required('auth.group.change_group',raise_exception=True)
def adm_add_to_group(request,group_id,user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    group.user_set.add(user)
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)


def adm_del_from_group(request,group_id,user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    group.user_set.remove(user)
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)


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

@permission_required('blog_app.add_article',raise_exception=True)
def add_item(request):
    form = ArticleForm()
    menu2 = Category.objects.all()
    # if request.method == 'POST':
    #     cat = Category.objects.get(id=request.POST['category'])
    #     if request.FILES:
    #         uploded_img = request.FILES['image']
    #         fs = FileSystemStorage()
    #         filename = fs.save(uploded_img.name, uploded_img)
    #     else:
    #         filename = 'default.png'
    #     article = Article.objects.create(text=request.POST['text'],
    #                                      title=request.POST['title'],
    #                                      summary=request.POST['summary'],
    #                                      user=request.user,
    #                                      category=cat,
    #                                      image=filename)

    article = ArticleForm(request.POST, request.FILES)
    if article.is_valid():
        article.save()
        article_model = Article.objects.get(title=request.POST['title'],category__id=request.POST['category'])
        article_model.user = request.user
        article_model.save(update_fields=['user'])

        return redirect('all_item')
    return render(request, 'blog_app/add_item.html', {'menu2': menu2,
                                                         'form': form})


def index(request):
    menu2 = Category.objects.all()
    data = Article.objects.all()
    form = SearchForm()

    #session
    # visit = request.session.get('visit',0) +1
    # request.session['visit'] = visit
    # cookies
    if request.COOKIES.get('visit') is not None:
        visit = int(request.COOKIES.get('visit')) +1
        response = render(request, 'blog_app/index.html', {'menu2': menu2,
                                                   'form': form,
                                                   'visit': visit,
                                                   'data': data
        })
        response.set_cookie(key='visit', value=visit)
    else:
        response = render(request, 'blog_app/index.html', {'menu2': menu2,
                                                   'form': form,
                                                   'visit': 1,
                                                   'data': data
        })
        response.set_cookie(key='visit', value=1)
    return response

    # if request.method == 'POST':
    #     if request.POST['where'] == '1':
    #         data = Article.objects.filter(title__icontains=request.POST['searchtext'])
    #     elif request.POST['where'] == '2':
    #         data = Article.objects.filter(summary__icontains=request.POST['searchtext'])
    # return render(request, 'blog_app/index.html', {'menu2': menu2,
    #                                                'form': form,
    #                                                'visit': visit,
    #                                                'data': data})


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

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from blog_app.views import index,page1,page2,page, category_item, all_item, \
                        category_item_by_name, my_item, one_item, favorite_item,\
                        add_item, update_item, delete_item, delete_item_care

urlpatterns = [
    path('', index),
    path('page1/', page1, name='page1'),
    path('page2/', page2, name='page2'),
    path('page/<int:page_num>/', page, name='page'),
    path('category/<int:cat_id>/', category_item, name='category_item'),
    path('category_name/<str:cat_name>/', category_item_by_name, name='category_item_by_name'),
    path('my_articles/', my_item, name='my_item'),
    path('articles/', all_item, name='all_item'),
    path('articles/<int:item_id>/', one_item, name='one_item'),
    path('favorite/', favorite_item, name='favorite_item'),
    path('addarticle/', add_item, name='add_item'),
    path('updarticle/<int:item_id>/', update_item, name='update_item'),
    path('delarticle/<int:item_id>/', delete_item, name='delete_item'),
    path('delcarearticle/<int:item_id>/', delete_item_care, name='delete_item_care'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


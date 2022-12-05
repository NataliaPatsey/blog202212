from django.urls import path
from blog_app.views import index,page1,page2,page

urlpatterns = [
    path('', index),
    path('page1/', page1, name='page1'),
    path('page2/', page2, name='page2'),
    path('page/<int:page_num>/', page, name='page'),

]

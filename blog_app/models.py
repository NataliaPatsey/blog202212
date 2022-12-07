from django.db import models
import datetime

# Create your models here.
class Category(models.Model):
    short_name = models.CharField(max_length=20)
    about = models.CharField(max_length=50)

    def __str__(self):
        return self.short_name

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=False, blank=False )
    edit_count = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    summary = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)
    user = models.ForeignKey('auth.User', default=1, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_app/img/', default='blog_app/img/default.png')

    class Meta:
        unique_together = ['category', 'title']
        ordering = ["-title"]

    def __str__(self):
        return self.title

    @property
    def len_text(self):
        return len(self.text)

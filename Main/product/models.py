from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg, Count


class Category(MPTTModel):
    # Кортеж для панели администратора Для выбора статуса
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    # Для создания дерева категорий, мы хотим обозначить взаимосвязи между категориями
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)  # вот этого статуса
    slug = models.SlugField(null=False, unique=True)  # для вызова данных из БД через URL
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        cat = self.parent
        while cat is not None:
            full_path.append(cat.title)
            cat = cat.parent

        return ' / '.join(full_path[::-1])

    def get_absoulte_url(self):
        return reverse('category_detail', kwargs={'slug':self.slug})

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/', null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.IntegerField(default=0)
    minamount = models.IntegerField()
    detail = RichTextField()  # models.TextField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="auto" height="50"/>')
        else:
            return 'no image'

    def get_absoulte_url(self):
        return reverse('product_detail', kwargs={'slug':self.slug})
    #from django.db.models import Avg, Count
    def average_rating(self):
        av_rate = Comment.objects.filter(product=self, status=True).aggregate(average=Avg('rate'))
        av_rate = av_rate['average']
        if av_rate is not None:
            return round(float(av_rate),1)
        else:
            return 0.0

class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        return mark_safe(f'<p style="background-color:{self.code}">Color</p>')

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.SET_NULL,blank=True,null=True)
    size = models.ForeignKey(Size,on_delete=models.SET_NULL,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=50)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title


    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image()}" width="auto" height="50"/>')
        else:
            return 'no image'


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='images/', null=False)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="auto" height="50"/>')
        else:
            return 'no image'

#from django.contrib.auth.models import User
class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank = True)
    text = models.CharField(max_length=50, blank = True)
    rate = models.IntegerField(default = 5)
    ip = models.CharField(max_length=20, blank = True)
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
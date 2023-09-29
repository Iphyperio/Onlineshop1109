from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=150)
    image = models.ImageField(blank=True, upload_to='images/users/', default='images/users/default.jpg')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return f'{self.user.first_name} {self.user.last_name}+{self.user.username}'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="auto" height="50"/>')
        else:
            return 'no image'

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    college_name = models.CharField(max_length=50)
    SEMESTER = [
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', '6th'),
        ('7', '7th'),
        ('8', '8th')
    ]
    semester = models.CharField(max_length=1,choices=SEMESTER,)
    profile_image = models.ImageField(upload_to = 'profile_pics', blank=True)

    def save(self, *args, **kwargs):
        self.slug=slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'the_slug':self.slug})
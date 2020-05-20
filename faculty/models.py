from django.db import models
from django.utils.text import slugify


class Batch(models.Model):
    batch = models.CharField(max_length=1,blank=True)

    def __str__(self):
        return (self.batch)

class Category(models.Model):
    faculty = models.CharField(max_length=50, blank=True)
    slug = models.SlugField( blank=True)
    SEASONS = [('Y', "Year"),
               ('S', "Semester")]

    seasons = models.CharField(max_length=1, choices=SEASONS, blank=True)
    batches = models.ManyToManyField(Batch, blank=True)

    def __str__(self):
        return f'{self.faculty} '

    def save(self, *args, **kwargs):
        self.slug = slugify(self.faculty)
        super(Category, self).save(*args, **kwargs)

class Subject(models.Model):
    name = models.TextField(max_length=100)
    slug = models.SlugField( blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name}({self.category}-{self.batch})'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

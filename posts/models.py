import random
import string

from django.contrib.auth.models import User
from django.db import models

def randomString(stringLength=15):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class Batch(models.Model):
    SEMESTERS = [('1', '1st Sem'),
                 ('2', '2nd Sem'),
                 ('3', '3rd Sem'),
                 ('4', '4th Sem'),
                 ('5', '5th Sem'),
                 ('6', '6th Sem'),
                 ('7', '7th Sem'),
                 ('8', '8th Sem'), ]

    YEARS = [('1', '1st Year'),
             ('2', '2nd Year'),
             ('3', '3rd Year'),
             ('4', '4th Year'), ]

    semesters = models.CharField(max_length=1, choices=SEMESTERS, blank=True)
    years = models.CharField(max_length=1, choices=YEARS, blank=True)

    def __str__(self):
        return (self.get_semesters_display() or self.get_years_display())

class Category(models.Model):
    faculty = models.CharField(max_length=50, blank=True)

    SEASONS = [('Y', "Year"),
               ('S', "Semester")]

    seasons = models.CharField(max_length=1, choices=SEASONS, blank=True)

    def __str__(self):
        return f'{self.faculty} '

class Question(models.Model):
    slug = models.SlugField(max_length=20, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    title = models.TextField(blank=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvotes')
    downvotes = models.ManyToManyField(User, blank=True, related_name='downvotes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  blank=True, null=True)
    created = models.DateField(auto_now_add=True, )
    updated = models.DateField(auto_now=True)



    def save(self, *args, **kwargs):
        while True and self.slug=='':
            slug = randomString()
            existed_slug = [post.slug for post in Question.objects.all()]
            if (slug in existed_slug):
                pass
            else:
                self.slug = slug
                break
        super(Question, self).save(*args, **kwargs, )


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name='a_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    upvotes = models.ManyToManyField(User, blank=True, related_name='a_upvotes')
    downvotes = models.ManyToManyField(User, blank=True, related_name='a_downvotes')
    created = models.DateField(auto_now_add=True, )
    updated = models.DateField(auto_now=True)

def get_image_filename(instance, filename):
    id = instance.question.id
    return 'post_pics/%s' % (id)

class Image(models.Model):
    #id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null = True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null = True, blank=True)
    image = models.ImageField(upload_to=get_image_filename, null = True, blank=True)



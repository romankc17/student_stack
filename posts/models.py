import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from faculty.models import Category,Batch,Subject

def randomString(stringLength=3):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



class Question(models.Model):
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='question_user')
    title = models.CharField(max_length=500)
    upvotes = models.ManyToManyField(User, blank=True, related_name='question_upvotes')
    downvotes = models.ManyToManyField(User, blank=True, related_name='question_downvotes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True )
    updated = models.DateField(auto_now=True, blank=True, null=True)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        while True and self.slug=='':
            slug=slugify(self.title)
            # slug = randomString()
            existed_slug = [post.slug for post in Question.objects.all()]
            if (slug in existed_slug):
                slug += '-' + randomString()
            else:
                self.slug = slug
                break
        super(Question, self).save(*args, **kwargs, )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', kwargs = {'slug':self.slug})


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.TextField()
    upvotes = models.ManyToManyField(User, blank=True, related_name='answer_upvotes')
    downvotes = models.ManyToManyField(User, blank=True, related_name='answer_downvotes')
    created = models.DateField(auto_now_add=True, )
    updated = models.DateField(auto_now=True)

def get_image_filename(instance, filename):
    try:
        id = instance.question.id
    except:
        id = instance.answer.id
    return 'post_pics/%s' % (id)

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null = True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null = True, blank=True)
    image = models.ImageField(upload_to=get_image_filename, null = True, blank=True)



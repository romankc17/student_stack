from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    #id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question_title = models.TextField(blank=True)
    #question_image = models.ImageField(upload_to='question_pics', blank=True, null=True)
    question_upvote = models.IntegerField(null = True, default=0)
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
    question_sem = models.CharField(max_length=1, choices=SEMESTER, verbose_name='Semester' )
    date_published = models.DateField(auto_now=True, )


class Answer(models.Model):
    #id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_title = models.CharField(max_length=200)
    date_published = models.DateField(auto_now=True,)

def get_image_filename(instance, filename):
    id = instance.question.id
    return 'post_pics/%s' % (id)

class Image(models.Model):
    #id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null = True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null = True)
    image = models.ImageField(upload_to=get_image_filename, null = True, blank=True)

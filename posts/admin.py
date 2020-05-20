from django.contrib import admin
from .models import Question,Answer,Image

admin.site.register([Image,])

class AnswerInline(admin.StackedInline):
    model = Answer
    fields = ('title','user', 'upvotes','downvotes')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user')
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory, inlineformset_factory, BaseFormSet
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy

from faculty.models import Category
from .forms import QuestionCreateForm,ImageForm

from .models import Question, Image
from posts.models import Answer
from posts.forms import AnswerForm

def question_view(request, question_sem):
    try:
        objects = Question.objects.filter(semester=question_sem)
    except:
        raise Http404
    return render(request, 'posts/questions_list.html', {'objects':objects})

def home_page(request):
    context={
        'questions':Question.objects.all().order_by('-created'),
        'categories':Category.objects.all()
    }
    return render(request, 'index.html', context)


def question_create_view(request):
    ImageFormSet = modelformset_factory(Image,
                                        fields=('image',),
                                        extra=1)
    if request.method == 'POST':
        qform = QuestionCreateForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,)
        if qform.is_valid() and formset.is_valid():
            qform = qform.save(commit=False)
            qform.user = request.user
            qform.save()
            for form in formset.cleaned_data:
                try:
                    image = form['image']

                    photo = Image(question = qform, image=image)
                    photo.save()
                except:
                    pass
            messages.success(request,  "Your Question has been Posted!")
            return HttpResponseRedirect("/")
        else:
            messages.warning(request,"Sorry Something Went Wrong!")
    else:
        qform = QuestionCreateForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    context = {'qform': qform, 'formset': formset}
    return render(request, 'posts/question_create.html',context)



# Question Update View






def question_answers(request, slug):

    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm,
                                        extra=3)
    question = Question.objects.get(slug = slug)

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        formset = ImageFormSet(request.POST,
                               request.FILES,
                               queryset = Image.objects.none())
        if answer_form.is_valid() and formset.is_valid():
            answer_form = answer_form.save(commit=False)
            answer_form.user = request.user
            answer_form.question = question
            answer_form.save()

            for form in formset.cleaned_data:
                try:
                    image = form['image']
                    photo = Image(answer=answer_form, image=image)
                    photo.save()
                except :
                    pass


            messages.success(request, "Answer Posted!")

            return HttpResponseRedirect(reverse('question_detail', kwargs={'slug':question.slug}))


    answer_form = AnswerForm()
    formset = ImageFormSet(queryset=Image.objects.none())

    context = {
        'question':question,
        'answer_form': answer_form,
        'formset': formset,
    }

    return render(request, 'posts/question_detail.html', context)


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer



    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'slug': self.object.question.slug})


def question_update_view(request, slug):
    ImageFormSet = modelformset_factory(Image,
                                        fields=('image',),
                                        max_num=1)
    question = get_object_or_404(Question, slug=slug)
    if question.user != request.user:
        raise Http404()
    if request.method == 'POST':
        qform = QuestionCreateForm(request.POST, instance=question)
        formset = ImageFormSet(request.POST or None,
                               request.FILES or None, )
        if qform.is_valid() and formset.is_valid():
            qform.save()
            data = Image.objects.filter(question=question)
            for index, form in enumerate(formset):
                if form.cleaned_data:

                    print(formset.cleaned_data)

                    #to add new image
                    if form.cleaned_data['id'] is None:
                        image = form.cleaned_data.get('image')
                        photo = Image(question=question, image=image)
                        photo.save()

                    #to delete image
                    elif form.cleaned_data['image'] is False:
                        photo = Image.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete(save=False)

                    # to update existing image
                    else:
                        image = form.cleaned_data.get('image')
                        photo = Image(question=question, image=image)
                        d = Image.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()
            messages.success(request, "Your Question has been Updated!")
            return redirect(question)
        else:
            messages.warning(request, "Sorry Something Went Wrong!")

    else:
        qform = QuestionCreateForm(instance=question)
        formset = ImageFormSet(queryset=Image.objects.filter(question=question))
    context = {'qform': qform,
               'formset': formset,
               'question': question
               }
    return render(request, 'posts/question_create.html', context)



def answer_update(request, pk):
    ImageFormSet = modelformset_factory(Image,
                                        fields=('image',),
                                        max_num=3)
    answer = Answer.objects.get(id=pk)
    question = answer.question

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST, instance=answer)
        formset = ImageFormSet(request.POST or None,
                               request.FILES or None,
                               )
        if answer_form.is_valid() and formset.is_valid():
            answer_form.save()
            data = Image.objects.filter(answer=answer)
            for index,form in enumerate(formset):
                if form.cleaned_data:
                    if form.cleaned_data['id'] is None:
                        photo = Image(answer=answer, image=form.cleaned_data.get('image'))
                        photo.save()

                    # to delete image
                    elif form.cleaned_data['image'] is False:
                        photo = Image.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()

                    # to update existing image
                    else:
                        image = form.cleaned_data.get('image')
                        photo = Image(answer=answer, image=image)
                        d = Image.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()

            messages.success(request, "Your Answer has been Update!")

            return redirect(question)
        else:
            messages.error(request, formset.errors)
    else:
        answer_form = AnswerForm(instance=answer)
        formset = ImageFormSet(queryset=Image.objects.filter(answer=answer))
    context = {'answer_form': answer_form,
           'formset': formset,
           'question': question,
           }
    return render(request, 'posts/answer_update.html', context)

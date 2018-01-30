from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from . import models, forms

def course_list(request):
    courses = models.Course.objects.all()
    email = 'questsions@learning_site.com'
    return render(request, 'courses/course_list.html', {'courses': courses,
                                                        'email': email})


def course_detail(request, pk):
    course = get_object_or_404(models.Course, pk=pk)
    steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),
                   key=lambda step: step.order)
    return render(request, 'courses/course_detail.html',
                  {'course': course,
                   'steps': steps})


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/text_detail.html', {'step': step})


def quiz_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Quiz, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/quiz_detail.html', {'step': step})

@login_required
def text_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.TextForm()

    if request.method == 'POST':
        form = forms.TextForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            text.course = course
            text.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Text post added!')
            return HttpResponseRedirect(text.get_absolute_url())
    return render(request, 'courses/text_form.html', {'form': form, 'course': course})

@login_required
def text_edit(request, course_pk, text_pk):
    text = get_object_or_404(models.Text, pk=text_pk, course_id=course_pk)
    form = forms.TextForm(instance=text)

    if request.method == 'POST':
        form = forms.TextForm(instance=text, data=request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            form.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(text.get_absolute_url())
    return render(request, 'courses/text_form.html', {'form': form, 'course': text.course})

@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.QuizForm()

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Quiz added!')
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': course})


@login_required
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course_id=course_pk)
    form = forms.QuizForm(instance=quiz)

    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            form.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': quiz.course})


@login_required
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)
    if question_type == 'tf':
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm

    form = form_class()

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            question = form.save()
            question.quiz = quiz
            question.save()
            messages.success(request, 'Added question!')
            return HttpResponseRedirect(quiz.get_absolute_url)
    return render(request, 'courses/question_form.html', {
        'quiz': quiz,
        'form': form,
        'question_type': question_type
    })
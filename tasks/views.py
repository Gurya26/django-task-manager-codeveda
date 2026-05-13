from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task


@login_required
def home(request):

    if request.method == 'POST':

        title = request.POST.get('title')

        if title:
            Task.objects.create(
                user=request.user,
                title=title
            )

        return redirect('home')

    tasks = Task.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'tasks/home.html',
        {
            'tasks': tasks
        }
    )


@login_required
def complete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect('home')


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect('home')


@login_required
def edit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title')

        if title:
            task.title = title
            task.save()

        return redirect('home')

    return render(
        request,
        'tasks/edit.html',
        {
            'task': task
        }
    )


def signup(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(
        request,
        'registration/signup.html',
        {
            'form': form
        }
    )
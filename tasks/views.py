from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task


@login_required
def home(request):

    search = request.GET.get('search')

    if request.method == 'POST':

        title = request.POST.get('title')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        if title:

            Task.objects.create(
                user=request.user,
                title=title,
                priority=priority,
                due_date=due_date
            )

        return redirect('home')

    tasks = Task.objects.filter(user=request.user)

    if search:
        tasks = tasks.filter(title__icontains=search)

    tasks = tasks.order_by('-created_at')

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

        task.title = request.POST.get('title')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date')

        task.save()

        return redirect('home')

    return render(
        request,
        'tasks/edit.html',
        {
            'task': task
        }
    )


def signup_view(request):

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
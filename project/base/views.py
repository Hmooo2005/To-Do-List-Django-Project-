from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    count = Task.objects.filter(user=request.user, complete=False).count()

    search = request.GET.get('search-area') or ''
    if search:
        search_result = tasks.filter(title__icontains=search)
        return render(request, 'base/task-list.html', {'tasks': search_result, 'search': search})

    return render(request, 'base/task-list.html', {'tasks': tasks, "count": count})


@login_required
def task_create(request):
    if request.method == 'POST':
        task = Task(
            user = request.user,
            title=request.POST['title-name'],
            description=request.POST['description'])
        task.save()


    return render(request, 'base/task-create.html')

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST['title-name']
        task.description = request.POST['description']
        if request.POST.get('complete') != 'on':
            task.complete = False
        else:
            task.complete = True
        task.save()
        return redirect('/')

    return render(request, 'base/task-update.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')

    return render(request, 'base/task-delete.html', {"task": task})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'base/login.html', {"form": form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("login_user")


def register_user(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = UserCreationForm()

    return render(request, 'base/register.html', {"form": form})

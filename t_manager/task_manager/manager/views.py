from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.core.paginator import Paginator
from .forms import *
from django.contrib import messages


def search(request):
    query = request.GET.get('search')
    if query:
        tasks = Task.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        messages.error(request, 'Поиск не дал результатов')
        tasks = Task.objects.all()
    return render(request, 'manager/index.html', {'task': tasks})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'manager/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'manager/register.html', context)


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.status is True:
        task.delete()
        # task.save()
    else:
        messages.error(request, 'Задание НЕ выполнено. Его пока нельзя удалить.')
    return redirect('home')


def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.status is not True:
        task.status = True
        task.save()
    else:
        messages.error(request, 'Задание уже выполнено.')
    return redirect('task_view', task_slug=task.slug)


def add_fav(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_fav = not task.is_fav
    task.save()
    return redirect('home')


class MainView(ListView):
    model = Task
    template_name = 'manager/index.html'
    context_object_name = 'task'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Задачи'
        return context

    def get_queryset(self):
        return Task.objects.filter(status=False)


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'manager/add_task.html'
    # success_url = reverse_lazy('home')
    login_url = 'home'


class TaskView(DetailView):
    model = Task
    template_name = 'manager/task_view.html'
    context_object_name = 'tasks_item'
    slug_url_kwarg = 'task_slug'


class FavTaskView(ListView):
    model = Task
    template_name = 'manager/index.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Задачи'
        return context

    def get_queryset(self):
        return Task.objects.filter(is_fav=True).order_by('status')


# class SearchFormView(FormView):
#     template_name = 'manager/index.html'
#     form_class = SearchForm
#     context_object_name = 'task'
#
#     def form_valid(self, form):
#         query = form.cleaned_data['query']
#         result = Task.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
#         context = self.get_context_data(form=form, result=result)
#         return self.render_to_response(context)

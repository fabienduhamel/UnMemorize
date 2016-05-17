from __future__ import unicode_literals

from django.views.generic.list import ListView
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from todolist.models import Task, TaskForm, TaskManager, Category, CategoryForm, LoginForm
import json

class HomeListView(ListView):
	context_object_name = "tasks"
	template_name = "todolist/tasks_list.html"
	
	def __init__(self, show_completed_tasks):
		super(HomeListView, self).__init__()
		self.show_completed_tasks = show_completed_tasks

	def get_current_category(self):
		if 'category_id' in self.kwargs:
			category = Category.objects.get(pk=self.kwargs['category_id'])
		else:
			category = Category.objects.get_first()
		return category

	def get_queryset(self, **kwargs):
		return Task.objects.get_tasks(self.get_current_category, False)

	def get_context_data(self, **kwargs):
		context = super(HomeListView, self).get_context_data(**kwargs)
		context['new_task_form'] = TaskForm
		context['current_category'] = self.get_current_category
		context['category_list'] = Category.objects.all()
		if self.show_completed_tasks:
			context['complete_tasks'] = Task.objects.get_tasks(self.get_current_category, True)
		return context


class Home(HomeListView):
	def __init__(self):
		super(Home, self).__init__(False)


class AllTasks(HomeListView):
	def __init__(self):
		super(AllTasks, self).__init__(True)


@login_required
def save_task(request):
	form = TaskForm(request.POST)
	if form.is_valid():
		task = form.save()
		if request.is_ajax():
			html = render(request, 'todolist/task/display_task.html', {'task': task})
			response_data = {
				"html": html.content.decode('utf-8'),
				"place": Task.objects.get_rank_in_list(task)
			}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return redirect(request.META.get('HTTP_REFERER', 'index'))
	else:
		raise Http404


@login_required
def update_task(request, task_id):
	try:
		task_to_update = Task.objects.get(pk=task_id)
		old_place = Task.objects.get_rank_in_list(task_to_update) + 1
		form = TaskForm(request.POST, instance = task_to_update)
		if form.is_valid():
			form.save()
		else:
			raise Http404
		if request.is_ajax():
			html = render(request, 'todolist/task/display_task.html', {'task': task_to_update})
			response_data = {
				"html": html.content.decode('utf-8'),
				"place": Task.objects.get_rank_in_list(task_to_update),
				"old_place": old_place
			}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return redirect(request.META.get('HTTP_REFERER', 'index'))
	except ObjectDoesNotExist:
		raise Http404


@login_required
def uncomplete_task(request, task_id):
	try:
		task_to_complete = Task.objects.get(pk=task_id)
		task_to_complete.complete = False
		task_to_complete.completed_at = timezone.now()
		task_to_complete.save()
		return redirect(request.META.get('HTTP_REFERER', 'index'))
	except ObjectDoesNotExist:
		raise Http404


@login_required
def complete_task(request, task_id):
	try:
		task_to_complete = Task.objects.get(pk=task_id)
		if task_to_complete.complete:
			raise Http404
		task_to_complete.complete = True
		task_to_complete.completed_at = timezone.now()
		task_to_complete.save()
		if request.is_ajax():
			response_data = {
				"completed": True
			}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return redirect(request.META.get('HTTP_REFERER', 'index'))
	except ObjectDoesNotExist:
		raise Http404


@login_required
def delete_task(request, task_id):
	try:
		task_to_delete = Task.objects.get(pk=task_id)
		task_to_delete.delete()
		return redirect(request.META.get('HTTP_REFERER', 'index'))
	except ObjectDoesNotExist:
		raise Http404


@login_required
def add_category(request):
	context = {'new_category_form': CategoryForm}
	return render(request, 'todolist/category/add_category.html', context)


@login_required
def save_category(request):
	form = CategoryForm(request.POST)
	if form.is_valid:
		category = form.save()
		if request.is_ajax():
			context = {'category': category}
			html = render(request, 'todolist/category/display_category.html', context)
			response_data = {
				"html": html.content.decode('utf-8')
			}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return redirect('index')
	else:
		raise Http404


@login_required
def modify_category(request, category_id):
	category = Category.objects.get(pk=category_id)
	context = {'category': category}
	return render(request, 'todolist/category/modify_category.html', context)


@login_required
def update_category(request):
	try:
		category_id = request.POST.get('id')
		category = Category.objects.get(pk=category_id)
		form = CategoryForm(request.POST, instance = category)
		if form.is_valid():
			form.save()
		else:
			context = {'category_form': form, 'category': category}
			if request.is_ajax():
				html = render(request, 'todolist/category/modify_category.html', context)
				response_data = {
					"html": html.content.decode('utf-8')
				}
				return HttpResponse(json.dumps(response_data), content_type="application/json")
			return render(request, 'todolist/category/modify_category.html', context)
		if request.is_ajax():
			response_data = {
				"new_name": category.name
			}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return redirect(request.META.get('HTTP_REFERER', 'index'))
	except ObjectDoesNotExist:
		raise Http404


@login_required
def delete_category(request):
	context = {'category_list': Category.objects.all()}
	return render(request, 'todolist/category/delete_category.html', context)


@login_required
def remove_category(request):
	form = CategoryForm(request.POST)
	if form.is_valid:
		category_id = request.POST.get('category_id')
		category = Category.objects.get(pk=category_id)
		tasks_to_delete = Task.objects.all().filter(category_id=category_id)
		for task in tasks_to_delete:
			task.delete
		category.delete()
		if request.is_ajax():
			response_data = {
				"category_id": category_id
			}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return redirect('index')
	else:
		raise Http404


def display_login(request):
	if request.user.is_authenticated():
		return redirect(request.META.get('HTTP_REFERER', 'index'))
	context = {'login_form': LoginForm(request.POST)}
	return render(request, 'todolist/login.html', context)


def do_authentication(request):
	form = LoginForm(request.POST)
	if form.is_valid:
		username = 'user'
		password = request.POST['password']
		user = User.objects.filter(username=username)[:1]
		if user.count() == 0:
			user = User.objects.create_user(username, '', password)
		user = authenticate(username=username, password=password)
		if user is None:
			return display_login(request)
		else:
			if user.is_active:
				login(request, user)
				return redirect('index')
			else:
				return display_login(request)


@login_required
def do_logout(request):
    logout(request)
    return redirect('display_login')


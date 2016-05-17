from django.contrib.auth.models import User
from django.db.models import Count
from django.db import models
from django.forms import ModelForm
from todolist.better_models import BetterModel
from todolist.custom_fields import HexadecimalColorField


class HexadecimalColor(BetterModel):
	value = HexadecimalColorField(unique=True)
	
	def __unicode__(self):
		return self.value


class Priority(BetterModel):
	value = models.IntegerField(unique=True)
	color = models.ForeignKey(HexadecimalColor)
	
	def __unicode__(self):
		if self.value > 0:
			return "+" + str(self.value)
		return self.value


class CategoryManager(models.Manager):
	def get_first(self):
		first_category = super(CategoryManager, self).get_query_set().all()[0]
		if not first_category:
			first_category = None
		return first_category


class Category(BetterModel):
	objects = CategoryManager()
	name = models.CharField(unique=True, max_length=30)
	
	def __unicode__(self):
		return self.name


class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ['name']


class TaskManager(models.Manager):
	def get_tasks(self, category_id, completed_tasks):
		return super(TaskManager, self).get_query_set()\
			.select_related()\
			.filter(complete=completed_tasks, category=category_id)\
			.extra(select={'has_due_date': 'due_date IS NOT NULL'})\
			.order_by('-priority__value', '-has_due_date', 'due_date')

	def get_rank_in_list(self, task):
		task_list = self.get_tasks(task.category_id, False)
		current_rank = 1
		for current_task in task_list:
			if current_task == task:
				return current_rank
			current_rank = current_rank + 1
		return 1


class Task(BetterModel):
	objects = TaskManager()
	description = models.CharField(max_length=300)
	note = models.TextField(max_length=2000, null=True, blank=True)
	due_date = models.DateField(null=True, blank=True)
	complete = models.BooleanField(default=False)
	completed_at = models.DateTimeField(null=True, blank=True)
	priority = models.ForeignKey(Priority)
	category = models.ForeignKey(Category)
	
	def __unicode__(self):
		return self.description


class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['description', 'priority', 'category', 'due_date']

	def __init__(self, *args, **kwargs):
		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['priority'].empty_label = None


class LoginForm(ModelForm):
	class Meta:
		model = User


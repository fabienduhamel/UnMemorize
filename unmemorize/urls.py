from django.conf.urls import patterns, url
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from todolist.views import Home, AllTasks

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^(?P<category_id>\d+)/', login_required(Home.as_view()), name='index'),
	url(r'^$', login_required(Home.as_view()), name='index'),
	url(r'^accounts/login/', 'todolist.views.display_login', name='display_login'),
	url(r'^authenticate/', 'todolist.views.do_authentication', name='do_authentication'),
	url(r'^logout/', 'todolist.views.do_logout', name='do_logout'),
	url(r'^all/(?P<category_id>\d+)/$', login_required(AllTasks.as_view()), name='all_tasks'),
	url(r'^all/$', login_required(AllTasks.as_view()), name='all_tasks'),
	url(r'^delete/(?P<task_id>\d+)/', 'todolist.views.delete_task', name='delete_task'),
	url(r'^uncomplete/(?P<task_id>\d+)/', 'todolist.views.uncomplete_task', name='uncomplete_task'),
	url(r'^complete/(?P<task_id>\d+)/', 'todolist.views.complete_task', name='complete_task'),
	url(r'^save_task/', 'todolist.views.save_task', name='save_task'),
	url(r'^update_task/(?P<task_id>\d+)/', 'todolist.views.update_task', name='update_task'),
	url(r'^add_category/', 'todolist.views.add_category', name='add_category'),
	url(r'^save_category/', 'todolist.views.save_category', name='save_category'),
	url(r'^modify_category/(?P<category_id>\d+)/', 'todolist.views.modify_category', name='modify_category'),
	url(r'^update_category/', 'todolist.views.update_category', name='update_category'),
	url(r'^delete_category/', 'todolist.views.delete_category', name='delete_category'),
	url(r'^remove_category/', 'todolist.views.remove_category', name='remove_category'),
	(r'^change_password/$', 'django.contrib.auth.views.password_change'),
	url(r'^password/change/done/$',
                    views.password_change_done,
                    name='password_change_done'),
	(r'^password_change_done/$', 'django.contrib.auth.views.password_change_done'),
	# url(r'^unmemorize/', include('unmemorize.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),
)

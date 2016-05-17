from django import template
from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat

register = template.Library()


@register.filter
def is_before_today(date):
	current_date = DateFormat(datetime.now()).format('Y/m/d')
	arg_date = DateFormat(date).format('Y/m/d')
	return current_date > arg_date


@register.filter
def is_in_current_year(date):
	current_year = DateFormat(datetime.now()).format('Y')
	date_year = DateFormat(date).format('Y')
	return current_year == date_year


@register.filter
def comes_in_days(date, day_count):
	current_date = DateFormat(datetime.now()).format('Y/m/d')
	current_date_with_day_counts = DateFormat(datetime.now() + timedelta(days=day_count)).format('Y/m/d')
	arg_date = DateFormat(date).format('Y/m/d')
	return arg_date <= current_date_with_day_counts and arg_date >= current_date


@register.filter
def is_yesterday(date):
	yesterday_date = DateFormat(datetime.now() + timedelta(days=-1)).format('Y/m/d')
	arg_date = DateFormat(date).format('Y/m/d')
	return yesterday_date == arg_date


from django.db.models.fields import CharField
from django.db import models
import re

class HexadecimalColorField(CharField):
	def __init__(self, *args, **kwargs):
		super(HexadecimalColorField, self).__init__(max_length=6, *args, **kwargs)

	def clean(self, value):
		try:
			return re.match("^[A-Fa-f0-9]{6}$", value)
		except:
			raise ValidationError

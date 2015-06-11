from django.db import models


class Contact(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()
	message = models.TextField()

	def __unicode__(self):
		return str(self.email)

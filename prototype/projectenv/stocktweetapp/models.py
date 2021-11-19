from django.db import models

class Stock(models.Model):
	image = models.ImageField(upload_to = 'images/')
	summary = models.CharField(max_length = 100)


	def __str__(self):  #current instance of the class
		return self.summary

# Create your models here.

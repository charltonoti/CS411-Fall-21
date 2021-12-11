from django.db import models
import datetime
from django.utils import timezone


class Stock(models.Model):
	image = models.ImageField(upload_to = 'images/')
	summary = models.CharField(max_length = 100)

	def __str__(self):  #current instance of the class
		return self.summary

class Recommendations(models.Model):
    
    daily_recommemdation = models.CharField(max_length=5000)
    pub_date = models.CharField(max_length=100)
    
    def __str__(self):
        return self.daily_recommemdation
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



# Create your models here.

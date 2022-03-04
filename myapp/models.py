from pickle import TRUE
from time import time
from django.db import models
from django.utils.timezone import now
# Create your models here.


class Employee(models.Model):
    Social_Network = models.CharField(max_length=255)
    Post_Id = models.CharField(max_length=1000)
    Key_word = models.CharField(max_length=255)
    Names = models.CharField(max_length=255,)
    Link_post = models.CharField(max_length=5000)
    post = models.CharField(max_length=400)
    comment = models.CharField( max_length=5000)
    device = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    Job_title = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    Note = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    
# ross = Employee.objects.get(Post_Id='1')
# ross.Post_Id = '2'
# ross.save()
# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     price = models.CharField(max_length=255)
#     content = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name


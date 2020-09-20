from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

class feedback(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=40)
    date_posted = models.DateTimeField(auto_now_add = True)
    content = models.TextField(max_length=1000)
    admin_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.author} feedback"

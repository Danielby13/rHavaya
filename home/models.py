from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.urls import reverse

# about model
class About(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = FroalaField()

    def get_absolute_url(self):
        return reverse('update_about_page')
        
    def __str__(self):
        return self.title

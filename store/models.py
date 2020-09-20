from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

type_store_choices = (
    ('collaborations','collaborations'),('sales','sales'),
)
# store model
class store(models.Model):
    title = models.CharField(max_length=100)
    type_store = models.CharField(max_length = 30,choices=type_store_choices, default='sales')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add = True)
    coupon_code = models.CharField(max_length=255, blank = True, null = True)
    link_to_store = models.CharField(max_length=1000, blank = True, null = True)
    content = models.TextField()
    image = models.ImageField(default='default.jpeg', upload_to='store_pics')
    

    def __str__(self):
        return '{0} {1}'.format(self.title,self.type_store)

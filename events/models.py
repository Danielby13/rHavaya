from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from django_google_maps import fields as map_fields
from users.views import send_email_to_all
from PIL import Image
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags


type_event_choices = (
    ('ride','ride'),('event','event'),
)

# events model for rides and events
class events(models.Model):
    title = models.CharField(max_length=100)
    type_event = models.CharField(max_length = 10,choices=type_event_choices, default='ride')
    event_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='')
    subscribed_to_event = models.TextField(blank = True, null = True ,default='')
    attended_to_event = models.IntegerField(default=0)
    address = map_fields.AddressField(max_length=200)
    google_map = models.CharField(max_length=500,default='')
 
    def __str__(self):
        return '{0} {1}'.format(self.title,self.type_event)

    # override the built-in save method - added sending email when staff member is updated/created new event 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        subject = '{} עודכן'.format(self.title) 
        html_message = render_to_string('events/email_update_users.html', {'title': self.title, 'address': self.address})
        plain_message = strip_tags(html_message)
        send_email_to_all(subject, plain_message)

    # help function to check if user can register to event
    @property
    def check_if_date_passed(self):
        return timezone.now() > self.event_date

# help model to control the amount of users that attendant to come to event
class registered_to_event(models.Model):
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='related_user')
    passengers_counter = models.IntegerField(default=1)
    
    def __str__(self):
        return '{0} registered to {1}'.format(self.user.username, self.event.title)

# gallery model
class Gallery(models.Model):
    title = models.CharField(max_length=400)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    event_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpeg', upload_to='gallery')
    link_to_google_drive = models.CharField(max_length=1500,default='')

    def __str__(self):
        return self.title
        
    #override the built-in method for space-saving pictures 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.image.path)
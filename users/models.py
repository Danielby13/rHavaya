from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField()
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    join_meet_the_rider = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)
    phone_number = models.CharField(default='',max_length=10)
    role = models.CharField(default='member',max_length=100)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.image.path)





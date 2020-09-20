from django.shortcuts import render, redirect
from .models import About
from events.models import events,Gallery
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

# the main page
def home(request):
    context = {
        'home': About.objects.filter(title="דף ראשי").first(),
        'vision': About.objects.filter(title="חזון").first(),
        'event': events.objects.order_by('-event_date')[:3],
        'gallery_imgs': Gallery.objects.all().order_by('-event_date'),
          }
    return render(request, 'home/home.html',context) 

# about us page
def AboutUs(request):
    context = {
        'about': About.objects.filter(title="אודות")
    }
    return render(request, 'home/AboutUs.html', context)

# vision page
def vision(request):
    context = {
        'about': About.objects.filter(title="חזון")
    }
    return render(request, 'home/vision.html', context)

# rules page
def rules(request):
    context = {
        'about': About.objects.filter(title="חוקי הקבוצה")
    }
    return render(request, 'home/rules.html', context)

# contact page
def contact(request):
    context = {
        'about': About.objects.filter(title="צור קשר")
    }
    return render(request, 'home/contact.html', context)

# when user is try to accses to restrict page, this page will appear
def pageNotFound(request):
    return render(request, 'home/pagenotfound.html')

# update content for about page (vision,contact...)
def update_about_page(request):
    context = {
        'about': About.objects.all()
    }
    return render(request, 'home/update_about_page.html', context)
    
# form to update the about page   
class aboutUpdate(LoginRequiredMixin, UpdateView):
    model = About
    template_name = 'home/aboutform.html'
    fields = ['content']
    def form_valid(self, form):
        return super().form_valid(form)
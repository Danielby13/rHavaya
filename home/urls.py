from django.urls import path
from . import views
from .views import aboutUpdate

urlpatterns = [
				path('aboutus/',views.AboutUs, name="aboutus-page"),
				path('vision/',views.vision, name="vision-page"),
				path('rules/',views.rules, name="rules-page"),
				path('contact/',views.contact, name="contact-page"),
				path('admin/',views.home, name="admin-db"),
				path('pagenotfound/',views.pageNotFound, name="pagenotfound"),
				path('update_about_page/',views.update_about_page, name="update_about_page"),
				path('<int:pk>/update/', aboutUpdate.as_view(), name="about_update"),
				path('',views.home, name="home-page"),
			      ]
from django.urls import path
from . import views
from django.conf.urls import include
urlpatterns = [
				path('feedback/',views.usersFeedback, name="feedback"),
				path('feedback_approval/',views.feedbackApproval, name="feedback_approval"),
			      ]
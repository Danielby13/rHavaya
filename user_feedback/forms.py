from django import forms
from user_feedback.models import feedback


class feedbackForm(forms.ModelForm):
	class Meta:
		model = feedback
		fields = ['title','author', 'content'] 


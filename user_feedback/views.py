from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import feedbackForm
from .models import feedback
from django.contrib.auth.decorators import login_required

# user feedback 
def usersFeedback(request):
	if request.method == 'POST':
		form = feedbackForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('feedback')
	else:
		if not request.user.is_authenticated:
			form = feedbackForm()
		else:
			form = feedbackForm(initial={'author':f"{request.user.first_name} {request.user.last_name}"})

		""" change buit-in fields name"""
		title = form.fields['title']
		title.label = "כותרת "

		author = form.fields['author']
		author.label = "שם "

		content = form.fields['content']
		content.label = "כתבו תגובה "	

	context = {
		'form': form, 'feedbacks': feedback.objects.filter(admin_approved='True')
	}
	return render(request, 'user_feedback/users_feedback.html',context)

# member staff need to approve the feedback 
@login_required
def feedbackApproval(request):
	if request.user.is_staff:
		if(request.POST.get('approved_feedback')):
			feedback_id = request.POST.get("id")
			feedback.objects.filter(id=feedback_id).update(admin_approved = True)
			messages.success(request, 'המשוב אושר')
			redirect("feedback_approval")

		if(request.POST.get('delete_feedback')):
			feedback_id = request.POST.get("id")
			feedback.objects.filter(id=feedback_id).delete()
			messages.success(request, 'המשוב נמחק')
			redirect("feedback_approval")
		
		context = {
			'feedbacks': feedback.objects.filter(admin_approved='False')
		}
		return render(request, 'user_feedback/feedback_approval.html', context)
	else:
		return render(request, 'home/pagenotfound.html')
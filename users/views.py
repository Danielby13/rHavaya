from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,CustomAuthenticationForm,UserUpdateForm,ProfileUpdateForm,ProfileRegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail

# register form
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		p_form = ProfileRegisterForm(request.POST)
		if form.is_valid() and p_form.is_valid():
			user = form.save()
			user.refresh_from_db()
			p_form = ProfileRegisterForm(request.POST, instance=user.profile)
			p_form.full_clean()
			p_form.save()
			firstname = form.cleaned_data.get('first_name')
			messages.success(request, f'ההרשמה בוצעה בהצלחה. ברוכים הבאים {firstname}')
			return redirect('login')
	else:
		form = UserRegisterForm()
		p_form = ProfileRegisterForm()

		""" change buit-in fields name"""
		usrnm = form.fields['username']
		usrnm.label = "שם משתמש "
		usrnm.help_text = " "

		eml = form.fields['email']
		eml.label = "כתובת אימייל "
		eml.help_text = " "

		frstnm = form.fields['first_name']
		frstnm.label = "שם פרטי "

		lstnm = form.fields['last_name']
		lstnm.label = "שם משפחה "

		pswrd1 = form.fields['password1']
		pswrd1.label = "סיסמה "
		pswrd1.help_text = "הסיסמה חייבת להכיל לפחות 8 אותיות. <br> הסיסמה חייבת לכלול אותיות ומספרים. <br> הסיסמה לא יכולה להיות דומה לשם המשתמש."

		pswrd2 = form.fields['password2']
		pswrd2.label = "אימות סיסמה "
		pswrd2.help_text = " "

		phn_nbmr= form.fields['phone_number']
		phn_nbmr.help_text ="המספר ישמש הרשמה לאירועים"

	context = {
		'form': form,
		'p_form': p_form
	}
	return render(request, 'users/register.html',context)

class CustomLoginView(LoginView):
	authentication_form = CustomAuthenticationForm

# profile page, the user can change thier personal data
@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'הפרטים עודכנו בהצלחה')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

		""" change buit-in user fields name"""
		usrnm = u_form.fields['username']
		usrnm.label = "שם משתמש "
		usrnm.help_text = " "

		eml = u_form.fields['email']
		eml.label = "כתובת אימייל "
		eml.help_text = " "

		frstnm = u_form.fields['first_name']
		frstnm.label = "שם פרטי "

		lstnm = u_form.fields['last_name']
		lstnm.label = "שם משפחה "


		phone = p_form.fields['phone_number']
		phone.label = "מספר פלאפון"
		
		join_rider = p_form.fields['join_meet_the_rider']
		join_rider.label = "---להצטרף להכר את הרוכב"


	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'users/profile.html', context)

# meet the rider page
def riders(request):
	context = {
		'riders': Profile.objects.filter(join_meet_the_rider="True", admin_approved="True").order_by('-role')
	}
	return render(request, 'users/riders.html', context)

# member satff need to approve the user before they can dispaly in the meet the rider
@login_required
def userApproval(request):
	if request.user.is_staff:
		if(request.POST.get('approved_user')):
			user_id = request.POST.get("id")
			Profile.objects.filter(id=user_id).update(admin_approved = True)
			messages.success(request, 'המשתמש אושר')
			redirect("userapproval")

		if(request.POST.get('delete_user')):
			user_id = request.POST.get("id")
			Profile.objects.filter(id=user_id).delete()
			messages.success(request, 'המשתמש נמחק')
			redirect("userapproval")
		
		context = {'users': Profile.objects.filter(join_meet_the_rider="True",admin_approved="False")}
		return render(request, 'users/user_approval.html', context)
	else:
		return render(request, 'home/pagenotfound.html')

# send email function
def send_email(subject, message, recievers):
    send_mail(
    subject,
    message,
    'rochvim.h@gmail.com',
    recievers,
    fail_silently=True,
    )

# send email to all the users in the system
def send_email_to_all(subject, message):
    recievers = []
    for user in User.objects.all():
        recievers.append(user.email)

    send_email(subject, message, recievers)
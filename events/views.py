from django.shortcuts import render, redirect
from .models import events,registered_to_event,Gallery
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.views import send_email

# display all the rides and see their details and register to the rides
def rides(request):
    if(request.POST.get('reg_ride')):
        ride_id = request.POST.get("id")
        extra_pass = request.POST.get("extra_pass")   
        # pull the specific ride to register, and check if the user is already register
        ride = events.objects.get(id = ride_id)
        if (f"{request.user}" not in ride.subscribed_to_event.split()):
            incr_att_to_come = events.objects.get(id = ride_id).attended_to_event
            # amount of riders 
            if extra_pass == 'on':
                extra_pass_input=2
                counter = incr_att_to_come + 2
            else:
                extra_pass_input=1
                counter = incr_att_to_come + 1
            # add the rider to the ride(user name) and add the rider to register chart for the specific ride
            add_rider = f"{ride.subscribed_to_event} {request.user} "
            events.objects.filter(id=ride_id).update(subscribed_to_event = add_rider)
            add_to_reg_chart = registered_to_event(event=ride, user=request.user, passengers_counter=extra_pass_input)
            add_to_reg_chart.save()
            events.objects.filter(id=ride_id).update(attended_to_event = counter)

            # sent mail to the user with the ride details
            subject = 'הרשמה לאירוע {}'.format(ride.title)
            message = 'פרטי הרשמה לאירוע: \n תאריך ושעה: {}, {} \n מיקום: {} \n\n נשמח לראותכם, דו גלגלי רוכבים חוויה'.format(ride.event_date.time(), ride.event_date.date(),ride.address)
            recievers = [request.user.email]
            
            send_email(subject, message, recievers)
            messages.success(request, 'הרשמה לטיול בוצעה בהצלחה')
        else:
            messages.error(request, 'אתם כבר רשומים לטיול')
        redirect("rides")

    # removing the rider from the ride
    if(request.POST.get('undo_reg_ride')):
        ride_id = request.POST.get("id") 

        ride = events.objects.get(id = ride_id)
        if (f"{request.user}" in ride.subscribed_to_event.split()):
            dec_att_to_come = events.objects.get(id = ride_id).attended_to_event

            undo_rider_from_ride = ride.subscribed_to_event.replace(f"{request.user}", "")
            events.objects.filter(id=ride_id).update(subscribed_to_event = undo_rider_from_ride)
            counter = registered_to_event.objects.get(user=request.user, event=ride).passengers_counter

            events.objects.filter(id=ride_id).update(attended_to_event = dec_att_to_come-counter)
            undo_reg_chart = registered_to_event.objects.filter(user=request.user, event=ride)
            undo_reg_chart.delete()

            messages.success(request, 'הוסרת מהרשימה')
        else:
            messages.error(request, 'אירעה שגיאה, אנא נסו במועד מאוחר יותר')
        redirect("rides")

    var = {'rides': events.objects.filter(type_event='ride').order_by('-event_date')}
    return render(request, 'events/rides.html',var)

# display all the events and see their details and register to the events
def event(request):
    if(request.POST.get('reg_event')):
        event_id = request.POST.get("id")
        extra_pass = request.POST.get("extra_pass")   
        # pull the specific ride to register, and check if the user is already register
        event = events.objects.get(id = event_id)
        if (f"{request.user}" not in event.subscribed_to_event.split()):
            incr_att_to_come = events.objects.get(id = event_id).attended_to_event
            # amount of riders 
            if extra_pass == 'on':
                extra_pass_input = 2
                counter = incr_att_to_come + 2
            else:
                extra_pass_input = 1
                counter = incr_att_to_come + 1
            # add the rider to the ride(user name) and add the rider to register chart for the specific ride
            add_rider = f"{event.subscribed_to_event} {request.user} "
            events.objects.filter(id=event_id).update(subscribed_to_event = add_rider)
            add_to_reg_chart = registered_to_event(event=event, user=request.user, passengers_counter=extra_pass_input)
            add_to_reg_chart.save()
            events.objects.filter(id=event_id).update(attended_to_event = counter)
            # sent mail to the user with the ride details
            subject = 'הרשמה לאירוע {}'.format(event.title)
            message = 'פרטי הרשמה לאירוע: \n תאריך ושעה: {}, {} \n מיקום: {} \n\n נשמח לראותכם, דו גלגלי רוכבים חוויה'.format(event.event_date.time(), event.event_date.date(),event.address)
            recievers = [request.user.email]
            
            send_email(subject, message, recievers)
            messages.success(request, 'הרשמה לאירוע בוצעה בהצלחה')
        else:
            messages.error(request, 'אתם כבר רשומים לאירוע')
        redirect("events")
    # removing the rider from the list 
    if(request.POST.get('undo_reg_event')):
        event_id = request.POST.get("id") 

        event = events.objects.get(id = event_id)
        if (f"{request.user}" in event.subscribed_to_event.split()):
            dec_att_to_come = events.objects.get(id = event_id).attended_to_event

            undo_rider_from_event = event.subscribed_to_event.replace(f"{request.user}", "")
            events.objects.filter(id=event_id).update(subscribed_to_event = undo_rider_from_event)
            counter = registered_to_event.objects.get(user=request.user, event=event).passengers_counter

            events.objects.filter(id=event_id).update(attended_to_event = dec_att_to_come-counter)
            undo_reg_chart = registered_to_event.objects.filter(user=request.user, event=event)
            undo_reg_chart.delete()

            messages.success(request, 'הוסרת מהרשימה')
        else:
            messages.error(request, 'אירעה שגיאה, אנא נסו במועד מאוחר יותר')
        redirect("events")

    var = {'event': events.objects.filter(type_event='event').order_by('-event_date')}
    return render(request, 'events/event.html',var)

# display of the gallery
def gallery(request):
    var = {'images': Gallery.objects.all().order_by('-event_date')}
    return render(request, 'events/gallery.html', var)

# only staff member can view this page, this is for controling the attendant to come to the event   
@login_required
def registered_to_event_chart(request):
    if request.user.is_staff:
        var = {'reg_to_events': registered_to_event.objects.filter(event__type_event__contains="event").annotate(Count('id')).order_by("-event").filter(id__count__gt=0) }
        return render(request, 'events/registered_to_event.html',var)
    return render(request, 'home/pagenotfound.html')

# only staff member can view this page, this is for controling the attendant to come to the event  
@login_required
def registered_to_ride_chart(request):
    if request.user.is_staff:
        var = {'reg_to_events': registered_to_event.objects.filter(event__type_event__contains="ride").annotate(Count('id')).order_by("-event").filter(id__count__gt=0) }
        return render(request, 'events/registered_to_event.html',var)
    return render(request, 'home/pagenotfound.html')

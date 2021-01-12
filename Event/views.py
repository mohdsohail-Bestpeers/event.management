from django.shortcuts import render
from .models import EventUser, Event, Address, event_photo
from .forms import event_user_form, event_form, address_form, event_photo_form
from django.http import HttpResponseRedirect
#from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
'''smtp modules'''
from django.conf import settings 
from django.core.mail import send_mail 


'''Mobile number validation'''  
# def user(request):
#     form = user_form()
#     if request.method == "POST":
#         form = user_form(request.POST)
#         if form.is_valid():
#             form.save()
#     return render(request, "user.html", {"form": form})

'''This function shows event accourding to Publishers'''
def public_view(request, x):
        objs = Event.objects.filter(publisher__first_name=x, user_event_request="accepted",)
        if request.method == 'POST':
            form1 = event_user_form(request.POST)
            form2 = event_form(request.POST)
            form3 = address_form(request.POST)
            form4 = event_photo_form(request.POST, request.FILES)
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                #form1
                event_user_obj = form1.save()
                #form2
                form2.save(commit=False)
                form2.instance.event_user = event_user_obj
                event_obj = form2.save()
                #form3
                form3.save(commit=False)
                form3.instance.event = event_obj
                form3.save()
                #form4
                form4.save(commit=False)
                form4.instance.event = event_obj
                form4.save()

                '''smtp'''
                subject = 'welcome to the Event Management Indore'
                message = 'Hi {} {}, thank you for registering your event.'.format(event_user_obj.fname,event_user_obj.lname)
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [event_user_obj.email, ] 
                send_mail( subject, message, email_from, recipient_list ) 

                return HttpResponseRedirect('/payment/')
        
        else:
            form1 = event_user_form()
            form2 = event_form()
            form3 = address_form()
            form4 = event_photo_form()
        return render(request, 'public_result.html', {'objs':objs, 'form1':form1, 'form2':form2, 'form3':form3, 'form4':form4, 'x':x})
   

'''This is user login function'''
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user != None:
                    login(request, user)
                    return HttpResponseRedirect('/event/')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    else:
        return HttpResponseRedirect('/event/')

'''This is user logout function'''
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

'''this is payment fucntion which show the payment is done after click on the payment button'''
def payment(request):
    if request.method == 'POST':
        objs = Event.objects.filter(payment_status='pending').order_by('-id')[:1]
        for obj in objs:
            obj.payment_status = 'done'
            obj.save()
        return HttpResponseRedirect("/")
    return render(request, 'payment.html')
    


def find_data(request):
    if request.method == "POST":
        srch = request.POST.get("srch")
        srch2 = request.POST.get("srch2")
        if request.user.is_authenticated:
            objs = Event.objects.filter(publisher__first_name=request.user.first_name, service__icontains=srch,event_address__city__icontains=srch2)
            html = render_to_string('post.html', context={'objs':objs})
        else:
            srchformid = request.POST.get('searchform_id')
            objs = Event.objects.filter(publisher__first_name=srchformid, user_event_request='accepted', service__icontains=srch,event_address__city__icontains=srch2)
            html = render_to_string('public_post.html', context={'objs':objs})
        return JsonResponse({'status':200, 'html':html})
        
    else:
        return JsonResponse({'status':400})


def home(request):
    objs = Event.objects.all() #filter(user_event_request=request.user)
    if request.method == 'POST':
        form1 = event_user_form(request.POST)
        form2 = event_form(request.POST)
        form3 = address_form(request.POST)
        form4 = event_photo_form(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            #form1
            event_user_obj = form1.save()
            #form2
            form2.save(commit=False)
            form2.instance.event_user = event_user_obj
            event_obj = form2.save()
            #form3
            form3.save(commit=False)
            form3.instance.event = event_obj
            form3.save()
            #form4
            form4.save(commit=False)
            form4.instance.event = event_obj
            form4.save()
            '''smtp'''
            subject = 'welcome to the Event Management Indore'
            message = 'Hi {} {}, thank you for registering your event.'.format(event_user_obj.fname,event_user_obj.lname)
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [event_user_obj.email, ] 
            send_mail( subject, message, email_from, recipient_list ) 
            return HttpResponseRedirect('/payment/')
    else:
        form1 = event_user_form()
        form2 = event_form()
        form3 = address_form()
        form4 = event_photo_form()
    return render(request, 'home.html', {'objs':objs, 'form1':form1, 'form2':form2, 'form3':form3, 'form4':form4})

    #return render(request,'home.html')


def publisher_view(request):
    if request.user.is_authenticated:
        objs = Event.objects.filter(publisher__first_name=request.user.first_name)
        if request.method == 'POST':
            form1 = event_user_form(request.POST)
            form2 = event_form(request.POST)
            form3 = address_form(request.POST)
            form4 = event_photo_form(request.POST, request.FILES)
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                #form1
                event_user_obj = form1.save()
                #form2
                form2.save(commit=False)
                form2.instance.event_user = event_user_obj
                event_obj = form2.save()
                #form3
                form3.save(commit=False)
                form3.instance.event = event_obj
                form3.save()
                #form4
                form4.save(commit=False)
                form4.instance.event = event_obj
                form4.save()
                '''this loop is for status done '''
                for obj in objs:
                    obj.payment_status = 'done'
                    obj.save()
                
                return HttpResponseRedirect('/event/')
        
        else:
            form1 = event_user_form()
            form2 = event_form()
            form3 = address_form()
            form4 = event_photo_form()
        return render(request, 'result.html', {'objs':objs, 'form1':form1, 'form2':form2, 'form3':form3, 'form4':form4})
    else:
        return HttpResponseRedirect('/login/')
  


def publisher_approval(request):
    if request.method == 'GET':
        approval = request.GET.get('approval')
        obj_id = int(request.GET.get('obj_id'))
        event = Event.objects.get(id=obj_id)
        event.user_event_request = approval
        event.save()
        objs = Event.objects.filter(publisher=event.publisher)
        html = render_to_string('post.html', context={'objs':objs})
        return JsonResponse({'status':200, 'html':html})


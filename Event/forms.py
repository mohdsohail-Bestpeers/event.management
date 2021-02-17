from django import forms
from .models import User, Event, Address, event_photo, UserType

# from functools import partial
# DateInput = partial(forms.DateInput, {'class': 'datepicker'})


'''access all Event user field into form'''
class user_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
      
    # '''Mobile number validation'''  
    # def clean_mobile(self):
    #     mobile_passed = str(self.cleaned_data.get("mobile"))
    #     if len(mobile_passed) != 10:
    #         raise forms.ValidationError("Not a vailid number..! Please enter again")
    #     return mobile_passed


class usertype_form(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ['Mobile_no']


'''access some Event field into form'''
class event_form(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'start_date': forms.DateInput(attrs={'class':'datepicker'}),
            'end_date': forms.DateInput(attrs={'class':'datepicker'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Describe Your Needs !'}),
        }
        
        exclude = ['event_user','payment_status','user_event_request', 'user', 'publisher']

        #in the exculde there is some fields mentioned will not visible in form  

'''access some address field into form'''
class address_form(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["event"]
        #exclude hide the event field from form

'''access event photo field into form '''
class event_photo_form(forms.ModelForm):
    class Meta:
        model = event_photo
        exclude = ["event"]
        widgets = {
            'photo': forms.FileInput()
        }
        #exclude hide the event field from the form
        
        

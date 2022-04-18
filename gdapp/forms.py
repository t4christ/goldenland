from django import forms
from .models import Realtor,GENDER, RealtorDownline
import datetime 


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput())




class RealtorForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name",required=True, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(label="Last Name",required=True, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    mobile = forms.IntegerField(label="Mobile",required=False, widget=forms.TextInput(attrs={'placeholder':'Mobile'}))
    address = forms.CharField(label="Address",required=False, widget=forms.TextInput(attrs={'placeholder':'Address'}))
    state_of_origin = forms.CharField(label="State Of Origin",required=False, widget=forms.TextInput(attrs={'placeholder':'State Of Origin'}))
    date_of_birth = forms.DateField(label='What is your birth date?', widget=forms.TextInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER,required=True)
    account_number = forms.CharField(label="Account Number",required=False, widget=forms.TextInput(attrs={'placeholder':'Account Number'}))
    account_merchant = forms.CharField(label="Account Merchant",required=False, widget=forms.TextInput(attrs={'placeholder':'Account Merchant'}))
   
    class Meta:
        model = Realtor
        fields = ('first_name','last_name','mobile','gender','address','state_of_origin','account_merchant','account_number','date_of_birth')



    def clean_mobile(self):
        # Check that the two password entries match
        mobile = self.cleaned_data.get("mobile")

        if len(str(mobile)) < 10:
            raise forms.ValidationError("Mobile number must be 11 digits")
        return mobile

    def clean_date_of_birth(self):
        date_of_birth =  self.cleaned_data.get("date_of_birth") #datetime.datetime.strptime(str(self.cleaned_data.get("date_of_birth")),"%Y-%b-%d")
        year_difference = datetime.date.today().year - date_of_birth.year
        if year_difference < 18:
                raise forms.ValidationError("You must be older than 18yrs")
        return date_of_birth

    def save(self, commit=True):
        # Save the provided password in hashed format
        # user = super().save(commit=False)
        user = super().save()
        if commit:
            user.save()
        return user




class RealtorDownlineForm(forms.ModelForm):
    full_name = forms.CharField(label="Full Name",required=True, widget=forms.TextInput(attrs={'placeholder':'Full Name'}))
    email = forms.EmailField(label="Email",required=True, widget=forms.TextInput(attrs={'placeholder':'Email Address'}))
    mobile = forms.IntegerField(label="Mobile",required=False, widget=forms.TextInput(attrs={'placeholder':'Mobile'}))
    
    class Meta:
        model = RealtorDownline
        fields = ('full_name','mobile','email',)



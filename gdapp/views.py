from numbers import Real
from xml.dom import ValidationErr
from django.shortcuts import render
from gdapp.admin import UserCreationForm
from .models import MyUser,Realtor
from .forms import RealtorForm
from django.db import transaction,IntegrityError
from django.contrib import messages
from .form_validation import validate_input
import re
from django.shortcuts import redirect

# Create your views here.


def get_ip(request):
	try:
		x_forward=request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip=x_forward.split(",")[0]
		else:ip= request.META.get("REMOTE_ADDR")
	except:
			ip=""
	return ip


def home(request):
    obj = None
    context = {}
    template = "home.html"
    return render(request,template,context)


def realtor_register(request):
    # args =  {}
    register_form = UserCreationForm()
    realtor_form =RealtorForm()


    if request.method == 'POST':    
                register_form = UserCreationForm(request.POST)
                realtor_form = RealtorForm(request.POST)
                if register_form.is_valid() and realtor_form.is_valid():
                        username = register_form.cleaned_data['username']
                        # email = register_form.cleaned_data['email']
                        password = register_form.cleaned_data['password2']
                        # first_name = request.POST.get('first_name',)
                        # last_name = request.POST.get('last_name',) 
                        # gender = request.POST.get('gender',)
                        # mobile = request.POST.get('mobile',)
                        # address = request.POST.get('address',)
                        # state_of_origin = request.POST.get('state_of_origin',)
                        # account_merchant = request.POST.get('account_merchant',)
                        # account_number = request.POST.get('account_number',)
                        # date_of_birth = request.POST.get('date_of_birth',)

                        try:
                                with transaction.atomic():
                                        print("Am in the atomic")
                                        user =  register_form.save(commit=False)
                                        user.set_password(password)
                                        user.ip_address = get_ip(request)
                                        user.role = MyUser.REALTOR
                                        user.is_realtor = True
                                        user.save()
                                        realtor = realtor_form.save(commit=False)
                                        realtor_user = MyUser.objects.get(username=username)
                                        realtor.realtor = realtor_user
                                        realtor.save()
                                        # if validate_input(mobile,first_name,last_name,account_number,state_of_origin,account_merchant) == True:
                                        #         realtor_user = MyUser.objects.get(username=username)
                                        #         Realtor.objects.create(realtor=realtor_user,address=address,mobile=mobile,first_name=first_name,last_name=last_name,account_number=account_number,state_of_origin=state_of_origin,account_merchant=account_merchant,gender=gender,date_of_birth=date_of_birth)
                                        messages.success(request, "Registeration Successful. Welcome to Goldenland")
                                        return redirect("/")
                        except IntegrityError as e:
                                messages.error(request,"Please ensure all details are filled correctly or contact us directly for assistance.")

                else:
                        # print("errors",register_form.errors.as_data(),realtor_form.errors.as_data())
                        messages.error(request, "Please correct the errors below and resubmit.")
                        print("Errro",register_form.errors)
                        context = {"register_form": register_form,"realtor_form":realtor_form}
                        template = "realtor.html"
                        return render(request,template,context)


    context = {"register_form": register_form,"realtor_form":realtor_form}
    template = "realtor.html"
    return render(request,template,context)
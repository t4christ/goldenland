from django.shortcuts import render,redirect,HttpResponseRedirect
from gdapp.admin import UserCreationForm
from .models import MyUser,Realtor, RealtorDownline,Property
from .forms import RealtorForm,LoginForm,RealtorDownlineForm
from django.db import transaction,IntegrityError
from django.contrib import messages
from .utils import generate_referral_code,get_ip
from django.contrib.auth import authenticate, login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse 

# Create your views here.





def home(request):
    obj = None
    context = {}
    template = "home.html"
    return render(request,template,context)


def user_login(request):
    if not request.user.is_authenticated:
        form = LoginForm(request.POST or None)
        next_url = request.GET.get('next')
        context = {"login_form": form,}
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if next_url is not None:
                    return reverse('gdapp:realtor_dashboard', kwargs={'realtor':username})
                messages.success(request, "Access Granted")
                return HttpResponseRedirect("/dashboard/{}".format(username)) #reverse('gdapp:realtor_dashboard', kwargs={'realtor':user_dash.referral_code}) #HttpResponseRedirect("/")
            else:
                messages.error(request, "Invalid Details.Try Again")

            return render(request, "realtor/realtor_login.html", context)


        return render(request, "realtor/realtor_login.html", context)

    else:
        return HttpResponseRedirect("/")



def user_logout(request):
	logout(request)
	messages.success(request, "Successfully Logged out. We were glad to have you onboard.")
	return HttpResponseRedirect('/')




def realtor_register(request):
    # args =  {}
    register_form = UserCreationForm()
    realtor_form = RealtorForm()
    context = {"register_form": register_form,"realtor_form":realtor_form}
    template = "realtor/realtor.html"

    if request.method == 'POST':    
                register_form = UserCreationForm(request.POST)
                realtor_form = RealtorForm(request.POST)
                context = {"register_form": register_form,"realtor_form":realtor_form}
                template = "realtor/realtor.html"
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
                                        realtor.referral_code = realtor.realtor.username + "_" + generate_referral_code()
                                        realtor.save()
                                        # if validate_input(mobile,first_name,last_name,account_number,state_of_origin,account_merchant) == True:
                                        #         realtor_user = MyUser.objects.get(username=username)
                                        #         Realtor.objects.create(realtor=realtor_user,address=address,mobile=mobile,first_name=first_name,last_name=last_name,account_number=account_number,state_of_origin=state_of_origin,account_merchant=account_merchant,gender=gender,date_of_birth=date_of_birth)
                                        messages.success(request, "Registeration Successful. Welcome to Goldenland")
                                        return redirect("/")
                        except IntegrityError as e:
                                messages.error(request,"Please ensure all details are filled correctly or contact us directly for assistance.")

                else:
                        messages.error(request, "Please correct the errors below and resubmit.")
                        print("Errro",register_form.errors)
                        return render(request,template,context)


#     context = {"register_form": register_form,"realtor_form":realtor_form}
    template = "realtor/realtor.html"
    return render(request,template,context)



@login_required
def realtor_dashboard(request,realtor):
        print("Realtor",realtor,request.user.username)
        if request.user.username != realtor:
                messages.error(request, "You must be logged in to access your dashboard.")
                return redirect("/")
        realtor =  Realtor.objects.get(realtor=request.user)
        clients = RealtorDownline.objects.filter(referral_code = realtor.referral_code)
        referral_link = request.build_absolute_uri(reverse('gdapp:client_realtor_info', args=(realtor.referral_code, )))
        context = {"realtor":realtor,"clients":clients,"referral_link":referral_link}
        template = "realtor/dashboard.html"
        return render(request,template,context)
        


def client_realtor_info(request,referral_code):
    realtor_downline_form = RealtorDownlineForm()
    context = {"realtor_downline_form":realtor_downline_form}
    template = "realtor/client.html"
    if request.method == 'POST':    
                realtor_downline_form = RealtorDownlineForm(request.POST)
                if realtor_downline_form.is_valid():
                        realtor_downline =  realtor_downline_form.save(commit=False)
                        realtor = Realtor.objects.get(referral_code=referral_code)
                        realtor_downline.realtor = realtor
                        realtor_downline.referral_code = referral_code
                        realtor_downline.save()
                        messages.success(request, "Success. Thanks for been part of goldenland")
                        return HttpResponseRedirect("/")

                else:
                        messages.error(request, "Please correct the errors below and resubmit.")
                        return render(request,template,context)

    return render(request,template,context)


  
def sell_property(request):
        template = "realtor/sell.html"
        validate_realtor = Realtor.objects.get(realtor = request.user)
        if validate_realtor:
                if request.method == 'POST': 
                        property_id = request.POST.get('property_id',)
                        units = request.POST.get('units',)
                        Property.objects.get(property_id=property_id).update(no_of_unit_or_plot=units)
                        messages.success(request, "Property Sold. Thanks for been part of goldenland")
                        return render(request,template)
        messages.error(request, "You are not authorised to sell this property")

        
        return render(request,template)
                        


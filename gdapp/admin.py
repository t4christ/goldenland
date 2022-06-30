from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from .utils import generate_referral_code
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin
from .models import MyUser,Realtor,RealtorClient,Property,NowSelling


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label="Username",required=True, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.CharField(label="Email",required=True, widget=forms.TextInput(attrs={'placeholder':'Email Address'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username','email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        if len(password1) <= 4:
            raise forms.ValidationError("Password is too short")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            exists = MyUser.objects.get(username=username)
            raise forms.ValidationError("This username is taken")
        except MyUser.DoesNotExist:
            return username
        except:
            raise forms.ValidationError("Sorry This Username is Taken.")



    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This Email is taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("Invalid Mail Format or  Email Taken.")

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username','email','ip_address','is_active','is_staff',)


        def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            if len(password1) <= 4:
                raise forms.ValidationError("Password is too short")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            return password2

        def clean_username(self):
            username = self.cleaned_data.get("username")
            try:
                exists = MyUser.objects.get(username=username)
                raise forms.ValidationError("This username is taken")
            except MyUser.DoesNotExist:
                return username
            except:
                raise forms.ValidationError("Sorry This Username is Taken.")



        def clean_email(self):
            email = self.cleaned_data.get("email")
            try:
                exists = MyUser.objects.get(email=email)
                raise forms.ValidationError("This Email is taken")
            except MyUser.DoesNotExist:
                return email
            except:
                raise forms.ValidationError("Invalid Mail Format or  Email Taken.")
                



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model = MyUser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    readonly_fields = [
        'ip_address',
       
    ]
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email','is_realtor','is_staff',)
    list_filter = ()
    fieldsets = (
        (None, {'fields': ()}),
        ('Personal info', {'fields': ('username','email',)}),
        ('Permissions', {'fields': ('is_realtor','role','is_staff','is_admin',)}),
        ('Group Permissions', {
            'fields': ('groups',)
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email','password1', 'password2',),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    # def save_model(self, request, obj, form, change):
    #     print("My user",change)
    #     # print("My user1",obj.is_admin)
    #     print("M",obj.is_staff,obj.username)
    #     if obj.is_staff:
    #         print("Am here staff")
    #         obj.staff = True
    #         group_name = Group.objects.get(name = 'Realtor')
    #         user = MyUser.objects.get(username=obj.username)
    #         group_name.user_set.add(user)
    #         super(UserAdmin, self).save_model(request, obj, form, change)
    #     else:
    #         print("Am in the else")
    #         obj.staff = False
    #         super(UserAdmin, self).save_model(request, obj, form, change)

class PropertyAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and obj.property_name is not None:
            print("Am here")
            obj.property_id = "{}_{}".format(obj.property_name.lower(), generate_referral_code())
            super(PropertyAdmin, self).save_model(request, obj, form, change)
        else:
            super(PropertyAdmin, self).save_model(request, obj, form, change)


class RealtorAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists()


    def save_model(self, request, obj, form, change):
        if obj.referral is None:
            obj.referral = obj.referral
            super(RealtorAdmin, self).save_model(request, obj, form, change)
        else:
            super(RealtorAdmin, self).save_model(request, obj, form, change)

admin.site.register(Property,PropertyAdmin)

# Now register the new UserAdmin...

admin.site.register(MyUser, UserAdmin)
admin.site.register(Realtor,RealtorAdmin)
admin.site.register(NowSelling)
admin.site.register(RealtorClient)



# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)
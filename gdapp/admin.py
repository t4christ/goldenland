from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin
from gdapp.models import MyUser,Realtor

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label="Username",required=True, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.CharField(label="Email",required=True, widget=forms.TextInput(attrs={'placeholder':'Email Address'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username','email')

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
        fields = ('username','email', 'password','ip_address','is_active', 'is_admin')


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
    readonly_fields = [
        'ip_address',
        'email',
       
    ]
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email','is_admin','is_realtor')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ( 'password',)}),
        ('Personal info', {'fields': ('username','email',)}),
        ('Permissions', {'fields': ('is_admin','is_realtor','role')}),
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


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(Realtor)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)

# Unregister the provided model admin
# admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
# @admin.register(MyUser)
# class CustomUserAdmin(UserAdmin):
#     list_display = ('first_name','last_name','email','is_realtor')  # Contain only fields in your `custom-user-model`
#     list_filter = ()  # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
#     search_fields = ('first_name','last_name')  # Contain only fields in your `custom-user-model` intended for searching
#     ordering = ()  # Contain only fields in your `custom-user-model` intended to ordering
#     filter_horizontal = () # Leave it empty. You have neither `groups` or `user_permissions`
#     add_fieldsets = (
#             (None, {'fields': ('mobile','groups', 'user_permissions', 'is_superuser', 'is_staff', 'date_joined')}),
#     )

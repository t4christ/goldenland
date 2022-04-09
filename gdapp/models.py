from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


GENDER = (
        ('None','None'),
        ('Male','Male'),
        ('Female', 'Female'),
    )

class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('Must include username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password):
        """
        Creates and saves a superuser with the given username, email and password.
        """

        user = self.create_user(
			username=username,
			email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser,PermissionsMixin):
    MANAGER = 1
    REALTOR = 2
        
    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (REALTOR, 'Realtor'),
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        default=""
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        default="youremailisrequired",
        unique=True,
    )

    ip_address=models.CharField(max_length=120, default='ABC')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    # company=models.CharField(max_length=550,default='')
    # occupation=models.CharField(max_length=550, default='')

    is_realtor = models.BooleanField(default=False)
    #                 verbose_name='Is Paid Member')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return " ".join([self.first_name,self.last_name])


    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Realtor(models.Model):
    realtor = models.OneToOneField(MyUser, on_delete=models.CASCADE, null=True, blank = True)
    first_name = models.CharField(max_length=150,default='')
    last_name = models.CharField(max_length=150,default='')
    address = models.CharField(max_length=500,default='')
    state_of_origin = models.CharField(max_length=500,default='')
    account_merchant = models.CharField(max_length=500,default='')
    account_number = models.CharField(max_length=500,default='',unique=True)
    date_of_birth = models.DateField()
    mobile= models.CharField(max_length=13,null=True,blank=True,unique=True)
    gender= models.CharField(max_length=15, choices=GENDER,default='None')

    def __str__(self):
        return self.first_name + self.last_name
from django.db import models
from django.conf import settings
from .utils import generate_referral_code
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video


GENDER = (
        ('None','None'),
        ('Male','Male'),
        ('Female', 'Female'),
    )


PROPERTY_TYPE= (
        ('None','None'),
        ('Land','Land'),
        ('Buildings', 'Buildings'),
    )


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('Must include username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = self.normalize_email(email), **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,password,**extra_fields):
        """
        Creates and saves a superuser with the given username, email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username,email, password, **extra_fields)       

        # user = self.create_user(
		# 	username=username,
		# 	email=email,
        #     password=password
        # )
        # user.is_admin = True
        # user.save(using=self._db)
        # return user



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
        default="newuser@goldenland.ng",
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
    is_staff = models.BooleanField(default=False)


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

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin



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
    referral_code = models.CharField(max_length=40,default='',unique=True)
    referral = models.CharField(max_length=50,default='',blank=True)


    def save(self, *args, **kwargs):
        if self.referral is None:
            self.referral = self.referral
        super(Realtor, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + self.last_name


class RealtorClient(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, null=True, blank = True)
    # property = models.ForeignKey(, on_delete=models.CASCADE, null=True, blank = True)
    full_name = models.CharField(max_length=150,default='')
    email = models.CharField(max_length=150,default='',unique=True)
    mobile = models.CharField(max_length=13,default='',unique=True)
    referral_code = models.CharField(max_length=40,default='')

    def __str__(self):
        return "Client name is " + self.full_name 


class Reward(models.Model):
    FIFTEEN = 1
    THREE = 2
        
    REWARD_PERCENTAGE_CHOICES = (
        (FIFTEEN, '15'),
        (THREE, '3'),
    )
    realtor = models.OneToOneField(Realtor, on_delete=models.CASCADE, null=True, blank = True)
    current_reward_percentage = models.PositiveSmallIntegerField(choices=REWARD_PERCENTAGE_CHOICES, blank=True, null=True)
    fifteen_percent_unit = models.PositiveSmallIntegerField(default=0)
    three_percent_unit = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{} currently on {} percentage reward".format(self.realtor.first_name,self.current_reward_percentage)


class Property(models.Model):
    property_name = models.CharField(max_length=500,null=False)
    image = models.ImageField(upload_to='media/properties')
    video = models.FileField(upload_to='media/properties/videos',blank=True,storage=VideoMediaCloudinaryStorage(),
                              validators=[validate_video])
    property_id = models.CharField(max_length=50, default='',null=True,blank=True)
    property_type = models.CharField(max_length=15, choices=PROPERTY_TYPE,default='None')
    location = models.CharField(max_length=500,default='',null=False)
    no_of_unit_or_plot = models.PositiveSmallIntegerField(default=0)
    price_per_unit_plot = models.CharField(max_length=15,default='')
    on_promo = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    promo_price_per_unit_or_plot = models.CharField(max_length=15,default='',blank=True,null=True)

    def save(self, *args, **kwargs):
        if self.property_name is not None:
            self.property_id = "{}_{}".format(self.property_name.lower(), generate_referral_code())
        super(Property, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        print("Update sales",kwargs['no_of_unit_or_plot'])
        unit_status = kwargs['no_of_unit_or_plot'] < self.no_of_unit_or_plot
        if unit_status:
            self.no_of_unit_or_plot = self.no_of_unit_or_plot - kwargs['no_of_unit_or_plot']
        else:
            return "Cannot sell at the moment. Units left is lesser than what is to be sold"
        super(Property, self).update(*args, **kwargs)

    def __str__(self):
        if self.on_promo:
            return "Property {} on promo going for {}".format(self.property_name,self.promo_price_per_unit_or_plot)
        return "Property {} going for {}".format(self.property_name,self.price_per_unit_plot) 


class NowSelling(models.Model):
    property_name = models.CharField(max_length=500,null=False)
    image = models.ImageField(upload_to='media/properties')
    property_type = models.CharField(max_length=15, choices=PROPERTY_TYPE,default='None')
    info = models.TextField(default="")
    title = models.CharField(max_length=80,default="",blank=True)
    location = models.CharField(max_length=500,default='',null=False)
    unit_of_plot = models.PositiveSmallIntegerField(default=0)
    price_per_unit_plot = models.CharField(max_length=15,default='')
    on_promo = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_sold_out =  models.BooleanField(default=False)
    promo_price_per_unit_or_plot = models.CharField(max_length=15,default='',blank=True,null=True)

    # def save(self, *args, **kwargs):
    #     if self.property_name is not None:
    #         print("Am here")
    #         self.property_id = "{}_{}".format(self.property_name.lower(), generate_referral_code())
    #     super(Property, self).save(*args, **kwargs)

    # def update(self, *args, **kwargs):
    #     print("Update sales",kwargs['no_of_unit_or_plot'])
    #     unit_status = kwargs['no_of_unit_or_plot'] < self.no_of_unit_or_plot
    #     if unit_status:
    #         self.no_of_unit_or_plot = self.no_of_unit_or_plot - kwargs['no_of_unit_or_plot']
    #     else:
    #         return "Cannot sell at the moment. Units left is lesser than what is to be sold"
    #     super(Property, self).update(*args, **kwargs)

    def __str__(self):
        if self.on_promo:
            return "Property {} on promo going for {}".format(self.property_name,self.promo_price_per_unit_or_plot)
        return "Property {} going for {}".format(self.property_name,self.price_per_unit_plot) 


class SoldProperty(models.Model):
    property_name = models.CharField(max_length=500,null=False)
    # image = models.ImageField(upload_to='media/properties')
    property_id = models.CharField(max_length=50, default='')
    property_type = models.CharField(max_length=15, choices=GENDER,default='None')
    location = models.CharField(max_length=500,default='',null=False)
    no_of_unit_or_plot = models.PositiveSmallIntegerField(default=0)
    price_per_unit_plot = models.CharField(max_length=15,default='')
    on_promo = models.BooleanField(default=False)
    promo_price_per_unit_or_plot = models.CharField(max_length=15,default='',blank=True,null=True)


    def __str__(self):
            return "Property {} was sold on {}. {} units".format(self.property_name,self.no_of_unit_or_plot)

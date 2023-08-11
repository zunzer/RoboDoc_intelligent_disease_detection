from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from common.models import UserSymptoms,Symptoms, Symptom_list

class myUserManger(BaseUserManager):
    def create_user(self, username, email, age,usertype,
                    country,password=None):

        if not email:
            raise ValueError("Email is missing")
        if not username:
            raise ValueError("No username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            #last_name = last_name,
            age = age,
            #sex = sex,
            usertype = usertype,
            #weight = weight,
            #height = height,
            country = country
        )

        user.set_password(password)
        user.save(using= self._db)

        return user

    def create_superuser(self, email,username,password, age = '1',
                          usertype = '1', country = 'germany'):
        user = self.create_user(
            username= username,
            email = email,age= age,usertype= usertype,
             country = country,
            password= password
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user






class myUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100,unique=True) # first name
    email = models.EmailField(verbose_name="email",max_length=100, unique=True)
    date_joined = models.DateTimeField(verbose_name="date-joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last-login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # STANDARD VARS  HERE THE NEW

    #last_name = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    #sex = models.CharField(max_length=6)
    usertype = models.CharField(max_length=8)
    #weight = models.CharField(max_length=3)
    #height = models.CharField(max_length=3)
    country = models.CharField(max_length=150)

    objects = myUserManger()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','age','usertype', 'country']


def __str__(self):
    return self.username

def has_perm(self,perm, obj=None):
    return self.is_admin

def has_module_perms(self,app_label):
    return True

# Create your models here.

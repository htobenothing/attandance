from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.
from .data import MemberType,Zone
from datetime import datetime

class District(models.Model):
    District_ID = models.AutoField(primary_key=True)
    Zone = models.CharField(max_length=3, choices=Zone)
    District_Name = models.CharField(max_length=50)
    Create_Date = models.DateTimeField()
    update_at = models.DateTimeField(auto_now_add=True)
    Address = models.CharField(max_length=120)
    PostCode = models.CharField(max_length=20)
    Status = models.BooleanField(default=True)

    def __str__(self):
        return "Zone {0}-{1}".format(self.Zone,self.District_Name)


class Member(models.Model):

    Member_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Given_Name = models.CharField(max_length=50, blank=True)
    Family_Name = models.CharField(max_length=50, blank=True)
    Other_Name = models.CharField(max_length=120,blank=True)
    Member_Type = models.CharField(max_length=1, choices=MemberType)
    District_ID = models.ForeignKey(District,on_delete=models.CASCADE,default='0')
    Phone = models.CharField(max_length=50)
    Email = models.CharField(max_length=120,default='', blank=True)
    Create_Date = models.DateTimeField(auto_now_add=True)
    Status = models.BooleanField(default=True)


    def __unicode__(self):
        return "{0}:{1}".format(self.Member_ID, self.Name)

    def __str__(self):
        return "{0}:{1}".format(self.Member_ID, self.Name)

class AttendanceHistory(models.Model):
    History_ID = models.AutoField(primary_key=True)
    Member_ID = models.ForeignKey(Member, related_name='AttandanceHistorys', on_delete=models.CASCADE)
    Create_Date = models.DateTimeField(auto_now_add=True)
    Lords_Table = models.BooleanField(default=True)
    Prayer_Meeting = models.BooleanField(default=True)
    Morning_Revival = models.BooleanField(default=True)
    Bible_Reading = models.BooleanField(default=True)
    Small_Group = models.BooleanField(default=True)

    def __str__(self):
        return "{0}".format(self.History_ID)






class AccountManager(BaseUserManager):

    def create_user(self,email,password=None,**kwargs):
        if not email:
            raise ValueError('Users must have a valid email address')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid name')

        account = self.model(
            email=self.normalize_email(email),username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self,email,password,**kwargs):
        account = self.create_user(email,password,**kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40,unique=True)

    first_name = models.CharField(max_length=40,blank=True)
    last_name = models.CharField(max_length=40,blank=True)
    tagline = models.CharField(max_length=140,blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join(self.firstName,self.lastName)

    def get_short_name(self):
        return self.firstName



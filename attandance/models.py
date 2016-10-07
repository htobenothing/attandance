from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.


MemberType = (
    ('1', 'Children'),
    ('2', 'Pre-Youth'),
    ('3', 'Campus'),
    ('4', 'Young-Working'),
    ('5', 'Community'),
    ('6', 'Full-time')

)


class Member(models.Model):
    Member_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Member_Type = models.CharField(max_length=1, choices=MemberType)
    Contact = models.CharField(max_length=50)
    Password = models.CharField(max_length=255)
    Create_Date = models.DateTimeField(auto_now_add=True)
    Status = models.BooleanField(default=True)

    def __str__(self):
        return "{0}:{1}".format(self.Member_ID, self.Name)

    class Meta:
        ordering = ('Create_Date',)

class AttendanceHistory(models.Model):
    History_ID = models.AutoField(primary_key=True)
    Member_ID = models.ForeignKey(Member,on_delete=models.CASCADE)
    Create_Date = models.DateTimeField(auto_now_add=True)
    Lords_Table = models.BooleanField(default=True)
    Prayer_Meeting = models.BooleanField(default=True)
    Morning_Revival = models.BooleanField(default=True)
    Bible_Reading = models.BooleanField(default=True)
    Small_Group = models.BooleanField(default=True)

    def __str__(self):
        return "{0}".format(self.History_ID)


# class AccountManager(BaseUserManager):
#
#     def create_user(self,email,password=None,**kwargs):
#         if not email:
#             raise ValueError('Users must have a valid email address')
#
#         if not kwargs.get('userName'):
#             raise ValueError('Users must have a valid name')
#
#         account = self.model(
#             email=self.normalize_email(email),userName=kwargs.get('userName')
#         )
#
#         account.set_password(password)
#         account.save()
#
#         return account
#
#     def create_superuser(self,email,password,**kwargs):
#         account = self.model(
#             email = self.normalize_email(email),userName=kwargs.get('userName')
#         )
#
#         account.isAdmin = True
#         account.save()
#
#         return account
#
#
# class Account(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     userName = models.CharField(max_length=40,unique=True)
#
#     firstName = models.CharField(max_length=40,blank=True)
#     lastName = models.CharField(max_length=40,blank=True)
#     tagLine = models.CharField(max_length=140,blank=True)
#
#     isAdmin = models.BooleanField(default=False)
#     isActive = models.BooleanField(default=True)
#
#     createDate = models.DateTimeField(auto_now_add=True)
#     updateDate = models.DateTimeField(auto_now=True)
#
#     objects = AccountManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['userName']
#
#     def __unicode__(self):
#         return self.email
#
#     def get_full_name(self):
#         return ' '.join(self.firstName,self.lastName)
#
#     def get_short_name(self):
#         return self.firstName
#
#

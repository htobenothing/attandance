from django.contrib import admin

# Register your models here.

from .models import Member,AttendanceHistory

admin.site.register([Member,AttendanceHistory])
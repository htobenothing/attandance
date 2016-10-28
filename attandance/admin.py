from django.contrib import admin

# Register your models here.

from .models import Member,AttendanceHistory,District

admin.site.register([Member,AttendanceHistory,District])
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from authentication.models import *

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'street', 'neighbourhood', 'age')
    
    fieldsets = [
        ("Location Info", 
            {
                "fields": ["city", "state", "street", "neighbourhood"],
            }
        ),
        ("User Aditional Info", 
            {
                "fields": ["age"],
            }
        ),
    ]
    
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'cpf', 'phone', 'user_info')
    
    fieldsets = [
        ("Login Info", 
            {
                "fields": ["username", "password", "cpf"],
            }
        ),
        ("Contact Info", 
            {
                "fields": ["phone", 'email'],
            }
        ),
        ("Aditional Info", 
            {
                "fields": ["user_info"],
            }
        ),
    ]

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
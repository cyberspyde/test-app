from django.contrib import admin
from .models import Test, Question, Answer, User
from django.contrib.auth.admin import UserAdmin

class CustomUser(admin.ModelAdmin):
    list_display = ['phone_number', 'name', 'id']


admin.site.register(User, CustomUser)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)

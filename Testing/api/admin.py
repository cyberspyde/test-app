from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUser(admin.ModelAdmin):
    list_display = ['phone_number', 'name', 'id']

class CustomTest(admin.ModelAdmin):
    list_display = ['id', 'test_title']

class CustomQuestion(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'test']

class CustomAnswer(admin.ModelAdmin):
    list_display = ['id', 'answer_text', 'created_by']

class CustomCategory(admin.ModelAdmin):
    list_display = ['id', 'name']

class CustomTestRoom(admin.ModelAdmin):
    list_display = ['room_key', 'created_at', 'is_active']

admin.site.register(User, CustomUser)
admin.site.register(Test, CustomTest)
admin.site.register(Question, CustomQuestion)
admin.site.register(Answer, CustomAnswer)
admin.site.register(Category, CustomCategory)
admin.site.register(TestRoom, CustomTestRoom)
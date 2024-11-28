from django.contrib import admin
from .models import Test, Question, Answer, User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)

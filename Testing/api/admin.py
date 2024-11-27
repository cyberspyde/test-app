from django.contrib import admin
from .models import User, Test, Question, Answer

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'role']

admin.site.register(User, UserAdmin)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)

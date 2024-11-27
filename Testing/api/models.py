from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(models.Model):
    ROLE_CHOICES = [
        ('user', 'Oddiy foydalanuvchi'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin')
    ]

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.phone_number
    
class Test(models.Model):
    
    STATUS_CHOICES = [
        ('published', 'Post qilingan'),
        ('in_queue', 'Navbatda')
    ]

    test_title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_queue')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test_title
    
class Question(models.Model):

    question_text = models.TextField()
    question_audio = models.FileField(upload_to='question_audio/', blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_questions', null=True)

    def __str__(self):
        return self.question_text[:50]
    

class Answer(models.Model):

    answer_text = models.TextField(blank=True, null=True)
    answer_audio = models.FileField(upload_to='answer_audio/', blank=True, null=True)
    test = models.ForeignKey(Test,on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.question} savolga {self.user} tomonidan javob"
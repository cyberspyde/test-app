from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
    
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Telefon raqam kiritilishi shart")
        if not name:
            raise ValueError("Ism kiritilishi shart")

        extra_fields.setdefault('is_active', True)
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)

        if extrafields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extrafields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(phone_number, name, password, **extrafields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('user', 'Oddiy foydalanuvchi'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]

    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Avoid conflict with default User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Avoid conflict with default User
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.phone_number} ({self.name})"

class Test(models.Model):
    
    STATUS_CHOICES = [
        ('published', 'Post qilingan'),
        ('in_queue', 'Navbatda')
    ]

    test_title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_queue')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question_text[:50]
    

class Answer(models.Model):

    answer_text = models.TextField(blank=True, null=True)
    answer_audio = models.FileField(upload_to='answer_audio/', blank=True, null=True)
    test = models.ForeignKey(Test,on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.question} savolga {self.user} tomonidan javob"
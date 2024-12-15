from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.utils.crypto import get_random_string
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")
        if not name:
            raise ValueError("Ism kiritilishi shart")

        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)

        if extrafields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extrafields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, name, password, **extrafields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('user', 'Oddiy foydalanuvchi'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]

    cities = [
        ('jizzakh', 'Jizzax'),
        ('tashkent', 'Toshkent'), 
        ('samarkand', 'Samarqand'),
        ('fergana', 'Farg`ona'),
        ('andijan', 'Andijon'),
        ('namangan', 'Namangan'),
        ('bukhara', 'Buxoro'),
        ('termiz', 'Termiz'),
        ('navoi', 'Navoiy'),
        ('qashqadaryo', 'Qashqadaryo'),
        ('sirdaryo', 'Sirdaryo'),
        ('surxondaryo', 'Surxondaryo')
    ]

    account_types = [
        ('teacher', 'Ustoz'),
        ('student', 'O`quvchi'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=20, choices=cities, null=True, blank=True)
    type = models.CharField(max_length=20, choices=account_types, null=True, blank=True)
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    interests = models.ManyToManyField(Category, related_name='interested_users', blank=True)
    lifetime_quiz_points = models.IntegerField(null=True, blank=True)
    weekly_points = ArrayField(models.IntegerField(), size=7, null=True, blank=True)
    tests_done = models.ManyToManyField('Test', related_name='tests_done_by', blank=True)
    favorites = ArrayField(models.CharField(max_length=20), size=5, null=True, blank=True)

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    MAX_INTEREST = 3

    def add_interest(self, category):
        if self.interests.count() < self.MAX_INTEREST:
            self.interests.add(category)
        else:
            raise ValueError(f"{self.MAX_INTEREST} dan ortiq qiziqish tanlash mumkin emas!")

    def get_interests(self):
        return self.interests.all()

    def __str__(self):
        return f"{self.email} ({self.name})"

class Test(models.Model):
    
    STATUS_CHOICES = [
        ('published', 'published'),
        ('in_queue', 'in_queue')
    ]

    test_title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_queue')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    random_generator = models.BooleanField(blank=True, null=True)
    number_of_questions = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.CharField(max_length=50), size=5, blank=True, null=True)

    def generate_room_key(self):
        return get_random_string(length=6).upper()

    def __str__(self):
        return self.test_title

class TestRoom(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    room_key = models.CharField(max_length=6, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_room(cls, test):
        room_key = test.generate_room_key()
        while cls.objects.filter(room_key=room_key).exists():
            room_key = test.generate_room_key()

        return cls.objects.create(
            test=test,
            room_key=room_key
        )

class TestParticipant(models.Model):
    STATUSES = (
        ('waiting', 'Waiting'),
        ('ready', 'Ready'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(TestRoom, on_delete=models.CASCADE, related_name='participants')
    status = models.CharField(max_length=20, choices=STATUSES, default='waiting')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')

class Question(models.Model):
    question_type = [
        ('multiple_choice', 'multiple_choice'),
        ('true_false', 'true_false'),
        ('type_answer', 'type_answer'),
        ('poll', 'poll'),
        ('audio', 'audio')
    ]

    points = [
        (5, '5 sec'),
        (10, '10 sec'),
        (20, '20 sec'),
        (30, '30 sec'),
        (45, '45 sec'),
        (60, '60 sec'),
        (90, '90 sec'),
        (120, '120'),
    ]

    timer_limits = [
        (50, '50 pt'),
        (100, '100 pt'),
        (200, '200 pt'),
        (250, '250 pt'),
        (500, '500 pt'),
        (750, '750 pt'),
        (1000, '1000 pt'),
        (2000, '2000 pt'),
    ]

    question_text = models.TextField()
    question_audio = models.FileField(upload_to='question_audio/', blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    point = models.IntegerField(choices=points, default=0)
    timer_limit = models.IntegerField(choices=timer_limits, default=50)
    type = models.CharField(max_length=50, choices=question_type, null=True, blank=True)
    image = models.FileField(upload_to='question_image/', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text[:50]
    

class Answer(models.Model):
    answer_text = models.TextField(blank=True, null=True)
    answer_audio = models.FileField(upload_to='answer_audio/', blank=True, null=True)
    test = models.ForeignKey(Test,on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    correct_answer = models.BooleanField(default=False)
    participant = models.ForeignKey(TestParticipant, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')

    def __str__(self):
        return f"{self.question} savolga {self.created_by} tomonidan javob"

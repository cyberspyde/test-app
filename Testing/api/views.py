from rest_framework import viewsets, permissions, status,  views
from rest_framework.response import Response
from .models import User, Test, Question, Answer, Category
from .serializers import (
    UserSerializer,
    TestSerializer, 
    QuestionSerializer, 
    AnswerSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from collections import Counter
from random import sample
from django.db import transaction


class CategoryPerformanceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        performance_data = {}
        user = request.user
        tests_done = user.tests_done.all()
        mylist = []

        for test in tests_done:
            mylist.append(test.category)
        
        tests_done_with_categories = Counter(mylist)
        performance_data = { category.name : int(tests_done_with_categories.get(category, 0) / tests_done.count() * 100) for category in mylist}
        
        response_data = {
            'total_tests_done' : tests_done.count(),
            'performance' : performance_data
        }
        return Response(response_data)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response(
                {"error" : "Telefon raqam va parol berilishi shart"}, status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, phone_number=phone_number, password=password)
        if not user:
            return Response(
                {"error": "Telefon raqam yoki parol noto'g'ri"}, status=status.HTTP_401_UNAUTHORIZED,
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        test_instance = serializer.save(created_by=self.request.user)
        random_generator = self.request.data.get('random_generator', False)
        number_of_questions = self.request.data.get('number_of_questions')
        if random_generator:
            category = serializer.validated_data.get('category')
            questions = Question.objects.filter(category=category)

            selected_questions = sample(list(questions), min(len(questions), 30))

            with transaction.atomic():
                for question in selected_questions:
                    question.test = test_instance
                    question.save()
        
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_permisssions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
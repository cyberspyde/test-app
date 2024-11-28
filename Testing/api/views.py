from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Test, Question, Answer
from .serializers import (
    UserSerializer,
    TestSerializer, 
    QuestionSerializer, 
    AnswerSerializer
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['POST'])
    def publish_test(self, request, pk=None):
        test = self.get_object()
        test.status = 'published'
        test.save()
        return Response({'status': 'test published'}, status=status.HTTP_200_OK)
        
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(created_by=user)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Answer.objects.filter(user=user)

    @action(detail=False, methods=['GET'])
    def get_user_answers(self, request):
        answers = Answer.objects.filter(user=request.user)
        serializer = self.get_serializer(answers, many=True)
        return Response(serializer.data)
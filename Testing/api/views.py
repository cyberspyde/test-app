from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Test, Question, Answer
from .serializers import (UserSerializer, TestSerializer, QuestionSerializer, AnswerSerializer)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def get_current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def perform_create(self, serializer):
        serializer.savev(created_by=self.request.user)

    @action(detail=True, methods=['POST'])
    def publish_test(self, request, pk=None):
        test = self.get_object()
        test.status = 'published'
        test.save()
        return Response({'status' : 'test_published'}, status=status.HTTP_200_OK)
    
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def get_user_answer(self, request):
        answers = Answer.objects.filter(user=request.user)
        serializer = self.get_serializer(answers, many=True)
        return Response(serializer.data)
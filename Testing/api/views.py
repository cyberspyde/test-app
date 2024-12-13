from rest_framework import viewsets, permissions, status,  views
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from collections import Counter
from random import sample
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from django.db.models import Count

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

class TopAuthorsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        top_authors = User.objects.annotate(
            test_count=Count('test')).order_by('-test_count')[:10]
        
        authors_data = [
            {
                'id': author.id,
                'name': author.name,
                'test_count': author.test_count
            } for author in top_authors
        ]

        return Response({
            'top_authors' : authors_data
        })
    
class WeeklyPointsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):

        weekly_points = User.objects.get(pk=request.user.id).weekly_points
        return Response({
            "weekly-points" : weekly_points
        })
    def post(self, request, *args, **kwargs):
        user = request.user
        new_point = int(request.data.get('new_point'))
        if len(user.weekly_points) == 7:
            user.weekly_points.pop()
        user.weekly_points.insert(0, new_point)
        user.save()
        return Response({
            "weekly-points" : user.weekly_points
        })

class FavoritesView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        tests = Test.objects.all()
    
        favorite_to_add = int(request.data.get('favorite'))
        if not favorite_to_add:
            return Response({"error" : "Favorite value is not passed"}, status=400)
        if user.favorites is None:
            user.favorites = []
        if len(user.favorites) >= 5:
            return Response({"error": "Maximum number of favorites reached"}, status=400)
        
        mylist = []
        for t in user.favorites:
            mylist.append(int(t))

        if favorite_to_add in mylist:
            return Response({"error": "The favorite is already in the list."}, status=400)
        
        for k in tests:
            if favorite_to_add == k.id:
                user.favorites.append(favorite_to_add)
                user.save()
            
                return Response({"message" : "Favorite added successfully", "favorites" : user.favorites}, status=200)

        return Response({"error" : "ID you specified is not in the list of TESTS!"}, status=400)

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'phone_number']
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def change_role(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"detail" : "Only staff can change user roles"},
                status=status.HTTP_403_FORBIDDEN
            )
        user = self.get_object()
        new_role = request.data.get('role')

        if new_role not in dict(User.ROLE_CHOICES):
            return Response(
                {"detail" "Invalid Role"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.role = new_role
        user.save()

        return Response(
            {"detail" : f"Role changed to {new_role}"},
            status=status.HTTP_200_OK
        )
    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class TestRoomViewSet(viewsets.ModelViewSet):
    queryset = TestRoom.objects.all()
    serializer_class = TestRoomSerializer

    def create(self, request):
        test_id = request.data.get('test')
        test = Test.objects.get(id=test_id)

        room = TestRoom.create_room(test)
        TestParticipant.objects.create(
            user=request.user,
            room=room,
            status='waiting'                
        )

        serializer = self.get_serializer(room)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        room = self.get_object()

        if not room.is_active:
            return Response({
                'error': 'Room is no longer available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        participant, created = TestParticipant.objects.get_or_create(
            user=request.user,
            room=room,
            defaults={'status': 'waiting'}
        )

        serializer = TestRoomSerializer(room)
        return Response(serializer.data)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['test_title']

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['question_text']

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['answer_text']

    def get_permisssions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TestViewSet, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls))
]
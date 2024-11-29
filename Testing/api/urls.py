from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, QuestionViewSet, AnswerViewSet, CustomAuthToken, UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api/users/create/', UserCreateView.as_view(), name='user-create'),
    # path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    # path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]
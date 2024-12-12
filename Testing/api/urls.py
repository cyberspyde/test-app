from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *
from .swagger import schema_view
from rest_framework_simplejwt import views as jwt_views
router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
#router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api/users/create/', UserCreateView.as_view(), name='user-create'),
    # path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    # path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    #path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api-token/', jwt_views.TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api-token-refresh/', jwt_views.TokenRefreshView.as_view(), name = 'token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('user-performance/', CategoryPerformanceView.as_view(), name='user-performance'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('top-authors/', TopAuthorsView.as_view(), name='top-authors'),
    path('weekly-points/', WeeklyPointsView.as_view(), name='weekly-points')
]
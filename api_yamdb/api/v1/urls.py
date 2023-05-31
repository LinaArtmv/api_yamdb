from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserAuthenticationView,
                    UserRegistration, UserViewset)

v1_router = SimpleRouter()
v1_router.register('users', UserViewset, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

auth_patterns = [
    path('signup/', UserRegistration.as_view({'post': 'create'})),
    path('token/', UserAuthenticationView.as_view())
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_patterns))
]

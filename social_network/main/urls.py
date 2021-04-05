from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'like', views.LikeViewSet)
router.register(r'dislike', views.DislikeViewSet)

urlpatterns = [
    path('', views.RegistrationAPI.as_view(), name='registration'),
    path('sign_in', views.SignInAPI.as_view(), name='sign_in'),
    path('blog', views.PostsFeedAPI.as_view(), name='blog'),
    path('add_post', views.CreatePostAPI.as_view(), name='add_post'),
    path('logout', views.logout_user, name='logout'),
    path('like/<int:post_id>', views.LikeAPI.as_view(), name='like'),
    path('unlike/<int:post_id>', views.DislikeAPI.as_view(), name='unlike'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/analytics/', views.LikesAnalyticsAPI.as_view(), name='analytics'),
    path('api/', include(router.urls)),
    path('api/models/', include('rest_framework.urls', namespace='rest_framework'))
]
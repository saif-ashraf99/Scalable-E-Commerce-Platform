from django.urls import path
from .views import CreateUserView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
]
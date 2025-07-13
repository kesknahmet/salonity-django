from django.urls import path
from .views import (
    RegisterView, CustomAuthToken, CustomerProfileUpdateView,
    CustomerLoyaltyView, PointHistoryView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', CustomerProfileUpdateView.as_view(), name='customer-profile-update'),
    path('loyalty/', CustomerLoyaltyView.as_view(), name='customer-loyalty'),
    path('points/history/', PointHistoryView.as_view(), name='point-history'),
] 
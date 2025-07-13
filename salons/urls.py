from django.urls import path
from .views import (
    SalonListView, SalonDetailView, SalonOwnerRegisterView,
    SalonProfileUpdateView, SalonWorkingHoursUpdateView
)

urlpatterns = [
    path('', SalonListView.as_view(), name='salon-list'),
    path('<uuid:id>/', SalonDetailView.as_view(), name='salon-detail'),
    path('owner/register/', SalonOwnerRegisterView.as_view(), name='salon-owner-register'),
    path('owner/profile/', SalonProfileUpdateView.as_view(), name='salon-profile-update'),
    path('owner/working-hours/<int:day_of_week>/', SalonWorkingHoursUpdateView.as_view(), name='salon-working-hours-update'),
] 
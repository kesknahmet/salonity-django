from django.urls import path
from .views import ServiceListView, ServiceCategoryListView, SalonServicesView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list'),
    path('categories/', ServiceCategoryListView.as_view(), name='service-categories'),
    path('salon/<uuid:salon_id>/', SalonServicesView.as_view(), name='salon-services'),
] 
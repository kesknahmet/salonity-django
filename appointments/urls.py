from django.urls import path
from .views import (
    AppointmentCreateView, AppointmentListView, AppointmentDetailView,
    AppointmentUpdateView, AppointmentCancelView, AppointmentReviewCreateView
)

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('list/', AppointmentListView.as_view(), name='appointment-list'),
    path('<uuid:id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<uuid:id>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('<uuid:id>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
    path('<uuid:appointment_id>/review/', AppointmentReviewCreateView.as_view(), name='appointment-review'),
] 
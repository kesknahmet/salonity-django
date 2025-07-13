from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from .models import Salon, SalonWorkingHours
from .serializers import (
    SalonListSerializer, SalonDetailSerializer, SalonOwnerRegisterSerializer,
    SalonProfileUpdateSerializer, SalonWorkingHoursUpdateSerializer
)

class SalonListView(generics.ListAPIView):
    """Salon listesi - filtreleme ve arama ile"""
    queryset = Salon.objects.filter(is_active=True)
    serializer_class = SalonListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['salon_type', 'city', 'district', 'is_verified']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['rating', 'total_reviews', 'created_at']
    ordering = ['-rating', '-total_reviews']

class SalonDetailView(generics.RetrieveAPIView):
    """Salon detay bilgileri"""
    queryset = Salon.objects.filter(is_active=True)
    serializer_class = SalonDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class SalonOwnerRegisterView(generics.CreateAPIView):
    """Salon sahibi kayıt"""
    serializer_class = SalonOwnerRegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'Salon sahibi başarıyla kayıt oldu'
        }, status=status.HTTP_201_CREATED)

class SalonProfileUpdateView(generics.UpdateAPIView):
    """Salon profil güncelleme"""
    serializer_class = SalonProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Salon.objects.get(owner=self.request.user)

class SalonWorkingHoursUpdateView(generics.UpdateAPIView):
    """Salon çalışma saatleri güncelleme"""
    serializer_class = SalonWorkingHoursUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        salon = Salon.objects.get(owner=self.request.user)
        day_of_week = self.kwargs.get('day_of_week')
        working_hours, created = SalonWorkingHours.objects.get_or_create(
            salon=salon,
            day_of_week=day_of_week
        )
        return working_hours

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    RegisterSerializer, CustomerProfileUpdateSerializer, 
    CustomerLoyaltySerializer, PointHistorySerializer
)

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user_id': user.id,
                'username': user.username,
                'message': 'Kullanıcı başarıyla kayıt oldu'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                return Response({
                    'user_id': user.id,
                    'username': user.username,
                    'message': 'Giriş başarılı'
                })
            else:
                return Response({'error': 'Geçersiz kullanıcı adı veya şifre'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Kullanıcı adı ve şifre gerekli'}, status=status.HTTP_400_BAD_REQUEST)

class CustomerProfileUpdateView(generics.UpdateAPIView):
    """Müşteri profil güncelleme"""
    serializer_class = CustomerProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.customer_profile

class CustomerLoyaltyView(generics.RetrieveAPIView):
    """Müşteri sadakat bilgileri"""
    serializer_class = CustomerLoyaltySerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.customer_profile

class PointHistoryView(generics.ListAPIView):
    """Müşteri puan geçmişi"""
    serializer_class = PointHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.customer_profile.point_history.all()

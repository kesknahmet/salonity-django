from rest_framework import serializers
from .models import Salon, SalonEmployee, SalonWorkingHours
from services.models import Service, ServiceCategory
from django.contrib.auth.models import User

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'icon']

class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'image', 'category']

class SalonWorkingHoursSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SalonWorkingHours
        fields = ['day_of_week', 'day_name', 'opening_time', 'closing_time', 'is_closed']
    
    def get_day_name(self, obj):
        return dict(SalonWorkingHours.DAYS_OF_WEEK)[obj.day_of_week]

class SalonEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonEmployee
        fields = ['id', 'name', 'position', 'photo', 'bio']

class SalonListSerializer(serializers.ModelSerializer):
    """Salon listesi için kısa bilgiler"""
    salon_type_display = serializers.CharField(source='get_salon_type_display', read_only=True)
    
    class Meta:
        model = Salon
        fields = ['id', 'name', 'salon_type', 'salon_type_display', 'address', 'city', 'district', 
                 'rating', 'total_reviews', 'logo', 'is_verified']

class SalonDetailSerializer(serializers.ModelSerializer):
    """Salon detay bilgileri"""
    salon_type_display = serializers.CharField(source='get_salon_type_display', read_only=True)
    working_hours = SalonWorkingHoursSerializer(many=True, read_only=True)
    employees = SalonEmployeeSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Salon
        fields = ['id', 'name', 'salon_type', 'salon_type_display', 'description', 'address', 
                 'city', 'district', 'phone', 'email', 'website', 'opening_time', 'closing_time',
                 'rating', 'total_reviews', 'is_active', 'is_verified', 'logo', 'cover_image',
                 'instagram', 'facebook', 'working_hours', 'employees', 'services', 'created_at']

class SalonOwnerRegisterSerializer(serializers.ModelSerializer):
    """Salon sahibi kayıt"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)
    salon_name = serializers.CharField(required=True)
    salon_type = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'salon_name', 'salon_type')
    
    def create(self, validated_data):
        salon_name = validated_data.pop('salon_name')
        salon_type = validated_data.pop('salon_type')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Salon oluştur
        salon = Salon.objects.create(
            owner=user,
            name=salon_name,
            salon_type=salon_type,
            is_active=True
        )
        
        return user

class SalonProfileUpdateSerializer(serializers.ModelSerializer):
    """Salon profil güncelleme"""
    class Meta:
        model = Salon
        fields = ['name', 'description', 'address', 'city', 'district', 'phone', 'email', 
                 'website', 'opening_time', 'closing_time', 'logo', 'cover_image', 
                 'instagram', 'facebook']
        read_only_fields = ['owner', 'is_verified']

class SalonWorkingHoursUpdateSerializer(serializers.ModelSerializer):
    """Salon çalışma saatleri güncelleme"""
    class Meta:
        model = SalonWorkingHours
        fields = ['day_of_week', 'opening_time', 'closing_time', 'is_closed'] 
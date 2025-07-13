from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, PointHistory

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)
    phone = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    district = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone', 'birth_date', 'gender', 'address', 'city', 'district')

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        birth_date = validated_data.pop('birth_date', None)
        gender = validated_data.pop('gender', '')
        address = validated_data.pop('address', '')
        city = validated_data.pop('city', '')
        district = validated_data.pop('district', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Customer.objects.create(
            user=user,
            phone=phone,
            birth_date=birth_date,
            gender=gender,
            address=address,
            city=city,
            district=district
        )
        return user

class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """Müşteri profil güncelleme"""
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = Customer
        fields = ['phone', 'birth_date', 'gender', 'address', 'city', 'district', 
                 'profile_image', 'first_name', 'last_name', 'email']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        
        # User modelini güncelle
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        # Customer modelini güncelle
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class CustomerLoyaltySerializer(serializers.ModelSerializer):
    """Müşteri sadakat bilgileri"""
    loyalty_level_display = serializers.CharField(source='get_loyalty_level_display', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['loyalty_level', 'loyalty_level_display', 'total_points', 'current_points', 
                 'total_spent', 'total_visits']

class PointHistorySerializer(serializers.ModelSerializer):
    """Puan geçmişi"""
    class Meta:
        model = PointHistory
        fields = ['points', 'reason', 'created_at'] 
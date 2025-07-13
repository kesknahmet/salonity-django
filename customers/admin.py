from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'district', 'created_at']
    list_filter = ['city', 'district', 'gender', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Kullanıcı Bilgileri', {
            'fields': ('user',)
        }),
        ('Kişisel Bilgiler', {
            'fields': ('phone', 'birth_date', 'gender')
        }),
        ('Adres Bilgileri', {
            'fields': ('address', 'city', 'district')
        }),
        ('Profil', {
            'fields': ('profile_image',)
        }),
        ('Zaman Damgaları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

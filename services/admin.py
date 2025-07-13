from django.contrib import admin
from .models import ServiceCategory, Service, ServiceEmployee

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['icon']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'salon', 'category', 'price', 'duration', 'is_active']
    list_filter = ['salon', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'salon__name', 'category__name']
    list_editable = ['price', 'duration', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('salon', 'category', 'name', 'description')
        }),
        ('Fiyat ve Süre', {
            'fields': ('price', 'duration')
        }),
        ('Durum', {
            'fields': ('is_active',)
        }),
        ('Görsel', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Zaman Damgaları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ServiceEmployee)
class ServiceEmployeeAdmin(admin.ModelAdmin):
    list_display = ['service', 'employee', 'is_available']
    list_filter = ['service__salon', 'is_available']
    search_fields = ['service__name', 'employee__name']
    list_editable = ['is_available']

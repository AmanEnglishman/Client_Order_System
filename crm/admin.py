from django.contrib import admin

from .models import Client, Order


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('client__name', 'client__phone')
    ordering = ('-created_at',)

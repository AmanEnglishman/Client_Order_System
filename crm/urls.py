from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import ClientViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'orders', OrderViewSet)

from .views import (
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    add_interaction,
    update_order_status,
    export_clients_csv,
    export_orders_csv,
    dashboard,
    RegisterAPIView,
    LoginAPIView,
)

app_name = 'crm'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('', dashboard, name='dashboard'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/add/', ClientCreateView.as_view(), name='client-add'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client-edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('clients/<int:pk>/interactions/add/', add_interaction, name='add-interaction'),
    path('clients/export/csv/', export_clients_csv, name='export-clients-csv'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/add/', OrderCreateView.as_view(), name='order-add'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order-edit'),
    path('orders/<int:pk>/status/<str:status>/', update_order_status, name='order-status'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('orders/export/csv/', export_orders_csv, name='export-orders-csv'),
]

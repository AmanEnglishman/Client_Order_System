import csv

from django.contrib import messages

from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models.functions import TruncMonth

from .forms import ClientForm, OrderForm, InteractionForm, UserRegistrationForm
from .models import Client, Order, Interaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, AuthTokenResponseSerializer


class ClientListView(LoginRequiredMixin, ListView):
    """Display client list with search by name or phone."""
    model = Client
    template_name = 'crm/client_list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) | models.Q(phone__icontains=query)
            )
        sort_by = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class RegisterView(CreateView):
    """Create a new user account."""
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Show a customer profile with related orders and interactions."""
    model = Client
    template_name = 'crm/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.orders.filter(user=self.request.user).order_by('-created_at')
        context['interactions'] = self.object.interactions.filter(user=self.request.user)
        context['interaction_form'] = InteractionForm()
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Create a new client."""
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('crm:client-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Клиент успешно добавлен.')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing client."""
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('crm:client-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a client."""
    model = Client
    template_name = 'crm/client_confirm_delete.html'
    success_url = reverse_lazy('crm:client-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Show order details including client information."""
    model = Order
    template_name = 'crm/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderListView(LoginRequiredMixin, ListView):
    """Display order list with status filtering."""
    model = Order
    template_name = 'crm/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).select_related('client')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        sort_by = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        context['status_choices'] = Order.STATUS_CHOICES
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Create a new order."""
    model = Order
    form_class = OrderForm
    template_name = 'crm/order_form.html'
    success_url = reverse_lazy('crm:order-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['client'].queryset = Client.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Заказ успешно добавлен.')
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing order."""
    model = Order
    form_class = OrderForm
    template_name = 'crm/order_form.html'
    success_url = reverse_lazy('crm:order-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['client'].queryset = Client.objects.filter(user=self.request.user)
        return form


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an order."""
    model = Order
    template_name = 'crm/order_confirm_delete.html'
    success_url = reverse_lazy('crm:order-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@login_required
def add_interaction(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.user = request.user
            interaction.client = client
            interaction.save()
    return redirect('crm:client-detail', pk=pk)


@login_required
def update_order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    allowed_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
    if request.method == 'POST' and status in allowed_statuses:
        order.status = status
        order.save()
    return redirect(request.POST.get('next', 'crm:order-list'))


@login_required
def export_clients_csv(request):
    """Export user's clients to CSV."""

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Created At'])

    clients = Client.objects.filter(user=request.user)
    for client in clients:
        writer.writerow([
            client.id,
            client.name,
            client.phone,
            client.email or '',
            client.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


@login_required
def export_orders_csv(request):
    """Export user's orders to CSV."""

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Client', 'Total Price', 'Status', 'Created At'])

    orders = Order.objects.filter(user=request.user).select_related('client')
    for order in orders:
        writer.writerow([
            order.id,
            order.client.name,
            str(order.total_price),
            order.get_status_display(),
            order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


@login_required
def dashboard(request):
    """Show user dashboard with statistics."""
    # Statistics for the user
    total_clients = Client.objects.filter(user=request.user).count()
    total_orders = Order.objects.filter(user=request.user).count()
    total_revenue = Order.objects.filter(user=request.user).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Orders by status
    orders_by_status = Order.objects.filter(user=request.user).values('status').annotate(count=Count('status')).order_by('status')

    # Orders by month
    orders_by_month = Order.objects.filter(user=request.user).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id')).order_by('month')

    context = {
        'total_clients': total_clients,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'orders_by_status': orders_by_status,
        'orders_by_month': orders_by_month,
    }
    return render(request, 'crm/dashboard.html', context)


# API Views for Authentication
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses=AuthTokenResponseSerializer,
        description='Зарегистрировать нового пользователя и получить JWT-токены.',
        examples=[
            OpenApiExample(
                'Register request',
                summary='Request body for user registration',
                value={
                    'username': 'ivan',
                    'email': 'ivan@example.com',
                    'password': 'strong_password',
                    'password_confirm': 'strong_password',
                    'first_name': 'Ivan',
                    'last_name': 'Ivanov'
                },
                request_only=True,
            ),
            OpenApiExample(
                'Register response',
                summary='Successful registration response',
                value={
                    'user': {
                        'id': 1,
                        'username': 'ivan',
                        'email': 'ivan@example.com',
                        'first_name': 'Ivan',
                        'last_name': 'Ivanov'
                    },
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'message': 'Пользователь успешно зарегистрирован.'
                },
                response_only=True,
            ),
        ]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Пользователь успешно зарегистрирован.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses=AuthTokenResponseSerializer,
        description='Выполнить вход и получить JWT-токены.',
        examples=[
            OpenApiExample(
                'Login request',
                summary='Request body for login',
                value={
                    'username': 'ivan',
                    'password': 'strong_password'
                },
                request_only=True,
            ),
            OpenApiExample(
                'Login response',
                summary='Successful login response',
                value={
                    'user': {
                        'id': 1,
                        'username': 'ivan',
                        'email': 'ivan@example.com',
                        'first_name': 'Ivan',
                        'last_name': 'Ivanov'
                    },
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'message': 'Вход выполнен успешно.'
                },
                response_only=True,
            ),
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Вход выполнен успешно.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

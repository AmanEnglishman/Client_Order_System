from rest_framework import serializers
from .models import Client, Order, Interaction


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
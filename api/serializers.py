from rest_framework import serializers
from .models import *


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "cost", "image")


class AppointmentSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = (
            'id',
            'service',
            'customer',
            'status',
            'paid',
            'date1',
            'time1'
        )

    def get_service(self, obj):
        return obj.service.name

    def get_customer(self, obj):
        return obj.customer.user.username


class CustomerSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'id',
            'user',
            'status',
            'mobile',
            'id_card_no',
            'gender',
            'image'
        )

    def get_status(self, obj):
        return obj.get_status_display()

    def get_user(self, obj):
        return obj.user.username

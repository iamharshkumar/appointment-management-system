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
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'id',
            'first_name',
            'last_name',
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

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

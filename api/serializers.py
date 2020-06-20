from rest_framework import serializers
from .models import *


class AppointmentSerializer(serializers.ModelSerializer):
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

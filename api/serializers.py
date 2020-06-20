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

from rest_framework import serializers
from .models import *


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

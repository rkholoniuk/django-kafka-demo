from rest_framework import serializers
from .models import Stamp


class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['object_cid', 'time_tolerance', 'created_date']

    def create(self, validated_data):
        print(validated_data)
        return Stamp.objects.create(**validated_data)

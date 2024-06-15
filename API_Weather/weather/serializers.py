from rest_framework import serializers
from .models import WeatherEntity

class WeatherSerializer(serializers.Serializer):
    id = serializers.CharField(allow_blank = True, required=False)
    temperature = serializers.FloatField()
    date = serializers.DateTimeField()
    city = serializers.CharField(required=False)
    atmosphericPressure = serializers.CharField(required=False)
    humidity = serializers.CharField(required=False)
    weather = serializers.CharField(required=False)

    def create(self, validated_data):
        return WeatherEntity(**validated_data)

    def update(self, instance, validated_data):
        instance.temperature = validated_data.get('temperature', instance.temperature)
        instance.date = validated_data.get('date', instance.date)
        instance.city = validated_data.get('city', instance.city)
        instance.atmosphericPressure = validated_data.get('atmosphericPressure', instance.atmosphericPressure)
        instance.humidity = validated_data.get('humidity', instance.humidity)
        instance.weather = validated_data.get('weather', instance.weather)
        return instance

from rest_framework import serializers
from .models import AboutUs


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'

    def update(self, instance, validated_data):
        # Only update fields provided in the validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

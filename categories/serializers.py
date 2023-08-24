from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    kind = serializers.ChoiceField(choices=Category.CategoryKingChoices.choices)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance

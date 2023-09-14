from rest_framework import serializers
from .models import Perk, Experience
from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from wishlists.models import Wishlist


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        return Wishlist.objects.filter(
            user=request.user,
            experiences__pk=experience.pk,
        ).exists()


class ExperienceListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_host",
            "photos",
        )

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

from django.conf import settings
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework import permissions
from .models import Perk, Experience
from . import serializers
from categories.models import Category


class Experiences(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            all_experiences,
            many=True,
            context={"request": request},
        )
        return Response(data=serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise exceptions.ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise exceptions.ParseError(
                        "The category kind should be experiences"
                    )
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category does not exist")
            try:
                with transaction.atomic():
                    new_experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        new_experience.perks.add(perk)
                    serializer = serializers.ExperienceDetailSerializer(
                        new_experience,
                        context={"request": request},
                    )
                    return Response(data=serializer.data)
            except Perk.DoesNotExist:
                raise exceptions.ParseError("Perks not found")
            except Exception as e:
                raise exceptions.ParseError(e)
        else:
            return Response(data=serializer.errors)


class ExperienceDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise exceptions.ParseError(
                            "The category kind should be experiences"
                        )
                except Category.DoesNotExist:
                    raise exceptions.ParseError("Category does not exist")
            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(
                            category=category,
                        )
                    else:
                        experience = serializer.save()
                    perks = request.data.get("perks")
                    if perks:
                        experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)
                    serializer = serializers.ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    )
                    return Response(data=serializer.data)
            except Perk.DoesNotExist:
                raise exceptions.ParseError("Perks not found")
            except Exception as e:
                raise exceptions.ParseError(e)
        else:
            return Response(data=serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(data=serializers.PerkSerializer(perk).data)
        else:
            return Response(data=serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(data=serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(data=serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(data=serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

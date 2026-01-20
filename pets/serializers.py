from rest_framework import serializers
from .models import Pets

class PetsSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Pets
        fields = [
            "id",
            "name",
            "species",
            "gender",
            "breed",
            "pet_chip",
            "birth_date",
            "features",
            "remark",
            "is_neutered",
            "is_deceased",
            "avatar_url",
            "owner_username",
            "created_at",
            "updated_at",
        ]

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if not obj.avatar:
            return None
        if request:
            return request.build_absolute_uri(obj.avatar.url)
        return obj.avatar.url

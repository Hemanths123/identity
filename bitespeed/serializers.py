from rest_framework import serializers
from .models import Identity, ContactIdentifier


class IdentifyRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    phoneNumber = serializers.CharField(required=False, allow_blank=True)


class ContactIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactIdentifier
        fields = ["type", "value"]


class IdentitySerializer(serializers.ModelSerializer):
    identifiers = ContactIdentifierSerializer(many=True)

    class Meta:
        model = Identity
        fields = ["id", "is_primary", "identifiers"]

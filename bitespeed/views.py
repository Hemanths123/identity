from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Identity, ContactIdentifier
from .serializers import IdentifyRequestSerializer, IdentitySerializer


@api_view(["POST"])
def identify(request):
    serializer = IdentifyRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email")
    phone = serializer.validated_data.get("phoneNumber")

    if not email and not phone:
        return Response({"error": "Email or phoneNumber required"}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        matching_identities = set()

        if email:
            email_contact = ContactIdentifier.objects.filter(type=ContactIdentifier.EMAIL, value=email).first()
            if email_contact:
                matching_identities.add(email_contact.identity)

        if phone:
            phone_contact = ContactIdentifier.objects.filter(type=ContactIdentifier.PHONE, value=phone).first()
            if phone_contact:
                matching_identities.add(phone_contact.identity)

        if not matching_identities:
            new_identity = Identity.objects.create(is_primary=True)
            if email:
                ContactIdentifier.objects.create(identity=new_identity, type=ContactIdentifier.EMAIL, value=email)
            if phone:
                ContactIdentifier.objects.create(identity=new_identity, type=ContactIdentifier.PHONE, value=phone)
            return Response(IdentitySerializer(new_identity).data)

        primary_identity = sorted(list(matching_identities), key=lambda i: i.id)[0]
        for other_identity in matching_identities:
            if other_identity != primary_identity:
                ContactIdentifier.objects.filter(identity=other_identity).update(identity=primary_identity)
                other_identity.is_primary = False
                other_identity.save()

        if email and not ContactIdentifier.objects.filter(identity=primary_identity, type=ContactIdentifier.EMAIL, value=email).exists():
            ContactIdentifier.objects.create(identity=primary_identity, type=ContactIdentifier.EMAIL, value=email)
        if phone and not ContactIdentifier.objects.filter(identity=primary_identity, type=ContactIdentifier.PHONE, value=phone).exists():
            ContactIdentifier.objects.create(identity=primary_identity, type=ContactIdentifier.PHONE, value=phone)

        return Response(IdentitySerializer(primary_identity).data)

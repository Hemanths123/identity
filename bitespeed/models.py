from django.db import models


class Identity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=True)  

    def __str__(self):
        return f"Identity {self.id} (Primary: {self.is_primary})"


class ContactIdentifier(models.Model):
    EMAIL = 'email'
    PHONE = 'phone'
    IDENTIFIER_TYPES = [(EMAIL, 'Email'), (PHONE, 'Phone')]
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name="identifiers")
    type = models.CharField(max_length=10, choices=IDENTIFIER_TYPES)
    value = models.CharField(max_length=255, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.value} (Identity {self.identity_id})"

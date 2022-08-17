from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import ModelSerializer

from .models import User


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]

        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        user = self.Meta.model(**validated_data)
        if password is not None:
            try:
                validate_password(user=user, password=password)
            except DjangoValidationError as error:
                raise ValidationError({"password": error.messages})
            user.set_password(password)
            user.save()
        return user

from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'username', 'email', 'password','is_staff']
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'min_length': 3},
                        'email': {'required': True},
                    }
        
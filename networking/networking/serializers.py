# serializers.py
from rest_framework import serializers
# from api.models import User

# class UserSignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password')

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             username=validated_data['username'],
#             password=validated_data['password']
#         )
#         return user

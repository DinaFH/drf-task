from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'type',  'gender', 'date_of_birth']
        depth = 1


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'type', 'gender', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True},
        }



    def save(self, **kwargs):
        user = User(
            username=self.validated_data.get('username'),
            email=self.validated_data.get('email'),
            password=self.validated_data.get('password'),
            type=self.validated_data.get('type'),
            gender=self.validated_data.get('gender'),
            date_of_birth=self.validated_data.get('date_of_birth'),

        )
        if self.validated_data.get('password') != self.validated_data.get('password_confirm'):
            raise serializers.ValidationError({'detail': 'passwords did not match'})
        user.set_password(self.validated_data.get('password'))
        user.save()
        return user

class AddEmployeeSerializer(serializers.ModelSerializer):
        type = serializers.ReadOnlyField(default='employee')
        class Meta:
            model = User
            fields = '__all__'

class AddClientSerializer(serializers.ModelSerializer):
        type = serializers.ReadOnlyField(default='client')
        class Meta:
            model = User
            fields = '__all__'
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['old_password','new_password']
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


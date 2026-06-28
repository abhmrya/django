from rest_framework import serializers
from .models import MyUser,Student,Staff,StudentRegistr,MyUser
from django.contrib.auth import authenticate



class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['userid', 'email', 'name', 'phonenumber', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data, role='admin')


class StaffRegistrationSerializer(serializers.ModelSerializer):
    department = serializers.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ['userid', 'email', 'name', 'phonenumber', 'password', 'department']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        department = validated_data.pop('department')
        user = MyUser.objects.create_user(**validated_data, role='staff')
        Staff.objects.create(user=user, department=department)
        return user


class StudentRegistrationSerializer(serializers.ModelSerializer):
    roll_no = serializers.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ['userid', 'email', 'name', 'phonenumber', 'password', 'roll_no']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        roll_no = validated_data.pop('roll_no')
        user = MyUser.objects.create_user(**validated_data, role='student')
        Student.objects.create(user=user, roll_no=roll_no)
        return user



# from django.contrib.auth import authenticate
# from rest_framework import serializers
# from rest_framework.exceptions import AuthenticationFailed
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')

#         user = authenticate(request=self.context.get('request'), email=email, password=password)

#         if not user:
#             raise AuthenticationFailed("Invalid credentials")
#         if not user.is_active:
#             raise AuthenticationFailed("User is inactive")

#         data['user'] = user
#         return data

from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])  # ✅ key point
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        return {"user": user}

class studentformserializer(serializers.ModelSerializer):
    class Meta:
        model=StudentRegistr
        fields="__all__"
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegistr
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegistr
        fields = ['name', 'age', 'student_class', 'address', 'phone', 'email']

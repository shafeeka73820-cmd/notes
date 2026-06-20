from rest_framework import serializers
from .models import Student, Department, Course, Profile, Document
from django.contrib.auth.models import User
import re


class StudentSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'email', 'branch', 'marks',
                  'phone', 'photo', 'department', 'department_name',
                  'is_active', 'joined', 'grade']
        read_only_fields = ['id', 'joined']

    def validate_marks(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Marks must be between 0 and 100.")
        return value

    def validate_name(self, value):
        if any(ch.isdigit() for ch in value):
            raise serializers.ValidationError("Name cannot contain numbers.")
        return value

    def validate_phone(self, value):
        if value and not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number (9-15 digits).")
        return value

    def validate(self, data):
        name = data.get('name')
        email = data.get('email')
        if name and email and name.lower() not in email.lower():
            raise serializers.ValidationError(
                "Email should contain the student's name for consistency."
            )
        return data


class StudentListSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'branch', 'marks', 'grade', 'is_active']


class DepartmentSerializer(serializers.ModelSerializer):
    students = serializers.HyperlinkedRelatedField(
        many=True, read_only=True,
        view_name='student-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'image_url', 'students']

    def validate_code(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError("Code must be at least 2 characters.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'credits', 'students']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'phone', 'role', 'bio']


class DocumentSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(read_only=True)
    size_display = serializers.CharField(read_only=True)
    uploaded_by_name = serializers.CharField(
        source='uploaded_by.username', read_only=True
    )

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'category', 'uploaded_by',
                  'uploaded_by_name', 'student', 'uploaded_at',
                  'file_size', 'size_display', 'description', 'filename']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'file_size']

    def validate_file(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size must be under 10 MB.")
            ext = value.name.split('.')[-1].lower()
            allowed = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'zip']
            if ext not in allowed:
                raise serializers.ValidationError(f"Allowed types: {', '.join(allowed)}")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if value and len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters.")
        if value and not value.isalnum():
            raise serializers.ValidationError("Username can only contain letters and numbers.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        if value and not value.endswith('@campus.com'):
            raise serializers.ValidationError("Only @campus.com email addresses are allowed.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Profile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class FeedbackSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=3)
    email = serializers.EmailField()
    message = serializers.CharField(min_length=10, max_length=500)
    rating = serializers.ChoiceField(choices=[1, 2, 3, 4, 5])

    def validate_message(self, value):
        if 'spam' in value.lower():
            raise serializers.ValidationError("Inappropriate content detected.")
        return value

    def validate_rating(self, value):
        if int(value) < 3:
            name = self.initial_data.get('name', 'User')
            raise serializers.ValidationError(
                f"Sorry to hear that, {name}! Please tell us how we can improve."
            )
        return value

    def validate(self, data):
        name = data.get('name')
        email = data.get('email')
        if name and email and name.lower() not in email.lower():
            raise serializers.ValidationError("Email should contain your name for consistency.")
        return data

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Job, Application


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, role=role)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'role', 'phone', 'resume']


class JobSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(source='recruiter.username', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'jtype', 'description',
                  'salary_min', 'salary_max', 'recruiter', 'recruiter_name',
                  'created', 'active']
        read_only_fields = ['id', 'recruiter', 'created']


class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'jtype',
                  'salary_min', 'salary_max', 'created']


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.username', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'candidate', 'candidate_name',
                  'resume', 'cover_note', 'status', 'applied_at']
        read_only_fields = ['id', 'candidate', 'status', 'applied_at']

    def validate_resume(self, value):
        if value:
            ext = value.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise serializers.ValidationError("Only PDF, DOC, DOCX allowed.")
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("File must be under 5 MB.")
        return value


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']

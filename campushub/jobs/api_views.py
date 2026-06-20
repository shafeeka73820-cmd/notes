from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from django.shortcuts import get_object_or_404
from .models import Profile, Job, Application
from .serializers import (
    RegisterSerializer, UserSerializer, ProfileSerializer,
    JobSerializer, JobListSerializer, ApplicationSerializer,
    ApplicationStatusSerializer
)
from .permissions import IsRecruiter, IsCandidate


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class JobFilter(FilterSet):
    location = CharFilter(field_name='location', lookup_expr='icontains')
    jtype = CharFilter(field_name='jtype', lookup_expr='iexact')

    class Meta:
        model = Job
        fields = ['location', 'jtype', 'active']


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'company', 'description']
    ordering_fields = ['created', 'salary_min', 'salary_max']
    ordering = ['-created']
    throttle_scope = 'apply'

    def get_throttles(self):
        if self.action == 'apply':
            return [ScopedRateThrottle()]
        return super().get_throttles()

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsRecruiter()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and self.action == 'list':
            if hasattr(user, 'job_profile') and user.job_profile.role == 'R':
                return Job.objects.filter(recruiter=user).select_related('recruiter')
        return Job.objects.filter(active=True).select_related('recruiter')

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsCandidate])
    def apply(self, request, pk=None):
        job = self.get_object()
        if not job.active:
            return Response({'detail': 'This job is no longer accepting applications.'}, status=400)
        if Application.objects.filter(job=job, candidate=request.user).exists():
            return Response({'detail': 'Already applied.'}, status=status.HTTP_400_BAD_REQUEST)
        ser = ApplicationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(job=job, candidate=request.user)
        return Response(ser.data, status=status.HTTP_201_CREATED)


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'job_profile') and user.job_profile.role == 'R':
            return Application.objects.filter(job__recruiter=user).select_related('job', 'candidate')
        return Application.objects.filter(candidate=user).select_related('job', 'candidate')

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsRecruiter])
    def set_status(self, request, pk=None):
        app = self.get_object()
        ser = ApplicationStatusSerializer(app, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ApplicationSerializer(app).data)

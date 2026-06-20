from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth import authenticate
from django.db.models import Avg, Max, Min, Count, F, Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student, Department, Course, Profile, Document
from .filters import StudentFilter
from .permissions import IsOwnerOrReadOnly, IsAdminRole
from .serializers import (
    StudentSerializer, StudentListSerializer,
    DepartmentSerializer, CourseSerializer,
    ProfileSerializer, DocumentSerializer,
    UserSerializer, RegisterSerializer,
    LoginSerializer, FeedbackSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('department').prefetch_related('courses')
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    search_fields = ['name', 'email', 'department__name']
    ordering_fields = ['marks', 'roll', 'name']
    ordering = ['-marks']

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAdminUser()]
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def promote(self, request, pk=None):
        student = self.get_object()
        student.marks = F('marks') + 5
        student.save(update_fields=['marks'])
        student.refresh_from_db()
        return Response(StudentSerializer(student).data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        agg = Student.objects.aggregate(
            avg_marks=Avg('marks'), top=Max('marks'),
            bottom=Min('marks'), total=Count('id')
        )
        dept_stats = Department.objects.annotate(
            strength=Count('students'), avg_marks=Avg('students__marks')
        ).values('name', 'strength', 'avg_marks')
        toppers = StudentListSerializer(
            Student.objects.order_by('-marks')[:3], many=True
        ).data
        return Response({'aggregates': agg, 'departments': dept_stats, 'toppers': toppers})

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        students = Student.objects.filter(name__icontains=query) if query else []
        return Response(StudentListSerializer(students, many=True).data)

    @action(detail=False, methods=['post'])
    def bulk(self, request):
        action_type = request.data.get('action')
        student_ids = request.data.get('student_ids', [])
        qs = Student.objects.filter(id__in=student_ids)
        if action_type == 'bonus':
            count = qs.update(marks=F('marks') + 5)
        elif action_type == 'deactivate':
            toppers = qs.filter(Q(marks__gte=90))
            others = qs.exclude(id__in=toppers.values('id'))
            count = others.update(is_active=False)
        elif action_type == 'reset':
            count = qs.update(marks=0)
        else:
            return Response({'error': 'Invalid action'}, status=400)
        return Response({'affected': count})


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.annotate(
        strength=Count('students', distinct=True),
        avg_marks=Avg('students__marks')
    )
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(
        student_count=Count('students', distinct=True),
        avg_marks=Avg('students__marks')
    )
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            return Response(ProfileSerializer(profile).data)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('uploaded_by', 'student')
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'login'
    queryset = None

    def get_throttles(self):
        if self.action == 'login':
            return [ScopedRateThrottle()]
        return super().get_throttles()

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=LoginSerializer)
    def login(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = authenticate(
            username=ser.validated_data['username'],
            password=ser.validated_data['password']
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def feedback(self, request):
        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': f"Thanks {serializer.validated_data['name']}! We received your feedback."})

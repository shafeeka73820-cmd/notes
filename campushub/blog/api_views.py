from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import ScopedRateThrottle
from django.shortcuts import get_object_or_404
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, PostListSerializer, CommentSerializer
from students.permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['created', 'title']
    ordering = ['-created']

    def get_queryset(self):
        qs = Post.objects.select_related('author', 'category').prefetch_related('comments')
        user = self.request.user
        if self.action == 'list' and not (user.is_authenticated and user.is_staff):
            return qs.filter(status='P')
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, slug=None):
        post = self.get_object()
        if request.method == 'GET':
            comments = post.comments.all()
            return Response(CommentSerializer(comments, many=True).data)
        ser = CommentSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save(post=post, author=request.user)
        return Response(ser.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    throttle_scope = 'comments'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_throttles(self):
        if self.action == 'create':
            return [ScopedRateThrottle()]
        return super().get_throttles()

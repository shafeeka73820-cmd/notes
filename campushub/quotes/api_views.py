from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Quote
from .serializers import QuoteSerializer


class QuoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quote.objects.select_related('category')
    serializer_class = QuoteSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['text', 'author', 'source']
    ordering_fields = ['author']
    filterset_fields = ['category', 'is_famous']

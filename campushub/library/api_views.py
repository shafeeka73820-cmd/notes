from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book, Member, Issue
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, IssueSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'isbn', 'author__name']
    ordering_fields = ['title', 'published_year']
    filterset_fields = ['is_available', 'author']

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def issue(self, request, pk=None):
        book = self.get_object()
        if not book.is_available:
            return Response({'detail': 'No copies available.'},
                            status=status.HTTP_400_BAD_REQUEST)
        ser = IssueSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(book=book)
        book.copies_available = F('copies_available') - 1
        book.save(update_fields=['copies_available'])
        return Response(ser.data, status=status.HTTP_201_CREATED)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related('user')
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ['user__username', 'phone']
    ordering_fields = ['joined_date']


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.select_related('book', 'member__user')
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-issue_date']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(member__user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def return_book(self, request, pk=None):
        issue = self.get_object()
        if issue.returned:
            return Response({'detail': 'Already returned.'}, status=400)
        issue.returned = True
        from datetime import date
        issue.returned_date = date.today()
        issue.save()
        book = issue.book
        book.copies_available = F('copies_available') + 1
        book.save(update_fields=['copies_available'])
        return Response(IssueSerializer(issue).data)

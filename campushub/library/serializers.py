from rest_framework import serializers
from .models import Author, Book, Member, Issue


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'born']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'author', 'author_name',
                  'publisher', 'published_year', 'total_copies',
                  'copies_available', 'is_available']


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'username', 'phone', 'address', 'joined_date']


class IssueSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_name = serializers.CharField(source='member.user.username', read_only=True)
    fine = serializers.ReadOnlyField()

    class Meta:
        model = Issue
        fields = ['id', 'book', 'book_title', 'member', 'member_name',
                  'issue_date', 'due_date', 'returned', 'returned_date', 'fine']
        read_only_fields = ['id', 'issue_date', 'returned', 'returned_date', 'fine']

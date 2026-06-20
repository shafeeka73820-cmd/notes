from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    born = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.CharField(max_length=100, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    total_copies = models.IntegerField(default=1)
    copies_available = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    def save(self, *args, **kwargs):
        self.is_available = self.copies_available > 0
        super().save(*args, **kwargs)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='library_member')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return self.user.username


class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issues')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    returned_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-issue_date']
        verbose_name_plural = 'issues'

    def __str__(self):
        return f"{self.book.title} -> {self.member.user.username}"

    @property
    def fine(self):
        if self.returned:
            return 0
        from datetime import date
        overdue = (date.today() - self.due_date).days
        return max(0, overdue * 5)

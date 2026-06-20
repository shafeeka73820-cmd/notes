from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, default='')
    image_url = models.URLField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=80)
    code = models.CharField(max_length=10, unique=True)
    credits = models.IntegerField(default=3)
    students = models.ManyToManyField('Student', related_name='courses', blank=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} – {self.title}"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('S', 'Student'),
        ('T', 'Teacher'),
        ('A', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='S')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Student(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics'),
        ('EEE', 'Electrical'),
        ('ME', 'Mechanical'),
        ('CE', 'Civil'),
    ]

    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    marks = models.IntegerField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    joined = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='students'
    )
    attendance = models.IntegerField(default=75, help_text="Attendance percentage (0-100)")
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_students'
    )

    class Meta:
        ordering = ['roll']

    def __str__(self):
        return f"{self.name} ({self.roll})"

    def get_absolute_url(self):
        return reverse('students:detail', args=[self.roll])

    def grade(self):
        if self.marks >= 75:
            return 'A'
        elif self.marks >= 60:
            return 'B'
        elif self.marks >= 40:
            return 'C'
        return 'F'


def document_upload_path(instance, filename):
    from datetime import datetime
    return f'documents/{datetime.now().strftime("%Y/%m/%d")}/{filename}'


class Document(models.Model):
    CATEGORY_CHOICES = [
        ('assignment', 'Assignment'),
        ('notes', 'Notes'),
        ('report', 'Report'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=document_upload_path)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(editable=False, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            try:
                self.file_size = self.file.size
            except:
                pass
        super().save(*args, **kwargs)

    def filename(self):
        import os
        return os.path.basename(self.file.name) if self.file else ''

    def size_display(self):
        if not self.file_size:
            return 'Unknown'
        size = self.file_size
        if size < 1024:
            return f'{size} B'
        elif size < 1024 * 1024:
            return f'{size / 1024:.1f} KB'
        else:
            return f'{size / (1024 * 1024):.1f} MB'

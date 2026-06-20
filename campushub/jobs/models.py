from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('C', 'Candidate'),
        ('R', 'Recruiter'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_profile')
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Job(models.Model):
    JTYPE_CHOICES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('IN', 'Internship'),
        ('CT', 'Contract'),
    ]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    jtype = models.CharField(max_length=2, choices=JTYPE_CHOICES, default='FT')
    description = models.TextField()
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.title} at {self.company}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Shortlisted'),
        ('R', 'Rejected'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='applications/resumes/')
    cover_note = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['job', 'candidate']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.candidate.username} -> {self.job.title}"

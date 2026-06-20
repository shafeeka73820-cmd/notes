from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Department, Course, Profile, Document
import re


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll', 'email', 'branch', 'marks', 'attendance', 'total_fees', 'paid_fees', 'phone', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'attendance': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'paid_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None and (marks < 0 or marks > 100):
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name and any(ch.isdigit() for ch in name):
            raise forms.ValidationError("Name cannot contain numbers.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise forms.ValidationError("Enter a valid phone number (9-15 digits).")
        return phone

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get('name')
        email = cleaned.get('email')
        if name and email and name.lower() not in email.lower():
            raise forms.ValidationError("Email should contain the student's name for consistency.")
        return cleaned


class AdminStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
            if marks < 0 or marks > 100:
                raise forms.ValidationError("Marks must be between 0 and 100.")
            if marks > 90 and not self.cleaned_data.get('is_active'):
                raise forms.ValidationError("A student with 90+ marks cannot be set as inactive.")
        return marks

    def clean_roll(self):
        roll = self.cleaned_data.get('roll')
        qs = Student.objects.filter(roll=roll)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This roll number is already taken.")
        return roll

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@campus.com'):
            raise forms.ValidationError("Only @campus.com email addresses are allowed.")
        return email

    def clean(self):
        cleaned = super().clean()
        marks = cleaned.get('marks')
        branch = cleaned.get('branch')
        if marks and branch and marks >= 85 and branch == 'ECE':
            raise forms.ValidationError("ECE branch students cannot have marks >= 85 per department policy.")
        return cleaned


class AdminDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def clean_code(self):
        code = self.cleaned_data.get('code', '')
        if code and len(code) < 2:
            raise forms.ValidationError("Code must be at least 2 characters.")
        return code

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name and len(name) < 3:
            raise forms.ValidationError("Department name must be at least 3 characters.")
        return name


class AdminCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits is not None and (credits < 1 or credits > 10):
            raise forms.ValidationError("Credits must be between 1 and 10.")
        return credits

    def clean_code(self):
        code = self.cleaned_data.get('code', '')
        if code and not re.match(r'^[A-Z]{2,4}\d{3}$', code):
            raise forms.ValidationError("Code must be like CS101 or ECE201 (2-4 letters + 3 digits).")
        return code


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    rating = forms.ChoiceField(
        choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name and len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters.")
        return name

    def clean_message(self):
        msg = self.cleaned_data.get('message', '')
        if msg and len(msg) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        if msg and len(msg) > 500:
            raise forms.ValidationError("Message must not exceed 500 characters.")
        if msg and 'spam' in msg.lower():
            raise forms.ValidationError("Inappropriate content detected.")
        return msg

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and int(rating) < 3:
            name = self.cleaned_data.get('name', 'User')
            raise forms.ValidationError(
                f"Sorry to hear that, {name}! Please tell us how we can improve."
            )
        return rating

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get('name', '')
        email = cleaned.get('email', '')
        if name and email and name.lower() not in email.lower():
            raise forms.ValidationError("Email should contain your name for consistency.")
        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'role', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'category', 'student', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10 MB.")
            ext = file.name.split('.')[-1].lower()
            allowed = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'zip']
            if ext not in allowed:
                raise forms.ValidationError(f"Allowed types: {', '.join(allowed)}")
        return file


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if username and len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters.")
        if username and not username.isalnum():
            raise forms.ValidationError("Username can only contain letters and numbers.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        if email and not email.endswith('@campus.com'):
            raise forms.ValidationError("Only @campus.com email addresses are allowed.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        if p1 and len(p1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        return cleaned

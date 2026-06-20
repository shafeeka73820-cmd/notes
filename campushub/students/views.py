from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Avg, Max, Min, Count, F, Q
from .models import Student, Department, Course, Profile, Document
from .forms import StudentForm, FeedbackForm, RegisterForm, AdminDepartmentForm, AdminCourseForm, ProfileForm, DocumentForm

def index(request):
    students = Student.objects.all()
    departments = Department.objects.annotate(
        strength=Count('students', distinct=True),
        avg_marks=Avg('students__marks'),
    )
    toppers = students.order_by('-marks')[:5]
    branch_data = students.values('branch').annotate(count=Count('id')).order_by('branch')
    grade_a = students.filter(marks__gte=75).count()
    grade_b = students.filter(marks__gte=60, marks__lt=75).count()
    grade_c = students.filter(marks__gte=40, marks__lt=60).count()
    grade_f = students.filter(marks__lt=40).count()
    attendance_high = students.filter(attendance__gte=85).count()
    attendance_mid = students.filter(attendance__gte=75, attendance__lt=85).count()
    attendance_low = students.filter(attendance__lt=75).count()
    context = {
        "students": students,
        "count": len(students),
        "dept_count": Department.objects.count(),
        "departments": departments,
        "toppers": toppers,
        "top_student": students.order_by('-marks').first(),
        "avg_attendance": students.aggregate(Avg('attendance'))['attendance__avg'] or 0,
        "attendance_high": attendance_high,
        "attendance_mid": attendance_mid,
        "attendance_low": attendance_low,
        "branch_data": branch_data,
        "grade_a": grade_a,
        "grade_b": grade_b,
        "grade_c": grade_c,
        "grade_f": grade_f,
        "title": "Student Portal",
    }
    return render(request, 'students/index.html', context)

def departments(request):
    depts = Department.objects.annotate(
        strength=Count('students', distinct=True),
        avg_marks=Avg('students__marks'),
    )
    return render(request, 'students/departments.html', {"departments": depts})

def department_detail(request, code):
    dept = get_object_or_404(Department.objects.annotate(
        strength=Count('students', distinct=True),
        avg_marks=Avg('students__marks'),
    ), code=code.upper())
    students = dept.students.all().order_by('-marks')[:10]
    return render(request, 'students/department_detail.html', {
        "dept": dept,
        "students": students,
    })

def detail(request, roll):
    student = get_object_or_404(Student, roll=roll)
    return render(request, 'students/detail.html', {"student": student})

def placements(request):
    companies = ["TCS", "Cognizant", "Infosys", "Capgemini", "Altimetrik", "Mphasis",
                 "Tech Mahindra", "Wipro", "Hexaware", "Mind Tree", "SecureW2", "Planet Spark"]
    context = {
        "title": "Placements | MTIET",
        "companies": companies,
    }
    return render(request, 'students/placements.html', context)

def gallery(request):
    context = {
        "title": "Gallery | MTIET",
    }
    return render(request, 'students/gallery.html', context)

def contact(request):
    return render(request, 'students/contact.html', {"title": "Contact | MTIET"})

def about(request):
    import django
    ver = ".".join(str(v) for v in django.VERSION[:3])
    return render(request, 'students/about.html', {
        "title": "About CampusHub",
        "django_version": ver,
    })

def stats(request):
    agg = Student.objects.aggregate(
        avg_marks=Avg('marks'), top=Max('marks'),
        bottom=Min('marks'), total=Count('id')
    )
    dept_stats = Department.objects.annotate(
        strength=Count('students'), avg_marks=Avg('students__marks')
    )
    toppers = Student.objects.order_by('-marks')[:3]
    course_counts = Course.objects.annotate(student_count=Count('students'))
    return render(request, 'students/stats.html', {
        "agg": agg, "dept_stats": dept_stats,
        "toppers": toppers, "course_counts": course_counts,
    })

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Student.objects.filter(name__icontains=query)
    return render(request, 'students/search.html', {"query": query, "results": results})

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data['message']
            return HttpResponse(f"Thanks! We received: {msg}")
    else:
        form = FeedbackForm()
    return render(request, 'students/feedback.html', {"form": form})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            return redirect('students:detail', roll=student.roll)
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {"form": form, "title": "Add Student"})

@login_required
def edit_student(request, roll):
    student = get_object_or_404(Student, roll=roll)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:detail', roll=student.roll)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {"form": form, "title": "Edit Student"})

def portal(request):
    students = Student.objects.all().select_related('department').prefetch_related('courses')
    agg = Student.objects.aggregate(
        avg_marks=Avg('marks'), top=Max('marks'),
        bottom=Min('marks'), total=Count('id')
    )
    dept_stats = Department.objects.annotate(
        strength=Count('students'), avg_marks=Avg('students__marks')
    )
    course_counts = Course.objects.annotate(student_count=Count('students'))

    student_form = StudentForm()
    feedback_form = FeedbackForm()

    if request.method == 'POST':
        if 'add_student' in request.POST:
            student_form = StudentForm(request.POST, request.FILES)
            if student_form.is_valid():
                s = student_form.save()
                return redirect('students:portal')
        elif 'feedback' in request.POST:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                return HttpResponse(f"Thanks! We received your feedback.")

    return render(request, 'students/portal.html', {
        'students': students,
        'agg': agg,
        'dept_stats': dept_stats,
        'course_counts': course_counts,
        'student_form': student_form,
        'feedback_form': feedback_form,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('students:index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {"form": form})


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'registration/profile.html', {
        'profile': profile,
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('students:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'registration/profile_edit.html', {'form': form})


@login_required
def delete_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        doc.delete()
        messages.success(request, 'Document deleted.')
        return redirect('students:admin_dashboard')
    return render(request, 'students/document_confirm_delete.html', {'doc': doc})


@login_required
def admin_dashboard(request):
    dept_form = AdminDepartmentForm()
    course_form = AdminCourseForm()
    student_form = StudentForm()
    document_form = DocumentForm()
    documents = Document.objects.all().select_related('uploaded_by', 'student')
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=profile)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'add_department' in request.POST:
            dept_form = AdminDepartmentForm(request.POST)
            if dept_form.is_valid():
                dept_form.save()
                messages.success(request, 'Department added successfully.')
                return redirect('students:admin_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'add_course' in request.POST:
            course_form = AdminCourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                messages.success(request, 'Course added successfully.')
                return redirect('students:admin_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'add_student' in request.POST:
            student_form = StudentForm(request.POST, request.FILES)
            if student_form.is_valid():
                student_form.save()
                messages.success(request, 'Student added successfully.')
                return redirect('students:admin_dashboard')
            else:
                messages.error(request, 'Please correct student errors.')

        elif 'upload_document' in request.POST:
            document_form = DocumentForm(request.POST, request.FILES)
            if document_form.is_valid():
                doc = document_form.save(commit=False)
                doc.uploaded_by = request.user
                doc.save()
                messages.success(request, 'Document uploaded successfully.')
                return redirect('students:admin_dashboard')
            else:
                messages.error(request, 'Please correct document errors.')

        elif 'bulk_action' in request.POST:
            action = request.POST.get('action')
            student_ids = request.POST.getlist('selected_students')
            queryset = Student.objects.filter(id__in=student_ids)
            if action == 'bonus':
                count = queryset.update(marks=F('marks') + 5)
                messages.success(request, f'{count} student(s) received +5 bonus marks.')
            elif action == 'deactivate':
                toppers = queryset.filter(Q(marks__gte=90))
                others = queryset.exclude(id__in=toppers.values('id'))
                count = others.update(is_active=False)
                messages.warning(request, f'{count} student(s) deactivated (toppers preserved).')
            elif action == 'reset':
                count = queryset.update(marks=0)
                messages.error(request, f'{count} student(s) marks reset to 0.')
            return redirect('students:admin_dashboard')

        elif 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated.')
            else:
                messages.error(request, 'Please correct profile errors.')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed.')
            else:
                messages.error(request, 'Please correct password errors.')

    students = Student.objects.all().select_related('department').prefetch_related('courses')
    departments = Department.objects.annotate(
        strength=Count('students', distinct=True),
        avg_marks=Avg('students__marks'),
    ).prefetch_related('students')
    for d in departments:
        top = d.students.order_by('-marks').first()
        d.top_student_name = top.name if top else '-'
        d.top_student_marks = top.marks if top else ''
    courses = Course.objects.annotate(
        student_count=Count('students', distinct=True),
        avg_marks=Avg('students__marks'),
        max_marks=Max('students__marks'),
    )
    agg = Student.objects.aggregate(
        avg_marks=Avg('marks'), top=Max('marks'),
        bottom=Min('marks'), total=Count('id')
    )
    toppers = Student.objects.order_by('-marks')[:3]
    dept_stats = Department.objects.annotate(
        strength=Count('students'), avg_marks=Avg('students__marks')
    )

    return render(request, 'students/admin_dashboard.html', {
        'students': students,
        'departments': departments,
        'courses': courses,
        'agg': agg,
        'toppers': toppers,
        'dept_stats': dept_stats,
        'dept_form': dept_form,
        'course_form': course_form,
        'student_form': student_form,
        'document_form': document_form,
        'documents': documents,
        'profile': profile,
        'profile_form': profile_form,
        'password_form': password_form,
    })

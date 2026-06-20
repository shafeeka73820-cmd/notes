from django.contrib import admin, messages
from django.db.models import F, Q, Count, Avg, Max, Min, Sum
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html
from .models import Student, Department, Course, Profile
from .forms import AdminStudentForm, AdminDepartmentForm, AdminCourseForm

admin.site.site_header = 'CampusHub Administration'
admin.site.site_title = 'CampusHub Admin'
admin.site.index_title = 'Welcome to CampusHub Portal'


class StudentInline(admin.TabularInline):
    model = Student
    form = AdminStudentForm
    fields = ['name', 'roll', 'marks', 'is_active']
    extra = 0
    readonly_fields = ['marks']

    def has_change_permission(self, request, obj=None):
        return False


@admin.action(description='Add 5 bonus marks (F expression)')
def apply_bonus_marks(modeladmin, request, queryset):
    updated = queryset.update(marks=F('marks') + 5)
    modeladmin.message_user(request, f'{updated} student(s) received +5 bonus marks.', messages.SUCCESS)


@admin.action(description='Mark as inactive (Q object: exclude toppers)')
def deactivate_non_toppers(modeladmin, request, queryset):
    toppers = queryset.filter(Q(marks__gte=90))
    others = queryset.exclude(id__in=toppers.values('id'))
    count = others.update(is_active=False)
    modeladmin.message_user(request, f'{count} student(s) deactivated (toppers preserved).', messages.WARNING)


@admin.action(description='Reset marks to 0')
def reset_marks(modeladmin, request, queryset):
    count = queryset.update(marks=0)
    modeladmin.message_user(request, f'{count} student(s) marks reset to 0.', messages.ERROR)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    form = AdminDepartmentForm
    list_display = ['name', 'code', 'student_count', 'avg_marks', 'top_student']
    search_fields = ['name', 'code']
    list_filter = ['name']
    inlines = [StudentInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _student_count=Count('students', distinct=True),
            _avg_marks=Avg('students__marks'),
        )

    def student_count(self, obj):
        return obj._student_count
    student_count.short_description = 'Students'
    student_count.admin_order_field = '_student_count'

    def avg_marks(self, obj):
        if obj._avg_marks:
            return f'{obj._avg_marks:.1f}'
        return '-'
    avg_marks.short_description = 'Avg Marks'
    avg_marks.admin_order_field = '_avg_marks'

    def top_student(self, obj):
        top = obj.students.order_by('-marks').first()
        if top:
            return format_html('<strong>{}</strong> ({})', top.name, top.marks)
        return '-'
    top_student.short_description = 'Top Performer'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = AdminCourseForm
    list_display = ['code', 'title', 'credits', 'student_count', 'avg_marks', 'max_marks']
    search_fields = ['title', 'code', 'students__name']
    list_filter = ['credits']
    filter_horizontal = ['students']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _student_count=Count('students', distinct=True),
            _avg_marks=Avg('students__marks'),
            _max_marks=Max('students__marks'),
        )

    def student_count(self, obj):
        return obj._student_count
    student_count.short_description = 'Students'
    student_count.admin_order_field = '_student_count'

    def avg_marks(self, obj):
        if obj._avg_marks:
            return f'{obj._avg_marks:.1f}'
        return '-'
    avg_marks.short_description = 'Avg'
    avg_marks.admin_order_field = '_avg_marks'

    def max_marks(self, obj):
        return obj._max_marks or '-'
    max_marks.short_description = 'Highest'
    max_marks.admin_order_field = '_max_marks'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'email_lookup']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email', 'phone']

    def email_lookup(self, obj):
        return obj.user.email
    email_lookup.short_description = 'Email (FK lookup)'
    email_lookup.admin_order_field = 'user__email'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = AdminStudentForm
    actions = [apply_bonus_marks, deactivate_non_toppers, reset_marks]

    list_display = [
        'photo_thumbnail', 'name', 'roll', 'branch', 'department', 'marks',
        'grade', 'is_active', 'courses_preview',
    ]
    list_filter = ['branch', 'department', 'is_active', 'marks']
    search_fields = ['name', 'roll', 'email', 'department__name']
    ordering = ['roll']
    list_editable = ['marks', 'is_active']
    list_select_related = ['department']
    autocomplete_fields = ['department']

    fieldsets = (
        ('Personal Info', {'fields': ('name', 'roll', 'email', 'phone')}),
        ('Academics', {'fields': ('branch', 'department', 'marks', 'is_active')}),
        ('Media', {'fields': ('photo',)}),
    )

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="48" height="60" style="object-fit:cover;border-radius:6px;">',
                obj.photo.url
            )
        return format_html(
            '<img src="/static/images/default-avatar.svg" width="48" height="60" '
            'style="object-fit:cover;border-radius:6px;opacity:0.6;">'
        )
    photo_thumbnail.short_description = 'Photo'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('courses')

    def courses_preview(self, obj):
        courses = obj.courses.all()[:3]
        if not courses:
            return '-'
        return ', '.join(c.code for c in courses)
    courses_preview.short_description = 'Courses (prefetch)'

    class Media:
        css = {
            'all': ('css/style.css',),
        }

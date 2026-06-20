from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count, Q, Avg, Max, Min, Sum, F
from .models import Student
from .forms import StudentForm


class StudentListView(ListView):
    model = Student
    template_name = 'students/index.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list
        context['count'] = qs.count()
        context['dept_count'] = Student.objects.values('branch').distinct().count()
        context['title'] = 'Student Portal'
        context['grade_a'] = qs.filter(marks__gte=75).count()
        context['grade_b'] = qs.filter(marks__gte=60, marks__lt=75).count()
        context['grade_c'] = qs.filter(marks__gte=40, marks__lt=60).count()
        context['grade_f'] = qs.filter(marks__lt=40).count()
        agg = qs.aggregate(
            avg_marks=Avg('marks'), top_marks=Max('marks'),
            min_marks=Min('marks'),
            avg_attendance=Avg('attendance')
        )
        context['avg_marks'] = agg['avg_marks']
        context['min_marks'] = agg['min_marks']
        context['avg_attendance'] = agg['avg_attendance']
        context['top_student'] = qs.order_by('-marks').first()
        context['toppers'] = qs.order_by('-marks')[:5]
        context['attendance_high'] = qs.filter(attendance__gte=85).count()
        context['attendance_mid'] = qs.filter(attendance__gte=75, attendance__lt=85).count()
        context['attendance_low'] = qs.filter(attendance__lt=75).count()
        fee_agg = qs.aggregate(
            total_fees_sum=Sum('total_fees'),
            paid_fees_sum=Sum('paid_fees'),
            fees_pending=Sum('total_fees') - Sum('paid_fees'),
            avg_paid=Avg('paid_fees')
        )
        context['total_fees_sum'] = fee_agg['total_fees_sum'] or 0
        context['paid_fees_sum'] = fee_agg['paid_fees_sum'] or 0
        context['fees_pending'] = fee_agg['fees_pending'] or 0
        context['fully_paid_count'] = qs.filter(total_fees=F('paid_fees')).count()
        context['pending_count'] = qs.filter(paid_fees__lt=F('total_fees')).count()
        context['fee_zero_count'] = qs.filter(paid_fees=0).count()
        context['partial_count'] = qs.filter(paid_fees__gt=0, paid_fees__lt=F('total_fees')).count()
        context['branch_data'] = (
            qs.values('branch')
            .annotate(count=Count('id'))
            .order_by('branch')
        )
        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/detail.html'
    context_object_name = 'student'
    slug_field = 'roll'
    slug_url_kwarg = 'roll'


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Student'
        return context

    def get_success_url(self):
        return reverse_lazy('students:detail', kwargs={'roll': self.object.roll})


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    slug_field = 'roll'
    slug_url_kwarg = 'roll'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Student'
        return context

    def get_success_url(self):
        return reverse_lazy('students:detail', kwargs={'roll': self.object.roll})


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    slug_field = 'roll'
    slug_url_kwarg = 'roll'
    success_url = reverse_lazy('students:index')


class DashboardView(TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Student.objects.all()
        context['count'] = qs.count()
        context['dept_count'] = Student.objects.values('branch').distinct().count()
        agg = qs.aggregate(
            avg_marks=Avg('marks'), top_marks=Max('marks'),
            avg_attendance=Avg('attendance'),
            total_fees_sum=Sum('total_fees'),
            paid_fees_sum=Sum('paid_fees'),
            fees_pending=Sum('total_fees') - Sum('paid_fees'),
        )
        context['avg_marks'] = agg['avg_marks']
        context['top_marks'] = agg['top_marks']
        context['avg_attendance'] = agg['avg_attendance']
        context['total_fees_sum'] = agg['total_fees_sum'] or 0
        context['paid_fees_sum'] = agg['paid_fees_sum'] or 0
        context['fees_pending'] = agg['fees_pending'] or 0
        context['top_student'] = qs.order_by('-marks').first()
        context['toppers'] = qs.order_by('-marks')[:5]
        context['fully_paid_count'] = qs.filter(total_fees=F('paid_fees')).count()
        context['partial_count'] = qs.filter(paid_fees__gt=0, paid_fees__lt=F('total_fees')).count()
        context['fee_zero_count'] = qs.filter(paid_fees=0).count()
        context['grade_a'] = qs.filter(marks__gte=75).count()
        context['grade_b'] = qs.filter(marks__gte=60, marks__lt=75).count()
        context['grade_c'] = qs.filter(marks__gte=40, marks__lt=60).count()
        context['grade_f'] = qs.filter(marks__lt=40).count()
        context['branch_data'] = (
            qs.values('branch')
            .annotate(count=Count('id'))
            .order_by('branch')
        )
        context['attendance_high'] = qs.filter(attendance__gte=85).count()
        context['attendance_mid'] = qs.filter(attendance__gte=75, attendance__lt=85).count()
        context['attendance_low'] = qs.filter(attendance__lt=75).count()
        return context

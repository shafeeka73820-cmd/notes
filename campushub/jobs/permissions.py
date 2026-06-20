from rest_framework.permissions import BasePermission


class IsRecruiter(BasePermission):
    message = "Only recruiters can perform this action."

    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                hasattr(request.user, 'job_profile') and
                request.user.job_profile.role == 'R')


class IsCandidate(BasePermission):
    message = "Only candidates can perform this action."

    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                hasattr(request.user, 'job_profile') and
                request.user.job_profile.role == 'C')


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.recruiter == request.user

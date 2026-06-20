from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from students.api_views import (
    StudentViewSet, DepartmentViewSet, CourseViewSet,
    ProfileViewSet, DocumentViewSet, AuthViewSet
)
from library.api_views import (
    AuthorViewSet, BookViewSet, MemberViewSet, IssueViewSet
)
from blog.api_views import CategoryViewSet as BlogCategoryViewSet, PostViewSet, CommentViewSet
from store.api_views import (
    CategoryViewSet as StoreCategoryViewSet, ProductViewSet,
    CartViewSet, OrderViewSet
)
from jobs.api_views import JobViewSet, ApplicationViewSet, RegisterView
from quotes.api_views import QuoteViewSet

router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')
router.register('departments', DepartmentViewSet)
router.register('courses', CourseViewSet)
router.register('profiles', ProfileViewSet, basename='profile')
router.register('documents', DocumentViewSet)
router.register('auth', AuthViewSet, basename='auth')
router.register('library/authors', AuthorViewSet)
router.register('library/books', BookViewSet)
router.register('library/members', MemberViewSet)
router.register('library/issues', IssueViewSet)
router.register('blog/categories', BlogCategoryViewSet)
router.register('blog/posts', PostViewSet, basename='post')
router.register('blog/comments', CommentViewSet, basename='comment')
router.register('store/categories', StoreCategoryViewSet, basename='store-category')
router.register('store/products', ProductViewSet)
router.register('store/cart', CartViewSet, basename='cart')
router.register('store/orders', OrderViewSet, basename='order')
router.register('jobs', JobViewSet, basename='job')
router.register('applications', ApplicationViewSet, basename='application')
router.register('quotes', QuoteViewSet, basename='quote')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('', lambda req: redirect('students:index'), name='root'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='jobs-register'),
]

from django.shortcuts import render

def campus_home(request):
    return render(request, 'campus_home.html')

urlpatterns += [
    path('', campus_home, name='campus_home'),
]

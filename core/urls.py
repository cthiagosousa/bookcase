from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

urlpatterns = [
    path('api/users/', views.AccountViewSet.as_view({'get': 'get'})),

    path('api/books/',views.BookViewSet.as_view({'get': 'get', 'post': 'create'})),
    path('api/book/update/<int:book_id>',views.BookViewSet.as_view({'put': 'update'})),
    path('api/book/delete/<int:book_id>',views.BookViewSet.as_view({'delete': 'delete'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views

urlpatterns = [
    path('api/login/', views.AccountViewSet.as_view({'post': 'login'})),
    path('api/create-account/', views.AccountViewSet.as_view({'post': 'create'})),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/books/',views.BookViewSet.as_view({'get': 'get', 'post': 'create'})),
    path('api/book/update/<int:book_id>',views.BookViewSet.as_view({'put': 'update'})),
    path('api/book/delete/<int:book_id>',views.BookViewSet.as_view({'delete': 'delete'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)

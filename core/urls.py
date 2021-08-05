from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views

urlpatterns = [
    path('api/account-details/<int:account_id>', views.AccountViewSet.as_view({'post': 'account_details'})),
    path('api/login/', views.AccountViewSet.as_view({'post': 'login'})),
    path('api/create-account/', views.AccountViewSet.as_view({'post': 'create'})),
    path('api/update-account/<int:account_id>', views.AccountViewSet.as_view({'put': 'update'})),
    path('api/delete-account/<int:account_id>', views.AccountViewSet.as_view({'delete': 'delete'})),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/books/',views.BookViewSet.as_view({'get': 'get_all'})),
    path('api/books/<book_id>', views.BookViewSet.as_view({'get': 'get_by_id'})),
    path('api/books/rent/<book_id>', views.BookViewSet.as_view({'post': 'rent'})),
    path('api/books/refund/<book_id>', views.BookViewSet.as_view({'post': 'refund'})),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from .serializers.book_serializer import BookSerializer
from .serializers.user_serializer import UserSerializer
from .models import Book

class AccountViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [BasePermission]

    def login(self, request: HttpRequest) -> Response:
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Conta não encontrada'})

        auth_user = authenticate(username=user.username, password=password)
        serializer = UserSerializer(auth_user)

        if auth_user is not None:
            login(request, auth_user)
            
            data_user = {
                "id": serializer.data['id'],
                "last_login": serializer.data['last_login'],
                "is_superuser": serializer.data['is_superuser'],
                "username": serializer.data['username'],
                "email": serializer.data['email'],
                "is_staff": serializer.data['is_staff'],
                "is_active": serializer.data['is_active'],
                "date_joined": serializer.data['date_joined'],
                "groups": serializer.data['groups'],
                "user_permissions": serializer.data['user_permissions']
            }

            return Response(data_user)

        return Response({
            'error': 'Conta não encontrada',
        })

    def create(self, request: HttpRequest) -> Response:
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        user = User.objects.create_user(username, email, password)
        
        if user is not None:
            return Response({
                'message': 'Conta criada'
            })

        return Response({
            'error': 'Houve um problema ao criar a conta'
        })


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: HttpRequest) -> Response:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
    
        return Response(serializer.data)

    def create(self, request: HttpRequest) -> Response:
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def update(self, request: HttpRequest, book_id: int) -> Response:
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book, request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'book': serializer.data,
                'message': 'The item has been updated'
            })
        
        return Response(serializer.errors)

    def delete(self, request: HttpRequest, book_id: int) -> Response:
        book = Book.objects.get(id=book_id)
        book.delete()
        
        return Response({
            'message': 'Deleted'
        })

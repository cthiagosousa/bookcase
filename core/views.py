from django.http.request import HttpRequest
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers.book_serializer import BookSerializer
from .serializers.user_serializer import UserSerializer
from .models import Book

class AccountViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request: HttpRequest) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def login(self, request: HttpRequest) -> Response:
        pass

    def create(self, request: HttpRequest) -> Response:
        pass

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request: HttpRequest) -> Response:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
    
        return Response(serializer.data)

    def create(self, request: HttpRequest) -> Response:
        if request.POST:
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

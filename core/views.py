from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from .serializers.book_serializer import BookSerializer
from .serializers.user_serializer import UserSerializer
from .models import Book
from .email_messages import create_account_message

class AccountViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [BasePermission]

    def login(self, request: HttpRequest) -> Response:
        email = str(request.data['email'])
        password = str(request.data['password'])

        if len(email.strip()) == 0 or len(password.strip()) == 0:
            return Response({
                'error': 'A campos vazios'
            })

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'Conta não encontrada'
                })

        auth_user = authenticate(username=user.username, password=password)
        data_user = UserSerializer(auth_user).data
        data_user['password'] = password

        if auth_user is not None:
            login(request, auth_user)

        return Response(data_user)

    def create(self, request: HttpRequest) -> Response:
        username = str(request.data['username'])
        email = str(request.data['email'])
        password = str (request.data['password'])
        
        if len(username.strip()) == 0 or len(email.split()) == 0 or len(password.strip()) == 0:
            return Response({
                'error': 'A campos vazios'
            })

        user = User.objects.create_user(username, email, password)
        data_user = UserSerializer(user).data
        data_user['password'] = password

        if user is not None:
            send_mail(
                create_account_message['subject'],
                create_account_message['message'],
                create_account_message['from'],
                [email],
            )

            return Response(data_user)

        return Response({
            'error': 'Houve um problema ao criar a conta'
        })

    def update(self, request: HttpRequest, account_id: int) -> Response:
        username = str(request.data['username'])
        email = str(request.data['email'])
        password = str(request.data['password'])

        if len(username.strip()) == 0 or len(email.split()) == 0 or len(password.strip()) == 0:
            return Response({
                'error': 'A campos vazios'
            })

        user = User.objects.get(id=account_id)
        user.username = username
        user.email = email
        user.set_password(password)

        user.save()

        return Response({
            'message': 'Updated'
            })
    
    def delete(self, request: HttpRequest, account_id: int) -> Response:
        User.objects.get(id=account_id).delete()

        return Response({
            'message': 'Account deleted'
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

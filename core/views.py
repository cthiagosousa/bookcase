from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser, User
from django.core.mail import send_mail
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

    def account_details(self, request: HttpRequest, account_id: int):
        try:
            user = User.objects.get(id=account_id)
            data_user = UserSerializer(user).data
            del data_user['password']
        
        except User.DoesNotExist:
            return Response({
                "error": "Esse usuário não existe"
            })
        
        except Exception:
            return Response({
                "error": "Ocorreu um erro."
            })

        return Response(data_user)


    def login(self, request: HttpRequest) -> Response:
        email = str(request.data['email'])
        password = str(request.data['password'])

        if not email.strip() or not password.strip():
            return Response({
                'error': 'A campos vazios'
            })

        try:
            user = User.objects.get(email=email)
            auth_user = authenticate(username=user.username, password=password)

            if auth_user is not None:
                login(request, auth_user)

            data_user = UserSerializer(auth_user).data
            del data_user['password']

        except User.DoesNotExist:
            return Response({
                'error': 'Conta não encontrada'
                })
                
        except Exception:
            return Response({
                "error": "Ocorreu um erro"
            })
        
        return Response(data_user)

    def create(self, request: HttpRequest) -> Response:
        username = str(request.data['username'])
        email = str(request.data['email'])
        password = str (request.data['password'])
        
        if not username.strip() or not email.split() or not password.strip():
            return Response({
                'error': 'A campos vazios'
            })

        user = User.objects.create_user(username, email, password)
        data_user = UserSerializer(user).data
        del data_user['password']

        if user is not None:
            send_mail(
                subject=f'Olá {username} sua conta foi criada com sucesso!',

                message='''Sua conta foi criada e você já pode aproveitar e alugar qualquer livro da nossa
                estante, boa leitura.''',

                from_email='sendmail@project.com',
                recipient_list=[email],
            )

            return Response(data_user)

        return Response({
            'error': 'Houve um problema ao criar a conta'
        })

    def update(self, request: HttpRequest, account_id: int) -> Response:
        username = str(request.data['username'])
        email = str(request.data['email'])
        password = str(request.data['password'])

        if not username.strip() or not email.split() or not password.strip():
            return Response({
                'error': 'A campos vazios'
            })

        user = User.objects.get(id=account_id)
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        data_user = UserSerializer(user).data
        del data_user['password']

        return Response(data_user)
    
    def delete(self, request: HttpRequest, account_id: int) -> Response:
        User.objects.get(id=account_id).delete()

        return Response({
            'success': 'Conta deletada'
        })


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_all(self, request: HttpRequest) -> Response:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
    
        return Response(serializer.data)
    
    def get_by_id(self, request: HttpRequest, book_id: str) -> Response:
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
        
        except Book.DoesNotExist:
            return Response({
                "error": "Esse livro não existe."
            })
        
        except Exception:
            return Response({
                "error": "Ocorreu um erro."
            })
        
        return Response(serializer.data)

    def rent(self, request: HttpRequest, book_id: str) -> Response:
        user = request.user

        if user == AnonymousUser:
            return Response({
                "error": "Precisa de um usuário logado."
            })
        
        try:
            book = Book.objects.get(id=book_id)

            if book.users.filter(id=user.id):
                return Response({
                    "error": "Usuário já alugou esse livro."
                })

            if book.available_quantity == 0:
                return Response({
                    "error": "Livro esgotado."
                })

            book.users.add(user)
            book.available_quantity = book.available_quantity - 1
            book.save()

            send_mail(
                subject=f'Olá {user.username}, obrigado por alugar o livro {book.title}!',

                message=f'''Você acabou de alugar "{book.title}", não esqueça de devolver seu livro após a leitura.''',

                from_email='sendmail@project.com',
                recipient_list=[user.email],
            )
            
        except Book.DoesNotExist:
            return Response({
                "error": "Livro não encontrado."
            })

        except Exception as error:
            print(error)
            return Response({
                "error": "Ocorreu um erro"
            })

        return Response({
            "success": "Livro alugado."
        })

    def refund(self, request: HttpRequest, book_id: str) -> Response:
        user = request.user

        if user == AnonymousUser:
            return Response({
                "error": "Precisa de um usuário logado."
            })

        try: 
            book = Book.objects.get(id=book_id)

            if not user.books.filter(id=book_id):
                return Response({
                    "error": "Usuário não alugou esse livro."
                })

            user.books.remove(book)
            book.available_quantity = book.available_quantity + 1
            user.save()
            book.save()

            send_mail(
                subject=f'Olá {user.username}, espero que tenha tido uma boa leitura!',

                message=f'''Você devolveu "{book.title}" com sucesso, 
                fique a vontade para alugar qualquer outro livro de nossa estante.''',

                from_email='sendmail@project.com',
                recipient_list=[user.email],
            )

        except Book.DoesNotExist:
            return Response({
                "error": "Livro não encontrado"
            })

        except Exception as error:
            print(error)
            return Response({
                "error": "Ocorreu algum erro."
            })

        return Response({
                "success": "Livro devolvido."
            })

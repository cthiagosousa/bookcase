from django.shortcuts import HttpResponse, render
from django.http.request import HttpRequest

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello World')

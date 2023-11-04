from django.shortcuts import render
from django.http import HttpResponse
from .buscador import Buscador


def index(request):
    """
    Enpoint para el home
    """
    return HttpResponse("Hello World!")
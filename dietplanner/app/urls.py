from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("buscar/", views.buscar, name="buscar_resultados"),
    path("resultados/", views.resultados, name="resultados"), #Endpoint para buscar recetas
    path("receta/<int:id>", views.detalle_receta, name="detalle_receta"), #Endpoint para buscar detalles de una receta
    path("guardadas/", views.guardadas, name="guardadas")
]
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .buscador import Buscador
import json, re

buscador = Buscador()

def index(request):
    """
    Endpoint para el home
    """
    context = {
        "top": buscador.getRandom(5)
    }
    return render(request, 'buscador.html', context)

def buscar(request):
    """
    Endpoint para buscar los ingredientes en base a una query
    """
    resultados_lista = []
    if(request.method == 'GET'):
        query = request.GET.get('query','')
        resultados = buscador.buscarIngredienteNombre(query)
        for resultado in resultados:
            resultado_dict = {
                'id': resultado[0],
                'nombre': resultado[1]
            }
            resultados_lista.append(resultado_dict)
    return JsonResponse({'resultados': resultados_lista})

def resultados(request):
    """
    Endpoint para buscar recetas en base a los ingredientes seleccionados
    """
    if request.method == 'POST':
        metodo = request.POST.get("metodo")
        if request.COOKIES.get("recetas"):
            guardadas_json = json.loads(request.COOKIES.get("recetas"))
            guardadas  = [eval(i) for i in guardadas_json]
        else:
            guardadas = []
        if metodo == "ingredientes":
            if request.COOKIES.get("IDs"):
                seleccionados_json = json.loads(request.COOKIES.get("IDs"))
                if seleccionados_json:
                    IDs = list(map(int, seleccionados_json["seleccionados"]))
                    lista_recetas = buscador.buscarRecetasIngredientes(IDs)
                    recetas = []
                    for receta in lista_recetas:
                        recetas.append((receta[0],receta[1],receta[2],receta[0] in guardadas))
                    context = {
                        "top": buscador.getRandom(5),
                        "resultados": recetas
                    }
                else:
                    context = {
                        "top": buscador.getRandom(5)
                    }
            else:
                return redirect("index")
        if metodo == "recetas":
            query = request.POST.get('search-recetas')
            lista_recetas = buscador.buscarRecetasNombre(query)
            recetas = []
            for receta in lista_recetas:
                recetas.append((receta[0],receta[1],receta[2],receta[0] in guardadas))
            context = {
                "top": buscador.getRandom(5),
                "resultados": recetas
            }
        return render(request,'resultados.html',context)
    else:
        return redirect("index")
    
def detalle_receta(request, id):
    """
    Endpoint para ver los detalles de una receta
    """
    try:
        receta = buscador.buscarRecetasID(id)
        formateado = re.sub("Paso (\d+)\n\n","",receta[2]).split(";")
        IDs = []
        if request.COOKIES.get("recetas"):
            guardadas_json = json.loads(request.COOKIES.get("recetas"))
            IDs  = [eval(i) for i in guardadas_json]
        
        saved = id in IDs
        context = {
            "receta_id": receta[0],
            "receta_nombre": receta[1],
            "receta_pasos": formateado,
            "receta_ingredientes": receta[4],
            "saved": saved
        }
        return render(request,'receta.html', context)
    except:
        return redirect("index")

def guardadas(request):
    """
    Endpoint para ver las recetas guardadas
    """
    context = {}
    if request.COOKIES.get("recetas"):
        guardadas_json = json.loads(request.COOKIES.get("recetas"))
        IDs  = [eval(i) for i in guardadas_json]
        recipes = []
        for id in IDs:
            recipe = buscador.buscarRecetasID(id)
            saved = recipe[0] in IDs
            recipes.append((recipe[0],recipe[1],recipe[4],saved))

        context = {
            "top": buscador.getRandom(5),
            "resultados": recipes
        }
    
    return render(request,'resultados.html',context)
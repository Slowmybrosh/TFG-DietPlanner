from django.test import RequestFactory, TestCase
from django.urls import reverse
from app.buscador import Buscador
from ..models import RecipeIngredient, Recipes, Ingredients

class TestBuscador(TestCase):

    def setUp(self) -> None:
        self.buscador = Buscador()
        self.factory = RequestFactory()
        recipe1 = Recipes(name="test1", steps="test1")
        recipe2 = Recipes(name="test2", steps="test2")
        recipe3 = Recipes(name="test3", steps="test3")
        recipe4 = Recipes(name="test4", steps="test3")
        recipe5 = Recipes(name="test5", steps="test5")
        recipe1.save()
        recipe2.save()
        recipe3.save()
        recipe4.save()
        recipe5.save()
        ingredient1 = Ingredients(id=0,name="test1")
        ingredient1.save()
        contains = RecipeIngredient(recipe_id=recipe2,ingredient_id=ingredient1)
        contains.save()

    def test_call_view_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buscador.html')
    
    def test_call_view_resultados_no_exists(self):
        response = self.client.get(reverse("resultados"), follow=True)
        self.assertRedirects(response, '/')

    def test_call_view_resultados(self):
        self.client.cookies['IDs'] = []
        response = self.client.post(reverse("resultados"),data={'metodo': 'ingredientes'})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'resultados.html')

    def test_call_view_guardadas(self):
        request = self.client.get(reverse("guardadas"))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'resultados.html')

    def test_call_view_detalle(self):
        request = self.client.get(reverse("detalle_receta",args="1"))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'receta.html')

    def test_data_in_detalle(self):
        request = self.client.get(reverse("detalle_receta",args="1"))
        self.assertTemplateUsed(request, 'receta.html')
        self.assertEqual(request.context['receta_id'], 1)
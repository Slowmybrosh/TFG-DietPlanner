import sys, unittest, warnings, pytest

@pytest.fixture(autouse=True)
def suppress_all_warnings():
    warnings.filterwarnings('ignore')

sys.path.append('./')
sys.path.append('./src/')

from src.buscador import Buscador

class TestBuscador(unittest.TestCase):

    def setUp(self) -> None:
        self.buscador = Buscador()

    # Buscador
    def test_buscar_ingrediente_id(self):
        assert self.buscador.buscarIngredienteID(0) == [(0, 'bacalao')]

    def test_buscar_ingrediente_nombre(self):
        assert self.buscador.buscarIngredienteNombre('bacalao') == [(0, 'bacalao')]

    def test_buscar_receta_id(self):
        resultado = self.buscador.buscarRecetasID(1)
        expected = [(1,'Budín de bacalao con espinacas', 'Paso 1\n\nSe le quita al bacalao la piel y se seca con papel absorvente;Paso 2\n\nEn el vaso de la batidora se echa una clara de huevo, el bacalao y la nata con la sal, pimienta y nuez moscada. Se añada las espinacas y el limón. Cuidado con la sal y el bacalao.;Paso 3\n\nSe mete en un recipiente apto para Air fire engrasado con mantequilla. Se calienta la Air fire 2 minutos antes. Después se pone a 180 grados 15 minutos. Sino está poner unos minutos mas.', 7, ['bacalao', 'huevo', 'espinacas', 'nata', 'limón', 'queso en polvo', 'mantequilla'])]
        assert resultado == expected

    def test_buscar_receta_nombre(self):
        resultado = self.buscador.buscarRecetasNombre('bacalao')
        expected = [(1, 'Budín de bacalao con espinacas', ['bacalao', 'huevo', 'espinacas', 'nata', 'limón', 'queso en polvo', 'mantequilla']), (9, 'Bacalao con salsa de calabacín y langostinos con 2 texturas', ['bacalao', 'huevo', 'cebolla', 'ajo', 'harina', 'langostinos', 'calabazín', 'mejillones', 'caldo de verduras', 'hierbas provenzales', 'queso philadelpia']), (23, 'Potaje de garbanzos, bacalao y gambones salvajes (versión exprés)', ['bacalao', 'cebolla', 'ajo', 'pimentón', 'caldo de verduras', 'AOVE', 'pimiento verde', 'comino', 'vino blanco', 'caldo de pescado', 'garbanzos', 'gambones', 'pisto'])]
        assert resultado == expected

    def test_buscar_receta_ingredentes(self):
        resultado = self.buscador.buscarRecetasIngredientes([0,1,2,3,5,6,7])
        expected = [(1, 'Budín de bacalao con espinacas', ['bacalao', 'huevo', 'espinacas', 'nata', 'limón', 'queso en polvo', 'mantequilla'])]
        assert resultado == expected

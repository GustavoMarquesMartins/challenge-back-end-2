from django.test import TestCase

from financeiro.models import Receita

class FixtureDataTestCase(TestCase):

  fixtures = ['receitas_iniciais']

  def test_que_verifica_carregamento_das_fixtures(self):
    """Verifica carregamento da fixture para o banco de dados de teste"""
    receita = Receita.objects.get(pk=1)
    todas_as_receitas = Receita.objects.all()
    self.assertEqual(receita.descricao, 'Venda de um celular')
    self.assertEqual(len(todas_as_receitas), 17)

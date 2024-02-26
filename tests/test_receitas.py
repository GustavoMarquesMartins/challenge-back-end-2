from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from .base_test.base_test import BaseTest
from django.urls import reverse


class ReceitaAPITestCase(BaseTest, APITestCase):
  """
  Classe de teste para verificar o retorno esperado de cada endpoint da API.

  Esta classe contém métodos de teste que verificam se os endpoints da API estão retornando os códigos de status HTTP esperados,
  assim como os dados corretos. Os testes incluem requisições GET, POST, PUT e DELETE para diferentes recursos da API.
  """
  def setUp(self):
    super().setUp()
    self.lista_url = reverse('receitas-list')

  def test_tenta_buscar_lista_de_receitas(self):
    """Verifica se uma requisição GET para o recurso de receitas retorna um status HTTP  200 (OK)"""
    resposta = self.client.get(self.lista_url)
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_tenta_buscar_receita(self):
    """Verifica se uma requisição GET para um recurso de receita específico retorna um status HTTP   200 (OK)."""
    resposta = self.client.get(self.lista_url + '1/')
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_tenta_criar_uma_receita(self):
    """Verifica se uma requisição POST para criar uma receita retorna um status HTTP 201 (Created) e
    se a resposta inclui o cabeçalho 'location' com a URL do recurso criado"""
    resposta = self.client.post(self.lista_url, self.receita())
    url_usada_para_requisicao = resposta.wsgi_request.build_absolute_uri()

    self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
    self.assertEqual(resposta['location'], url_usada_para_requisicao + str(resposta.data['id']))

  def test_tenta_deletar_uma_receita(self):
    """Verifica se uma requisição DELETE para um recurso de receita específico retorna um status HTTP 204 (No Content)"""
    resposta = self.client.delete(self.lista_url + '1/')
    self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)

  def test_tenta_atualizar_uma_receita(self):
    """Verifica se uma requisição PUT para atualizar um recurso de receita específico retorna um status HTTP 200 (OK)"""
    resposta = self.client.put(self.lista_url + '1/', data=self.receita_atualiza())
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def receita(self):
    """Retorna um dicionário com os dados a serem enviados na requisição POST."""
    return {
        'descricao': 'Receita com menos de 30 dias criada',
        'valor': 13.00
    }

  def receita_atualiza(self):
    """Retorna um dicionário com os dados a serem enviados na requisição PUT."""
    return {
        'descricao': 'Receita com menos de 30 dias criada (Atualizada)',
        'valor': 23.00
    }

class ReceitaTestCase(BaseTest, TestCase):
  """
  Classe de teste para verificar o retorno esperado dos recursos de listagem de receitas por ano e mês ou por descrição.

  Esta classe contém métodos de teste que verificam se os endpoints da API estão retornando os códigos de status HTTP esperados,
  assim como os dados corretos. Os testes incluem requisições GET para recursos de listagem por ano e mês ou descrição.
  """
  def setUp(self):
    super().setUp()
    self.lista_url = reverse('receitas-list')

  def test_faz_uma_requisicao_com_o_parametro_descricao(self):
    """
    Quando passada uma URL com o parâmetro 'descricao', deve ser retornada apenas as receitas que atendam a esse parâmetro de pesquisa.
    Verifica também se o status da resposta é  200 (OK).
    """
    descricao = 'Descrição para teste'
    resposta = self.client.get(self.lista_url + f'?descricao={descricao}')
    lista_receitas = resposta.json()
    
    for receita in lista_receitas:
        self.assertEqual(receita['descricao'], descricao)
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_faz_uma_requisicao_com_o_parametro_mes_e_ano(self):
    """
    Quando são passados os parâmetros mês e ano usando o método GET, deve ser retornada uma lista de receitas.
    Verifica também se o status da resposta é  200 (OK) e se as datas das receitas retornadas correspondem ao mês e ano especificados.
    """
    mes = '02'
    ano = '2024'

    resposta = self.client.get(self.lista_url + f'{ano}/{mes}/')
    lista_receitas = resposta.json()
    for receita in lista_receitas:
        data = receita['data']
        self.assertEqual(data[3:5], str(mes))
        self.assertEqual(data[6:10], str(ano))
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

from rest_framework import serializers

from .models import *
from .validators import *

import json

class BaseTransacaoSerializer(serializers.ModelSerializer):
    """Base para ReceitaSerializer e DespesaSerializer."""

    data = serializers.SerializerMethodField(method_name='get_data_formatada')

    def get_data_formatada(self, obj):
        """Retorna 'data' formatada como 'dd/mm/aaaa : HH:MM'."""
        return obj.data.strftime('%d/%m/%Y : %H:%M')

    def validate(self, data):
        """Garante que a descrição não seja duplicada durante 1 mês."""
        if not descricao_valida(self.Meta.model, data['descricao']):
            raise serializers.ValidationError({'descricao': 'Descrição não pode ser duplicada por 1 mês'})
        return data

class ReceitaSerializer(BaseTransacaoSerializer):
    """Serializer para Receita."""

    class Meta:
        """Configurações do serializer."""
        model = Receita
        fields = ['id','descricao', 'valor', 'data']

class DespesaSerializer(BaseTransacaoSerializer):
    """Serializer para Despesa."""

    class Meta:
        """Configurações do serializer."""
        model = Despesa
        fields = ['id','descricao', 'valor', 'data']

class DespesaSerializerV2(BaseTransacaoSerializer):
    """Serializer para Despesa."""

    class Meta:
        """Configurações do serializer."""
        model = Despesa
        fields = ['id','descricao', 'valor', 'data','categoria']

class ResumoSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField(method_name='get_data')

    def to_representation(self, obj):
        """
        Sobrescreve o método padrão para adicionar um campo personalizado à representação.
        O campo 'valor_gasto_por_categoria' é deserializado de uma string JSON para um dicionário e adicionado à representação.
        """

        # Obter a representação padrão do serializer
        representation = super().to_representation(obj)
        
        # Converte o campo valor_gasto_por_categoria do obj para um dicionario
        valor_gasto_por_categoria = json.loads(obj.valor_gasto_por_categoria)

        # Adicionar o campo personalizado da representação
        representation['valor_gasto_por_categoria'] = valor_gasto_por_categoria
        
        return representation
    
    def to_internal_value(self, data):
        """
        Verifica se 'valor_gasto_por_categoria' está presente nos dados que estão sendo desserializados.
        Se estiver presente, o valor é transformado em uma representação string para que o método json.dumps() possa serializar os dados.
        """
        # Verifique se 'valor_por_categoria' está presente nos dados que estão sendo desserializados
        if 'valor_gasto_por_categoria' in data:
            
            # Caso esteja presente, ele é armazenado na variável valor_gasto_por_categoria
            valor_gasto_por_categoria = data['valor_gasto_por_categoria']  
            
            # Cada valor gasto por categoria é transformado em uma representação string
            # para que o método json.dumps() possa serializar os dados
            for categoria, valor in valor_gasto_por_categoria.items():
                valor_gasto_por_categoria[categoria] = str(valor)

            # Após o valor das chaves do dicionário ser convertido para string, o dicionário pode ser serializado
            data['valor_gasto_por_categoria'] = json.dumps(valor_gasto_por_categoria)

        # Chame o método pai para continuar com a desserialização padrão
        return super().to_internal_value(data)

    def get_data(self, obj):
        return obj.data.strftime('%d/%m/%Y')    
    
    class Meta:
        model = Resumo
        fields = '__all__'


from rest_framework import serializers

from .models import *
from .validators import *

from django.contrib.auth.models import User

class BaseFinanceiroSerializer(serializers.ModelSerializer):
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

class ReceitaSerializer(BaseFinanceiroSerializer):
    """Serializer para Receita."""

    class Meta:
        """Configurações do serializer."""
        model = Receita
        fields = ['id','descricao', 'valor', 'data']

class DespesaSerializer(BaseFinanceiroSerializer):
    """Serializer para Despesa."""

    class Meta:
        """Configurações do serializer."""
        model = Despesa
        fields = ['id','descricao', 'valor', 'data']

class DespesaSerializerV2(BaseFinanceiroSerializer):
    """Serializer para Despesa."""

    class Meta:
        """Configurações do serializer."""
        model = Despesa
        fields = ['id','descricao', 'valor', 'data','categoria']

class ResumoMensalSerializer(serializers.Serializer):
    """
    Serializer para resumos mensais.
    Este serializador é usado para representar resumos mensais de finanças.
    """
    total_receitas = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_despesas = serializers.DecimalField(max_digits=10, decimal_places=2)
    saldo_final = serializers.DecimalField(max_digits=10, decimal_places=2)
    despesas_por_categoria = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2))

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para usuários.
    Este serializador é usado para representar dados de usuário, como id, nome de usuário e email.
    O campo de senha é protegido e não é retornado nas respostas da API.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


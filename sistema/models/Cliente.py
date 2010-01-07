# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.managers.managers import ClienteManager

   
      
class Cliente(models.Model):
    
    nome = models.CharField(max_length=80)
    id_fiscal = models.CharField(max_length=100, blank=False, verbose_name='Identificador Fiscal', help_text='Pessoa Física = CPF, Pessoa Jurídica = CNPJ')
    fone = models.CharField(max_length=14, unique=True)
    email = models.EmailField(null=True, blank=True)
    #contato = models.CharField(max_length=100, null=True, blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    referencia = models.CharField(max_length=150,null=True,blank=True,verbose_name='Ponto de Referência')
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=False, blank=False)
    estado =  models.CharField(max_length=2,null=True, blank=True)
    CEP = models.CharField(max_length=20, null=True, blank=True)
    logradouro = models.CharField(max_length=50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=10, null=True, blank=True)
    
    objects = ClienteManager()
   
    def valor_total(self):
        return self._valor_total or 0.0
    valor_total.short_description = 'Valor em Aberto'
    
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0
   
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Lista de Clientes'
        ordering = ('nome',)
        unique_together = ['nome', 'id_fiscal']
        app_label = 'sistema'
   
    def __unicode__(self):
        return self.nome.upper()


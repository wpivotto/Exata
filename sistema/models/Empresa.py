# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.managers.managers import EmpresaManager

            

class Empresa(models.Model):
    
    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    servicos = models.CharField(max_length=200, null=True, blank=True, help_text='Serviços prestados pela empresa')
    email = models.EmailField(null=True, blank=True)
    objects = EmpresaManager()
    
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0
    quantidade_servicos.short_description = 'Quantidade de Servicos Prestados'
    
    def valor_aberto(self):
        return self._valor_em_aberto or 0
    valor_aberto.short_description = "Total em Aberto"
    
    def valor_pago(self):
        return self._valor_pago or 0
    valor_pago.short_description = "Total Pago"
    
    def __unicode__(self):
        return self.nome + " de " + self.cidade
    
    class Meta:
        verbose_name = 'Empresa Prestadora de Serviços'
        verbose_name_plural = 'Empresas Prestadoras de Serviços'
        app_label = 'sistema'
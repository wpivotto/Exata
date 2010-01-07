# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.managers.managers import RevendaManager


class Revenda(models.Model):
    
    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    objects = RevendaManager()
    
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0
    quantidade_servicos.short_description = "Serviços Realizados"
    
    def total_a_receber(self):
        return self._valor_a_receber or 0
    total_a_receber.short_description = "Total a Receber"
    
    def total_recebido(self):
        return self._valor_recebido or 0
    total_recebido.short_description = "Total Recebido"
    
    def total_a_pagar(self):
        return self._valor_a_pagar or 0
    total_a_pagar.short_description = "Total a Pagar"
    
    def total_pago(self):
        return self._valor_a_pagar or 0
    total_pago.short_description = "Total Pago"
    
    def __unicode__(self):
        return self.cidade
    
    class Meta:
        verbose_name = 'Revenda Autorizada'
        verbose_name_plural = 'Revendas Autorizadas'
        unique_together = ['nome', 'cidade']
        app_label = 'sistema'
        


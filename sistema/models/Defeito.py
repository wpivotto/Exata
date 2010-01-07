# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.managers.managers import DefeitoManager

      
        
class Defeito(models.Model):
    
    nome = models.CharField(max_length=200)
    objects = DefeitoManager()
    
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0
    quantidade_servicos.short_description = 'Número de Ocorrências em Serviços'
    
    def __unicode__(self):
        return self.nome

        
    class Meta:
        verbose_name = 'Defeito de Aparelhos'
        verbose_name_plural = 'Banco de Defeitos'
        app_label = 'sistema'
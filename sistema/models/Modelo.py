# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.managers.managers import ModeloManager



class Modelo(models.Model):
    
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=15)
    objects = ModeloManager()
    
        
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0
        
    def defeito_mais_comum(self):
        return self._defeito_mais_comum or 'Nenhum'
    
    def __unicode__(self):
        return self.marca + " - " + self.modelo
        
    class Meta:
        verbose_name = 'Modelo Celular'
        verbose_name_plural = 'Banco de Modelos de Aparelhos'
        app_label = 'sistema'


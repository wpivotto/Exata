# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.managers.managers import ItensEnviadosManager

class ItensEnviados(models.Model):
    
    nome = models.CharField(max_length=200)
    objects = ItensEnviadosManager()
    
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0
    quantidade_servicos.short_description = 'Quantidade de Serviços'
    
    def __unicode__(self):
        return self.nome

        
    class Meta:
        verbose_name = 'Item Enviado'
        verbose_name_plural = 'Banco de Itens Enviados'
        app_label = 'sistema'
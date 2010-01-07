# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.models.Servico import Servico
from claro.sistema.managers.managers import ServicosManager 
import datetime

class Orcamento(Servico):
    
    data_aprovacao = models.DateTimeField(blank=True, null=True, verbose_name=u"Data Aprovação/Reprovação")
    aprovado = models.BooleanField()
    objects = ServicosManager()
    
    def save(self, *args, **kwargs):
        self.tipo = u'Orçamento'
        super(Orcamento, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = u'Orçamento'
        verbose_name_plural = u'Orçamentos Solicitados'
        app_label = 'sistema'
        


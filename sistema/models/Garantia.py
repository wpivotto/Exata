# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.models.Servico import Servico
from claro.sistema.managers.managers import ServicosManager 
import datetime

class Garantia(Servico):
    
    dpy_si = models.CharField(verbose_name="Código DPY/SI", max_length=10, null=True, blank=True)
    data_compra = models.DateField(null=True, blank=True)
    numero_nota_fiscal = models.IntegerField(max_length=4, null=True, blank=True)
    valor_aparelho = models.DecimalField(verbose_name="Valor do Aparelho (Em nota fiscal)", default=0.0, max_digits=5, decimal_places=2, null=True, blank=True)
    bloqueado = models.BooleanField(verbose_name="Aparelho Bloqueado (Sim/Não)")
    objects = ServicosManager()
    
    
    def aparelho_emprestado(self):
        return self.aparelho_emprestado_detail() != 'Nenhum'
    aparelho_emprestado.boolean = True
    
    def save(self, *args, **kwargs):
        self.tipo = 'Garantia'
        super(Garantia, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Garantia'
        verbose_name_plural = 'Garantias Solicitadas'
        app_label = 'sistema'
        




        




        

# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.models.OrdemServico import OrdemServico
from claro.sistema.models.Empresa import Empresa
from claro.sistema.managers.managers import SolicitacaoManager
import datetime

POSSE_ITENS = (
    ('1', 'Cliente'),
    ('2', 'Empresa'),
    ('3', 'Revenda'),
    
)

class Solicitacao(models.Model):
    
    ordemServico = models.OneToOneField(OrdemServico, help_text="Informe código da Ordem de Serviço")
    empresa = models.ForeignKey(Empresa)
    posse_aparelho = models.CharField(max_length=1, choices=POSSE_ITENS, null=True, blank=True)
    data_solicitacao = models.DateField(default=datetime.date.today(), blank=False)
    data_entrega = models.DateField(null=True, blank=True)
    objects = SolicitacaoManager()
    
    def __unicode__(self):
        return u"Solicitação No - " + str(self.id);
    
    def os(self):
        return self.ordemServico.id
    os.short_description = 'Referente a Ordem de Serviço'
    
    def cliente(self):
        return self.ordemServico.servico.cliente.nome
    cliente.short_description = 'Pedido pelo Cliente'
    
    
    class Meta:
        verbose_name = u'Solicitação de Novo Aparelho'
        verbose_name_plural = u'Solicitações de Novos Aparelhos'
        app_label = 'sistema'
    
        
    
    
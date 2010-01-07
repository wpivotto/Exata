# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.models.Servico import Servico
from claro.sistema.models.Defeito import Defeito

AVALIACAO = (
    ('1', 'Ótimo'),
    ('2', 'Bom'),
    ('3', 'Regular'),
    ('4', 'Ruim'),
)
    
class ServicoExecutado(models.Model):
    
    servico = models.CharField(max_length=200, unique = True)
    
    def __unicode__(self):
        return self.servico
    
    class Meta:
        verbose_name = u'Serviço Executado'
        verbose_name_plural = u'Serviços Executados'
        db_table = 'sistema_servicos_executados'
        app_label = 'sistema'
        
    

class MotivoExecucaoNegada(models.Model):
    
    motivo = models.CharField(max_length=200, unique = True)
    
    def __unicode__(self):
        return self.motivo
    
    class Meta:
        verbose_name = u'Motivo de Não Execução'
        verbose_name_plural = u'Motivos de Não Execução'
        db_table = 'sistema_motivo_execucao_negada'
        app_label = 'sistema'
        
        
class ExecucaoServico(models.Model):
    
    servico = models.OneToOneField(Servico, verbose_name="Referente ao Serviço")
    defeitos_constatados = models.ManyToManyField(Defeito,  verbose_name="Defeitos", null=True, blank=True)
    servicos_executados = models.ManyToManyField(ServicoExecutado,  verbose_name=u"Serviços Executados", null=True, blank=True)
    motivo_nao_execucao = models.ManyToManyField(MotivoExecucaoNegada,  verbose_name=u"Motivos", null=True, blank=True)
    avaliacao = models.CharField(max_length=1, choices=AVALIACAO, verbose_name=u"Avaliação", null=True, blank=True)
      
    def __unicode__(self):
        return u"Execução %s" % self.id;

   
    class Meta:
        verbose_name = u'Execução do Serviço'
        verbose_name_plural = u'Execução do Serviço'
        db_table = 'sistema_execucao_servico'
        app_label = 'sistema'
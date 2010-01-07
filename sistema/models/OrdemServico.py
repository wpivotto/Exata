# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.models.Servico import Servico
from claro.sistema.models.Empresa import Empresa
from claro.sistema.managers.managers import StatusOrdemServicoManager, OrdemServicosManager
import datetime


class StatusOrdemServico(models.Model):
    
    status = models.CharField(max_length=200)
    objects = StatusOrdemServicoManager()
    
    def __unicode__(self):
        return self.status
    
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0  
    quantidade_servicos.short_description = "Serviços"
   
    class Meta:
        verbose_name = 'Status da Ordem de Serviço'
        verbose_name_plural = 'Status das Ordens de Serviço'
        app_label = 'sistema'
        
    

class OrdemServico(models.Model):
    
    servico = models.OneToOneField(Servico, help_text = 'Informe o código do serviço')
    data_entrada = models.DateField(default=datetime.date.today(), verbose_name="Data Solicitação", blank=False)
    valor = models.FloatField(verbose_name="Valor Serviço", help_text = 'Formato XXX.XX')
    status = models.ForeignKey(StatusOrdemServico, blank=True, null=True)
    descricao = models.CharField(max_length=200,  blank=True, null=True)
    objects = OrdemServicosManager()
    
    
    
    def __unicode__(self):
        return "OS - " + str(self.id);
    
    def os(self):
        return self.id
    os.short_description = 'OS'
    
    def empresa(self):
        return self.servico.empresa.nome
    
    def cliente(self):
        return self.servico.cliente.nome
    cliente.short_description = 'Solicitante'
    
    def servico_solicitado(self):
        return self.servico.tipo
    servico_solicitado.short_description = 'Serviço Solicitado'
    
 
    def tempoCadastro(self):
        difference = datetime.date.today() - self.data_entrada
        return "%d dia(s)" % (difference.days)
    tempoCadastro.short_description = 'Tempo Cadastro'
    
    
    
    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        app_label = 'sistema'
    
    

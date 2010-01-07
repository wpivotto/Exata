# -*- coding: utf-8 -*- 
from django.db import models
from claro.sistema.models.OrdemServico import OrdemServico
from claro.sistema.models.Empresa import Empresa
from claro.sistema.models.Cliente import Cliente
from claro.contas.managers.managers import ContasManager, PagamentosManager
import datetime

FORMAS_PGTO = (
    ('1', 'Dinheiro'),
    ('2', 'Cheque'),
    ('3', 'Boleto'),
    ('4', u'Cartão'),
)

class Conta(models.Model):
    
    valor = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    acrescimo =  models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    desconto =  models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    forma_pgto =  models.CharField(max_length=1, choices=FORMAS_PGTO, null=True)
    data_vencimento =  models.DateField(blank=True, null=True)
    data_pagamento =  models.DateField(blank=True, null=True)
    ordem_servico = models.OneToOneField(OrdemServico, verbose_name="Referente a Ordem de Serviço")
    
    def __unicode__(self):
        return "Conta " + str(self.id)
    
    def vencida(self):
        if self.data_vencimento != None:
            return datetime.date.today() > self.data_vencimento
        return False
    vencida.boolean = True
    
    def os(self):
        return self.ordem_servico.id
    os.short_description = "Referente a Ordem de Serviço"
    
    class Meta:
        abstract = True
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ('-data_vencimento', 'valor')
        app_label = 'contas'
    

class ContaReceber(Conta):
    
    cliente = models.ForeignKey(Cliente, editable = False)
    objects = ContasManager()
    
    def __unicode__(self):
        return "Conta a Receber " + str(self.id)
    
    def a_receber(self):
        return (self.valor + self.acrescimo) - self.desconto
    
    def recebido(self):
        total = 0
        for pgto in PagamentoRecebido.objects.filter(conta=self, pago=True):
            total += pgto.valor
        return total
    recebido.short_description = 'Total Recebido'
    
    def quitada(self):
        return self.a_receber() == self.recebido()
    quitada.boolean = True
    
    def save(self, *args, **kwargs):
        self.cliente = self.ordem_servico.servico.cliente
        super(ContaReceber, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        app_label = 'contas'
    
    
    
class ContaPagar(Conta):
    
    empresa = models.ForeignKey(Empresa, editable = False)
    objects = ContasManager()
    
    def __unicode__(self):
        return "Conta a Pagar " + str(self.id)
    
    def a_pagar(self):
        return (self.valor + self.acrescimo) - self.desconto
    
    def pago(self):
        total = 0
        for pgto in PagamentoPago.objects.filter(conta=self, pago=True):
            total += pgto.valor   
        return total
    pago.short_description = 'Total Pago'
    
    def quitada(self):
        return self.a_pagar() == self.pago()
    quitada.boolean = True
    
    def save(self, *args, **kwargs):
        self.empresa = self.ordem_servico.servico.empresa
        super(ContaPagar, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        app_label = 'contas'
        
        

class Pagamento(models.Model):

    valor = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField()
    
    class Meta:
        abstract = True
        app_label = 'contas'

   
class PagamentoRecebido(Pagamento):
    
    data_recebimento = models.DateField(blank=True, null=True)
    conta = models.ForeignKey(ContaReceber, verbose_name="Referente a Conta")
    objects = PagamentosManager()
    
    def cliente(self):
        return self.conta.cliente.nome
    cliente.short_description = 'Em nome do Cliente'
    
    def os(self):
        return self.conta.ordem_servico.id
    
    def __unicode__(self):
        return u"Cobrança " + str(self.id)
    
    class Meta:
        verbose_name = u'Pagamento Recebido'
        verbose_name_plural = u'Pagamentos Recebidos'
        app_label = 'contas'
        

class PagamentoPago(Pagamento):
    
    data_pagamento = models.DateField(blank=True, null=True)
    conta = models.ForeignKey(ContaPagar, verbose_name="Referente a Conta")
    objects = PagamentosManager()
    
    def __unicode__(self):
        return "Pagamento " + str(self.id)
    
    def empresa(self):
        return self.conta.empresa.nome
    
    def os(self):
        return self.conta.ordem_servico.id
    
    class Meta:
        verbose_name = u'Pagamento Efetuado'
        verbose_name_plural = u'Pagamentos Efetuados'
        app_label = 'contas'
        
      

    
    

# -*- coding: utf-8 -*- 
from django.db import models
import datetime
from claro.sistema.models.Revenda import Revenda
from claro.sistema.models.Cliente import Cliente
from claro.sistema.models.Empresa import Empresa
from claro.sistema.models.Defeito import Defeito
from claro.sistema.models.ItensEnviados import ItensEnviados
from claro.sistema.models.Modelo import Modelo
from claro.sistema.managers.managers import StatusServicoManager, ServicosManager 
from claro.middleware.current_user import Users


        
class StatusServico(models.Model):
    
    status = models.CharField(max_length=200)
    objects = StatusServicoManager()
    
    def __unicode__(self):
        return self.status
    
    class Meta:
        verbose_name = 'Status do Servico Prestado'
        verbose_name_plural = 'Status dos Servicos Prestados'
        app_label = 'sistema'
    
    def quantidade_servicos(self):
        return self._quantidade_servicos or 0  
    quantidade_servicos.short_description = "Serviços"
    
   
           
class Servico(models.Model):
    
    revenda = models.ForeignKey(Revenda, editable = False)
    cliente = models.ForeignKey(Cliente, verbose_name="Solicitante")
    empresa = models.ForeignKey(Empresa)
    defeitos = models.ManyToManyField(Defeito, verbose_name="Defeitos Relatados Pelo Cliente")
    itens = models.ManyToManyField(ItensEnviados, help_text="Itens enviados para a empresa credenciada")
    status = models.ForeignKey(StatusServico)
    data_solicitacao = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    descricao = models.CharField(max_length=200, null=True,  blank=True)
    tipo = models.CharField(max_length=50, null=True,  blank=True)
    valor = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    
    #Detalhes do Aparelho
    numero = models.CharField(max_length=8)
    ddd = models.IntegerField("DDD")
    imei = models.CharField(max_length=15)
    operadora = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.ForeignKey(Modelo)
    
    porcentagem = models.DecimalField(default=20.0, max_digits=5, decimal_places=2, verbose_name="Porcentagem sobre custo (%)", help_text="Valor Ordem de Serviço = Valor Serviço x (Porcentagem / 100)")
    objects = ServicosManager()
    
    def aparelho_detail(self):
        return self.modelo.marca + " - " + self.modelo.modelo +" (" + str(self.ddd) + ") " + self.numero
    aparelho_detail.short_description = 'Aparelho'
   
    def aparelho_emprestado_detail(self):
        try:
            return AparelhoEmprestado.objects.get(servico = self)
        except:
            return 'Nenhum'
        
    def revenda_atual(self):
        return Users.current().revenda
        
    
    def save(self, *args, **kwargs):
        self.revenda = self.revenda_atual()
        super(Servico, self).save(*args, **kwargs)
        
    
    
    def __unicode__(self):
        return self.tipo + " " + str(self.id)  
    
    class Meta:
        verbose_name = 'Serviço Prestado'
        verbose_name_plural = 'Serviços Prestados'
        app_label = 'sistema'
        


POSSE_ITENS = (
    ('1', 'Cliente'),
    ('2', 'Empresa'),
    ('3', 'Revenda'),
)

class AparelhoEmprestado(models.Model):
    
    imei = models.CharField(max_length=15)
    modelo = modelo = models.ForeignKey(Modelo)
    posse_aparelho = models.CharField(max_length=1, choices=POSSE_ITENS, null=True, blank=True)
    carregador = models.BooleanField(verbose_name="Inclui Carregador ?")
    data_emprestimo = models.DateTimeField(default = datetime.datetime.now(),blank=True, null=True)
    data_devolucao = models.DateTimeField(blank=True, null=True)
    servico = models.OneToOneField(Servico)
    devolvido = models.BooleanField()
    
    def __unicode__(self):
        return "Modelo: " + self.modelo.marca + " - " + self.modelo.modelo +"  IMEI: " + self.imei + "  Carregador: " + self.com_carregador()
    
    def com_carregador(self):
        return self.carregador
    com_carregador.boolean = True
    
    def servico_id(self):
        return self.servico.id
    servico_id.short_description = "Referente ao Serviço"
    
    def cliente(self):
        return self.servico.cliente.nome
    cliente.short_description = "Para o Cliente"
    
    
    class Meta:
        verbose_name = u'Empréstimo de Aparelho'
        verbose_name_plural = u'Empréstimos de Aparelhos'
        app_label = 'sistema'
        


  
        
 
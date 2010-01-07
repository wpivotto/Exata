# -*- coding: utf-8 -*- 
from django.contrib import admin
from django import forms
from django.contrib.localflavor.br.forms import BRStateChoiceField, BRCPFField, BRCPFCNPJField
from django.contrib.admin.options import ModelAdmin, TabularInline

from claro.sistema.models.Cliente import Cliente
from claro.sistema.models.Modelo  import Modelo 
from claro.sistema.models.Servico import StatusServico, Servico, AparelhoEmprestado
from claro.sistema.models.Revenda  import Revenda 
from claro.sistema.models.Empresa  import Empresa 
from claro.sistema.models.Defeito import Defeito 
from claro.sistema.models.Orcamento  import Orcamento 
from claro.sistema.models.Garantia  import Garantia 
from claro.sistema.models.OrdemServico import StatusOrdemServico, OrdemServico
from claro.sistema.models.Solicitacao import Solicitacao
from claro.sistema.models.ItensEnviados import ItensEnviados
from claro.sistema.models.Execucao import *

from claro.contas.models.Conta import ContaPagar, ContaReceber

from claro.widgets.autocomplete import *

from batchadmin.admin import BatchModelAdmin
import datetime

''' 
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('os', 'cliente', 'tipo_servico', 'avaliacao', 'data_avaliacao')
    list_filter = ['avaliacao']
    search_fields = ['ordemServico__id']
    search_fields_verbose = ['Filtre por: cod. ordem serviço']
    raw_id_fields = ("ordemServico",)
    
    readonly_fields = {'admin':['data_avaliacao']}
    hidden_fields = {'admin':['avaliacao']}
'''

class MotivoExecucaoNegadaAdmin(admin.ModelAdmin):
    pass

class ServicoExecutadoAdmin(admin.ModelAdmin):
    pass

class ExecucaoServicoInline(admin.StackedInline):
    
    model = ExecucaoServico
    max_num = 1
    min_num = 1
    
    filter_horizontal  = ('defeitos_constatados', 'servicos_executados', 'motivo_nao_execucao',)
    
    fieldsets = (
        ('Defeitos constatados após a avaliação da empresa', {'fields': ('defeitos_constatados',)}),
        ('Serviços realizados pela empresa para solucionar os defeitos', {'fields': ('servicos_executados',)}), 
        ('Avaliação pelo cliente do serviço realizado', {'fields': ('avaliacao',)}),
        ('Motivos apontados pelo cliente para não aprovação do serviço', {'fields': ('motivo_nao_execucao',)}),
        
    )
    


class ModeloAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'marca', 'quantidade_servicos', 'defeito_mais_comum')
    list_filter = ['marca']
    search_fields = ['modelo']
    search_fields_verbose = ['Filtre por: modelo do aparelho']
    

class RevendaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'quantidade_servicos', 'total_a_receber', 'total_recebido', 'total_a_pagar', 'total_pago')
    list_filter = ('cidade',)
    
class StatusServicoAdmin(admin.ModelAdmin):
     list_display = ('status', 'quantidade_servicos')
     search_fields = ['status']
     search_fields_verbose = ['Filtre por: status']
     
class StatusOrdemServicoAdmin(admin.ModelAdmin):
     list_display = ('status', 'quantidade_servicos')
     search_fields = ['status']
     search_fields_verbose = ['Filtre por: status']

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'servicos', 'quantidade_servicos', 'valor_pago', 'valor_aberto',)
    
    list_filter = (
                   'cidade',
                   'servicos',
    )
    
class DefeitoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade_servicos']
    
class ItensEnviadosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade_servicos']
    

class OrcamentoAdmin(AutocompleteModelAdmin, BatchModelAdmin):
   
    related_search_fields = {'cliente': ('nome',),
                             'modelo': ('marca',),}
    
    list_display = (
                    'id',
                    'aparelho_detail',
                    'cliente',
                    'revenda',
                    'empresa',
                    'valor',
                    'status',
                    'aprovado',
    )
    
    search_fields = ('id', 'cliente__nome', 'revenda__nome',)
    
    search_fields_verbose = ['Filtre por: id', 'nome cliente', 'nome da revenda']
    
    filter_horizontal = ("defeitos", "itens",)
    
    date_hierarchy = 'data_solicitacao'  
 
    fieldsets = (
        ('Dados da Solicitacao', {'fields': ('empresa', 'cliente')}),
        ('Dados do Aparelho', {'fields': ('numero', 'ddd', 'imei', 'operadora', 'modelo', 'defeitos')}), 
        ('Dados do Orcamento', {'fields': ('descricao', 'valor', 'porcentagem', 'itens', 'status')}),
        ('Dados Avancados', {
                             'fields': ('data_solicitacao', 'data_aprovacao', 'aprovado'),
                             'classes': ('collapse',),
                            }
        ),
    )
    
    list_filter = (
                   'data_solicitacao',
                   'status',
                   'aprovado',
                   'revenda',
                   'empresa',             
    )
    
    batch_actions = ['aprovar', 'reprovar']
    
    inlines = [ExecucaoServicoInline]
    
    def aprovar(self, request, objects):
        self.aprovacao(request, objects, True)
    aprovar.short_description = "Marcar como Aprovado"
    
    def reprovar(self, request, objects):
        self.aprovacao(request, objects, False)
    reprovar.short_description = "Marcar como Reprovado"
    
    def aprovacao(self, request, objects, status):
        try:
            for obj in objects:
                obj.aprovado = status
                obj.data_aprovacao = datetime.datetime.now()
                obj.save()
            self.message_user(request, "%s Orçamentos modificados com sucesso " % (objects.count()))
        except Exception,e:
            self.message_user(request, "Erro ao alterar orçamentos: " + str(e))

    
    
    
   
class AparelhoEmprestadoAdmin(AutocompleteModelAdmin, BatchModelAdmin): 
    
    list_display = (
                    'id',
                    'modelo',
                    'imei',
                    'cliente',
                    'servico_id',
                    'data_emprestimo',
                    'devolvido',
                    'data_devolucao',
                    
    )
    
    raw_id_fields = ("servico",)
    
    date_hierarchy = 'data_emprestimo' 
    
    related_search_fields = {'modelo': ('marca',),}
    
    search_fields = ('servico__id', 'servico__cliente__nome',)
    
    search_fields_verbose = ['Filtre por: cod. serviço', 'nome do cliente']
    
    list_filter = ('data_emprestimo', 'modelo',)
    
    batch_actions = ['devolver']
    
    def devolver(self, request, objects):
        try:
            for obj in objects:
                obj.devolvido = True
                obj.data_devolucao = datetime.datetime.now()
                obj.posse_aparelho = '3'
                obj.save()
            self.message_user(request, "%s Aparelhos modificados com sucesso " % (objects.count()))
        except Exception,e:
            self.message_user(request, "Erro ao alterar aparelhos emprestados: " + str(e))
    devolver.short_description = "Marcar como Devolvido"
    
    
    
    
class AparelhoEmprestadoInline(admin.StackedInline):
    
    model = AparelhoEmprestado
    max_num = 1
    raw_id_fields = ("modelo",)
       
class GarantiaAdmin(AutocompleteModelAdmin):
    
    related_search_fields = {'cliente': ('nome',),
                             'modelo': ('marca',),}
    
    list_display = (
                    'id',
                    'aparelho_detail',
                    'cliente',
                    'revenda',
                    'empresa',
                    'aparelho_emprestado',
                    'status',
    )
    
    search_fields = ('cliente__nome', 'id',)
    
    search_fields_verbose = ['Filtre por: nome cliente', 'cod. serviço']
    
    filter_horizontal = ("defeitos", "itens",)
    
    date_hierarchy = 'data_solicitacao' 
    
    list_filter = (
                   'data_solicitacao',
                   'empresa',
                   'revenda',
    )
    
    inlines = [AparelhoEmprestadoInline, ExecucaoServicoInline]
    
    fieldsets = (
        ('Dados da Solicitacao', {'fields': ('empresa', 'cliente')}),
        ('Dados do Aparelho', {'fields': ('numero', 'ddd', 'imei', 'operadora', 'modelo', 'defeitos')}), 
        ('Dados do Servico', {'fields': ('descricao', 'valor', 'porcentagem', 'itens', 'status')}),
        ('Dados Extras', {
                             'fields': ('data_solicitacao', 'dpy_si', 'numero_nota_fiscal', 'valor_aparelho', 'data_compra', 'bloqueado'),
                             'classes': ('collapse',),
                            }
        ),
    )
 

class ClienteForm(forms.ModelForm):
    
    estado = BRStateChoiceField(initial='SC')
    id_fiscal = BRCPFCNPJField(help_text='Pessoa Fisica = CPF, Pessoa Juridica = CNPJ')
    
    class Meta:
        model = Cliente
    
    
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome','id_fiscal', 'cidade', 'logradouro', 'bairro', 'valor_total','quantidade_servicos')
    
    search_fields = ('nome','id_fiscal',)
    
    search_fields_verbose = ['Filtre por: nome', 'cpf/cnpj']
    
    fieldsets = (
        ('Sobre o Cliente', {'fields': ('nome', 'id_fiscal', 'fone', 'email', 'data_nascimento')}),
        ('Endereco', {'fields': ('logradouro', 'bairro', 'cidade', 'estado', 'CEP', 'referencia', 'numero', 'complemento')}),
    )
    
    
    list_filter = ('cidade','CEP','bairro',)
    
    form = ClienteForm
    
    

    
class ServicoAdmin(AutocompleteModelAdmin):
    
    list_display = (
                    'id',
                    'aparelho_detail',
                    'tipo',
                    'cliente',
                    'revenda',
                    'status',
    )
    
    related_search_fields = {'cliente': ('nome',),
                             'modelo': ('marca',),}
    
    search_fields = ('cliente__nome', 'id',)
    
    search_fields_verbose = ['Filtre por: nome cliente', 'cod. serviço']
    
    filter_horizontal = ("defeitos", "itens",)
    
    date_hierarchy = 'data_solicitacao' 
    
    list_filter = (
                   'data_solicitacao',
                   'empresa',
                   'revenda',
                   'status',
    )
    
    fieldsets = (
        ('Dados da Solicitacao', {'fields': ('empresa', 'cliente')}),
        ('Dados do Aparelho', {'fields': ('numero', 'ddd', 'imei', 'operadora', 'modelo', 'defeitos')}), 
        ('Dados do Servico', {'fields': ('descricao', 'valor', 'itens', 'status')}),
    
    )
    
    inlines = [ExecucaoServicoInline]
      

class InlineContaReceber(admin.StackedInline):
    model = ContaReceber
    max_num = 1
    min_num = 1
    extra = 1
    
class InlineContaPagar(admin.StackedInline):
    model = ContaPagar
    max_num = 1
    min_num = 1
    extra = 1


class PagamentoRecebidoAdmin(BatchModelAdmin):
    list_display = ('id', 'data_vencimento', 'data_pagamento', 'valor','cliente', 'os', 'pago')
    date_hierarchy = 'data_pagamento'  
    list_filter = ('data_pagamento', 'pago')
    search_fields = ('ordemservico__id', 'ordemservico__servico__cliente__nome',)
    search_fields_verbose = ['Filtre por: nome cliente', 'cod. ordem serviço']
    raw_id_fields = ("ordemservico",)
    
    batch_actions = ['pago', 'excluir']

    list_per_page = 40
    
    def pago(self, request, objects):
        try:
            for obj in objects:
                obj.pago = True
                obj.data_pagamento = datetime.date.today()
                obj.save()
            self.message_user(request, "%s Pagamentos modificados com sucesso " % (objects.count()))
        except Exception,e:
            self.message_user(request, "Erro ao alterar pagamentos: " + str(e))
    pago.short_description = "Marcar como Pago"
    
    def excluir(self, request, objects):
        try:
            for obj in objects:
                obj.delete()
            self.message_user(request, "%s Pagamentos excluídos com sucesso " % (objects.count()))
        except Exception,e:
            self.message_user(request, "Erro ao excluir pagamentos: " + str(e))
    excluir.short_description = "Excluir Pagamento"


class PagamentoPagoAdmin(BatchModelAdmin):
    list_display = ('id', 'data_vencimento', 'data_pagamento', 'valor','empresa', 'os', 'pago')
    date_hierarchy = 'data_pagamento'  
    list_filter = ('data_pagamento', 'pago', 'empresa',)
    search_fields = ('ordemservico__id', 'empresa__nome',)
    search_fields_verbose = ['Filtre por: empresa', 'cod. ordem serviço']
    raw_id_fields = ("ordemservico",)
    
    batch_actions = ['pago', 'excluir']

    list_per_page = 40
    
    def pago(self, request, objects):
        try:
            for obj in objects:
                obj.pago = True
                obj.data_pagamento = datetime.date.today()
                obj.save()
            self.message_user(request, "%s Pagamentos modificados com sucesso " % (objects.count()))
        except Exception,e:
            self.message_user(request, "Erro ao alterar pagamentos: " + str(e))
    pago.short_description = "Marcar como Pago"
    
    def excluir(self, request, objects):
        try:
            for obj in objects:
                obj.delete()
            self.message_user(request, "%s Pagamentos excluídos com sucesso " % (objects.count()))
        except Exception,e:
            self.message_user(request, "Erro ao excluir pagamentos: " + str(e))
    excluir.short_description = "Excluir Pagamento"
    
    
   
    
class OrdemServicoAdmin(admin.ModelAdmin):
    
    list_display = ('os', 
                    'data_entrada', 
                    'cliente', 
                    'servico_solicitado', 
                    'empresa', 
                    'tempoCadastro', 
                    'valor', 
                    'status',)
    
    date_hierarchy = 'data_entrada'  
    list_filter = ('data_entrada', 'status',)
    search_fields = ('servico__cliente__nome','servico__empresa__nome', 'servico__revenda__cidade', 'id',)
    search_fields_verbose = ['Filtre por: nome cliente', 'cod. ordem serviço', 'revenda', 'empresa']
    raw_id_fields = ("servico",)
    
    
    inlines = [InlineContaPagar, InlineContaReceber, ]
    

class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('os', 'cliente','data_solicitacao', 'data_entrega', 'empresa', 'posse_aparelho')
    date_hierarchy = 'data_solicitacao'  
    list_filter = ('data_solicitacao', 'empresa')
    search_fields = ('ordemServico__servico__cliente__nome', 'id',)
    search_fields_verbose = ['Filtre por: nome cliente', 'cod. solicitacao']
    
    raw_id_fields = ("ordemServico",)
    


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(StatusServico, StatusServicoAdmin)
admin.site.register(StatusOrdemServico, StatusOrdemServicoAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Defeito, DefeitoAdmin)
admin.site.register(Orcamento, OrcamentoAdmin)
admin.site.register(Garantia, GarantiaAdmin)
admin.site.register(Revenda, RevendaAdmin)  
admin.site.register(Servico, ServicoAdmin) 
admin.site.register(OrdemServico, OrdemServicoAdmin) 
admin.site.register(Solicitacao, SolicitacaoAdmin) 
admin.site.register(ItensEnviados, ItensEnviadosAdmin) 
admin.site.register(AparelhoEmprestado, AparelhoEmprestadoAdmin)
admin.site.register(MotivoExecucaoNegada, MotivoExecucaoNegadaAdmin) 
admin.site.register(ServicoExecutado, ServicoExecutadoAdmin) 

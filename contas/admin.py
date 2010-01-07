# -*- coding: utf-8 -*- 
from django.contrib import admin
from claro.contas.models.Conta import *
from batchadmin.admin import BatchModelAdmin
import datetime




class ContaAdmin(admin.ModelAdmin):
    pass

class InlinePagamentoRecebido(admin.StackedInline):
    model = PagamentoRecebido
    max_num = 3
    min_num = 1
    extra = 1
    
class InlinePagamentoPago(admin.StackedInline):
    model = PagamentoPago
    max_num = 3
    min_num = 1
    extra = 1
    

class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'os', 'a_receber', 'recebido', 'data_vencimento', 'vencida', 'quitada')
    raw_id_fields = ('ordem_servico',) 
    list_filter = ('data_vencimento',)
    
    date_hierarchy = 'data_pagamento'  
    
    search_fields = ('ordem_servico__id', 'rdem_servico__servico__cliente__nome',)
    search_fields_verbose = ['Filtre por: nome cliente', 'cod. ordem serviço']
    
    inlines = [InlinePagamentoRecebido]
    
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa', 'os', 'a_pagar', 'pago', 'data_vencimento', 'vencida', 'quitada')
    raw_id_fields = ('ordem_servico',) 
    list_filter = ('data_vencimento',)
    
    date_hierarchy = 'data_pagamento'  
    
    search_fields = ('ordem_servico__id', 'ordem_servico__servico__empresa__nome',)
    search_fields_verbose = ['Filtre por: nome empresa', 'cod. ordem serviço']
    
    inlines = [InlinePagamentoPago]
    
    


class PagamentoPagoAdmin(BatchModelAdmin):
    list_display = ('id', 'data_vencimento', 'data_pagamento', 'valor','empresa', 'os', 'pago')
    date_hierarchy = 'data_pagamento'  
    list_filter = ('data_pagamento', 'pago',)
    raw_id_fields = ('conta',)
    
    search_fields = ('conta__ordem_servico__id', 'conta__ordem_servico__servico__empresa__nome',)
    search_fields_verbose = ['Filtre por: nome empresa', 'cod. ordem serviço']
    
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

class PagamentoRecebidoAdmin(BatchModelAdmin):
    list_display = ('id', 'data_vencimento', 'data_recebimento', 'valor','cliente', 'os', 'pago')
    date_hierarchy = 'data_recebimento'  
    list_filter = ('data_recebimento', 'pago',)
    raw_id_fields = ('conta',)
    
    search_fields = ('conta__ordem_servico__id', 'conta__ordem_servico__servico__cliente__nome',)
    search_fields_verbose = ['Filtre por: nome cliente', 'cod. ordem serviço']
    
    batch_actions = ['pago', 'excluir']

    list_per_page = 40
    
    def pago(self, request, objects):
        try:
            for obj in objects:
                obj.pago = True
                obj.data_recebimento = datetime.date.today()
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



#admin.site.register(Conta, ContaAdmin)
admin.site.register(ContaReceber, ContaReceberAdmin)
admin.site.register(ContaPagar, ContaPagarAdmin)
admin.site.register(PagamentoPago, PagamentoPagoAdmin)
admin.site.register(PagamentoRecebido, PagamentoRecebidoAdmin)




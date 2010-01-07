from django.db import models
from claro.middleware.current_user import Users

class ModeloManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(ModeloManager, self).get_query_set()
        return query_set.extra(select = {'_quantidade_servicos': """select count(*) from sistema_servico, sistema_modelo
                                          where sistema_servico.modelo_id = sistema_modelo.id""",
                                          '_defeito_mais_comum': """Select d.nome from 
                                            sistema_servico s, sistema_servico_defeitos sd, sistema_defeito d, sistema_modelo m
                                            where 
                                            sd.defeito_id = d.id and
                                            sd.servico_id  = s.id and
                                            s.modelo_id = m.id 
                                            group by d.id 
                                            order by count(*)
                                            desc LIMIT 1""",
                                         }
)
        

class ClienteManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(ClienteManager, self).get_query_set()
        return query_set.extra(select = {
                                          '_quantidade_servicos': """select count(*) from sistema_servico
                                          where sistema_servico.cliente_id = sistema_cliente.id""",
                                          '_valor_total': """select sum(pgto.valor) from contas_contareceber conta, contas_pagamentorecebido pgto
                                          where conta.id = pgto.conta_id and
                                          conta.cliente_id = sistema_cliente.id and
                                          pgto.pago = 0""",
                                         }
)
        

class RevendaManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(RevendaManager, self).get_query_set()
        return query_set.extra(select = {'_quantidade_servicos': """select count(*) from sistema_servico
                                          where sistema_servico.revenda_id = sistema_revenda.id""",
                                          
                                          
                                          '_valor_a_receber': """select sum(pgto.valor) from sistema_servico, sistema_ordemservico, 
                                          contas_contareceber conta, contas_pagamentorecebido pgto
                                          where sistema_servico.revenda_id = sistema_revenda.id and
                                          sistema_servico.id = sistema_ordemservico.servico_id and
                                          conta.ordem_servico_id = sistema_ordemservico.id and
                                          conta.id = pgto.conta_id and
                                          pgto.pago = 0""",
                                          
                                          
                                         '_valor_recebido': """select sum(pgto.valor) from sistema_servico, sistema_ordemservico, 
                                          contas_contareceber conta, contas_pagamentorecebido pgto
                                          where sistema_servico.revenda_id = sistema_revenda.id and
                                          sistema_servico.id = sistema_ordemservico.servico_id and
                                          conta.ordem_servico_id = sistema_ordemservico.id and
                                          conta.id = pgto.conta_id and
                                          pgto.pago = 1""",
                                          
                                          '_valor_a_pagar': """select sum(pgto.valor) from sistema_servico, sistema_ordemservico, 
                                          contas_contapagar conta, contas_pagamentopago pgto
                                          where sistema_servico.revenda_id = sistema_revenda.id and
                                          sistema_servico.id = sistema_ordemservico.servico_id and
                                          conta.ordem_servico_id = sistema_ordemservico.id and
                                          conta.id = pgto.conta_id and
                                          pgto.pago = 0""",
                                          
                                          '_valor_pago': """select sum(pgto.valor) from sistema_servico, sistema_ordemservico, 
                                          contas_contapagar conta, contas_pagamentopago pgto
                                          where sistema_servico.revenda_id = sistema_revenda.id and
                                          sistema_servico.id = sistema_ordemservico.servico_id and
                                          conta.ordem_servico_id = sistema_ordemservico.id and
                                          conta.id = pgto.conta_id and
                                          pgto.pago = 1""",
                                         
                                         }
        
)
        

class EmpresaManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(EmpresaManager, self).get_query_set()
        return query_set.extra(select = {'_quantidade_servicos': """select count(*) from sistema_servico
                                          where sistema_servico.empresa_id = sistema_empresa.id""",
                                          '_valor_pago': """select sum(pgto.valor) from contas_contapagar conta, contas_pagamentopago pgto
                                          where conta.id = pgto.conta_id and
                                          conta.empresa_id = sistema_empresa.id and
                                          pgto.pago = 1""",
                                          '_valor_em_aberto': """select sum(pgto.valor) from contas_contapagar conta, contas_pagamentopago pgto
                                          where conta.id = pgto.conta_id and
                                          conta.empresa_id = sistema_empresa.id and
                                          pgto.pago = 0"""
                                         }
)  
        
        
class DefeitoManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(DefeitoManager, self).get_query_set()
        return query_set.extra(select = {'_quantidade_servicos': """select count(*) from sistema_servico_defeitos
                                          where sistema_servico_defeitos.defeito_id = sistema_defeito.id""",
                                         }
)  
        
        
class StatusServicoManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(StatusServicoManager, self).get_query_set()
        return query_set.extra(select = {
                                         '_quantidade_servicos': """select count(*) from sistema_servico
                                          where sistema_servico.status_id = sistema_statusservico.id""",
                                         }
)
        

class StatusOrdemServicoManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(StatusOrdemServicoManager, self).get_query_set()
        return query_set.extra(select = {
                                         '_quantidade_servicos': """select count(*) from sistema_ordemservico
                                          where sistema_ordemservico.status_id = sistema_statusordemservico.id""",
                                         }
)

class ItensEnviadosManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(ItensEnviadosManager, self).get_query_set()
        return query_set.extra(select = {
                                         '_quantidade_servicos': """select count(*) from sistema_servico_itens
                                          where sistema_servico_itens.itensenviados_id = sistema_itensenviados.id""",
                                         }
)

class ServicosManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(ServicosManager, self).get_query_set()
        revenda = Users.current().revenda
        if revenda != None and revenda.cidade != 'Pinhalzinho':
            return query_set.filter(revenda = revenda)
        else:
            return query_set;
            
        
    
class OrdemServicosManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(OrdemServicosManager, self).get_query_set()
        revenda = Users.current().revenda
        if revenda != None and revenda.cidade != 'Pinhalzinho':
            return query_set.filter(servico__revenda = revenda)
        else:
            return query_set;
    
class SolicitacaoManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(SolicitacaoManager, self).get_query_set()
        revenda = Users.current().revenda
        if revenda != None and revenda.cidade != 'Pinhalzinho':
            return query_set.filter(ordemServico__servico__revenda = revenda)
        else:
            return query_set;

        
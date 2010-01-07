from django.db import models
from claro.middleware.current_user import Users

    
class ContasManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(ContasManager, self).get_query_set()
        revenda = Users.current().revenda
        if revenda != None and revenda.cidade != 'Pinhalzinho':
            return query_set.filter(ordem_servico__servico__revenda = revenda)
        else:
            return query_set;
        ''' 
        if user.has_perm('auth.acesso_contas'):
            return query_set 
        else:
            return query_set.filter(ordem_servico__servico__revenda = revenda)
        ''' 
    
class PagamentosManager(models.Manager):
    
    def get_query_set(self):
        query_set = super(PagamentosManager, self).get_query_set()
        revenda = Users.current().revenda
        if revenda != None and revenda.cidade != 'Pinhalzinho':
            return query_set.filter(conta__ordem_servico__servico__revenda = revenda)
        else:
            return query_set;

        
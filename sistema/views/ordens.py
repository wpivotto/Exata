# -*- coding: utf-8 -*- 
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from claro.sistema.models.OrdemServico  import OrdemServico 
from claro.sistema.models.Servico import Servico 
from claro.sistema.models.Garantia import Garantia 
from claro.sistema.models.Orcamento import Orcamento 

import datetime 
import math


def garantia(request, servico_id):
    msg = gerarOrdem(servico_id)
    request.user.message_set.create(message = msg)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'claro/admin/sistema/garantia/%s/'%servico_id))
    
def orcamento(request, servico_id):
    msg = gerarOrdem(servico_id)
    request.user.message_set.create(message = msg)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'claro/admin/sistema/orcamento/%s/'%servico_id))
     
def gerarOrdem(servico_id):
    
        servico = Servico.objects.get(id=servico_id)
        os = OrdemServico()
        os.servico = servico
        os.valor = math.ceil(servico.valor + (servico.valor * (servico.porcentagem / 100)))
        os.data_entrada = datetime.date.today()
        
        try:
            os.save()
            return 'Ordem de Servico gerada com sucesso!'
        except Exception,e:  
            return 'Erro ao gerar ordem de servico: ' + str(e)
    
        
# -*- coding: utf-8 -*- 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from geraldo.generators import PDFGenerator

from claro.sistema.relatorios.reports import RelatorioOrdemServico, RelatorioSolicitacao

from claro.sistema.models.OrdemServico  import OrdemServico 
from claro.sistema.models.Solicitacao import Solicitacao 

from django.shortcuts import render_to_response
import datetime 




def getResponse():
    response = HttpResponse()
    response['Content-Type'] = 'application/pdf'
    response['Pragma'] = 'public'
    response['Expires'] = '0'
    response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
    response['Content-Disposition'] = 'attachment; filename=relatorio_%s' % datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
    return response
    

def ordem_servico(request, os_id):
    
    response = getResponse()
    
    try: 
        
        ordem = OrdemServico.objects.filter(id=os_id)
        
        report = RelatorioOrdemServico(queryset = ordem)
        report.generate_by(PDFGenerator, filename = response)
    
    except Exception,e:
            request.user.message_set.create(message = 'Erro ao gerar listagem de ordens de servico: ' + str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'claro/admin/sistema/ordemservico/%s/'%os_id))
        
    return response


def solicitacao(request, param_id):
    
    response = getResponse()
    
    try: 
        
        solicitacao = Solicitacao.objects.filter(id = param_id)
       
        report = RelatorioSolicitacao(queryset = solicitacao)
        report.generate_by(PDFGenerator, filename = response)
    
    except Exception,e:
            request.user.message_set.create(message = 'Erro ao gerar relatorio de solicitacao: ' + str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'claro/admin/sistema/solicitacao/%s/'%param_id))
        
    return response
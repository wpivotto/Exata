# -*- coding: utf-8 -*- 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from claro.sistema.models.Servico import Servico 
from django.core.mail import EmailMessage



def send(request, servico_id):
    
        servico = Servico.objects.get(id=servico_id)
        
        try:
            
            recipient = servico.cliente.email
            subject = 'Mensagem Automatica'
            body = "Recebemos orcamento no valor de R$" + str(servico.valor) + \
               ", referente ao pedido realizado no dia " + str(servico.data_solicitacao) + \
               " pelo Sr(a) " + servico.cliente.nome + \
               ". Favor entrar em contato para aprovacao/reprovacao do mesmo. "
              
            email = EmailMessage(recipient = recipient, subject = subject, body = body)
            email.send(fail_silently = False)
            
            request.user.message_set.create(message = 'Mensagem de notificacao enviada com sucesso')
            
        except:
            request.user.message_set.create(message = 'Erro ao enviar mensagem de notificacao')
    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'claro/admin/sistema/orcamento/%s/'%servico_id))



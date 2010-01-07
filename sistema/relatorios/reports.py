# -*- coding: utf-8 -*-
from geraldo import Report, ReportBand, ObjectValue, ReportBand, landscape,\
        SystemField, BAND_WIDTH, Label, SubReport, Image

from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A5
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class RelatorioOrdemServico(Report):
    title = 'Relatório de Ordem de Serviço'
    print_if_empty = True
    #page_size = landscape(A5)
    margin_top = 0.5*cm
    margin_bottom = 0.5*cm
    margin_left = 1*cm
    margin_right = 1*cm
    
    class band_page_header(ReportBand):
        height = 1.5*cm
        elements = [
                Image(left=1*cm, top=0*cm, filename='C:/Python25/Scripts/claro/media/img/logo.png', style={'alignment': TA_LEFT}),
                SystemField(expression=u'Página %(page_number)d de %(page_count)d', top=0.7*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 8, 'alignment': TA_RIGHT}),
                SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 11, 'alignment': TA_CENTER}),
        ]
        borders = {'bottom': True}
    
    
    class band_detail(ReportBand):
        height = 0.4*cm
        elements=(
                Label(text='OS:', left=1*cm, top=1*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='id', left=5*cm, top=1*cm),
                Label(text='Data Solicitação:', left=1*cm, top=2*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='data_entrada', left=5*cm, top=2*cm,get_value=lambda instance: instance.data_entrada.strftime('%d/%m/%Y')),
                Label(text='Revenda:', left=1*cm, top=3*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.revenda.nome', left=5*cm, top=3*cm),
                Label(text='Empresa:', left=1*cm, top=4*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.empresa.nome', left=5*cm, top=4*cm),
                Label(text='Servico:', left=1*cm, top=5*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.tipo', left=5*cm, top=5*cm),
                Label(text='Cliente:', left=1*cm, top=6*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.cliente.nome', left=5*cm, top=6*cm),
                Label(text='CPF/CNPJ:', left=1*cm, top=7*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.cliente.id_fiscal', left=5*cm, top=7*cm),
                Label(text='Contado:', left=1*cm, top=8*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.cliente.fone', left=5*cm, top=8*cm),
                Label(text='Modelo:', left=1*cm, top=9*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.modelo.modelo', left=5*cm, top=9*cm),
                Label(text='Marca:', left=1*cm, top=10*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.modelo.marca', left=5*cm, top=10*cm),
                Label(text='IMEI:', left=1*cm, top=11*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.imei', left=5*cm, top=11*cm),
                Label(text='Defeitos:', left=1*cm, top=12*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),
                Label(text='Itens Enviados:', left=11.5*cm, top=12*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),
                
                Label(text='COMPROVANTE DO CLIENTE', top=18*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 8, 'alignment': TA_CENTER}),
                Label(text='Nome:', left=0.5*cm, top=19*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.cliente.nome', left=5*cm, top=19*cm),
                Label(text='Data Solicitação:', left=0.5*cm, top=20*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='data_entrada', left=5*cm, top=20*cm,get_value=lambda instance: instance.data_entrada.strftime('%d/%m/%Y')),
                Label(text='Modelo:', left=8*cm, top=20*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.modelo.modelo', left=9.5*cm, top=19.9*cm),
                Label(text='Marca:', left=13*cm, top=20*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='servico.modelo.marca', left=14.5*cm, top=19.9*cm),
                Label(text='Serviço Prestado:', left=0.5*cm, top=21*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='servico.tipo', left=5*cm, top=20.9*cm),
                Label(text='O aparelho NÂO retirado dentro de 60 dias será vendido posteriormente para cobrir as despesas do conserto, conforme lei 4.131/08. Aparelho reprovado não será avisado. Para a retirada o cliente deve procurar a loja.', left=0.5*cm, top=22*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),
                Label(text='Aparelho Emprestado:', left=0.5*cm, top=23.5*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='servico.aparelho_emprestado_detail', left=5*cm, top=23.5*cm, width=BAND_WIDTH),
                
        )
        
        
    
    class band_page_footer(ReportBand):
        height = 9.5*cm
        elements = [
            Label(text='Pinhalzinho - SC', top=8.5*cm, left=0.5*cm),
            SystemField(expression='Gerado em %(now:%d/%m/%Y)s às %(now:%H:%M)s   ', top=8.5*cm, left=13.5*cm),
        ]
        borders = {'top': True, 'bottom': True, 'left': True, 'right': True,}
    
    
    subreports = [
                  SubReport(
                            queryset_string = '%(object)s.servico.defeitos.all()',
                            band_detail = ReportBand(
                                                     height=0.5*cm,
                                                     elements=[
                                                               ObjectValue(attribute_name='nome', left=5*cm, top=11.6*cm),
                                                    ]
                            ),
                ),
                SubReport(
                            queryset_string = '%(object)s.servico.itens.all()',
                            band_detail = ReportBand(  
                                                     height=0.5*cm, 
                                                     elements=[
                                                               ObjectValue(attribute_name='nome', left=15*cm, top=10.5*cm),
                                                    ]
                            ),
                ),
    ]  
    




class RelatorioSolicitacao(Report):
    title = 'Relatorio de Solicitacao de Aparelho Novo'
    print_if_empty = True
    #page_size = landscape(A5)
    margin_top = 0.5*cm
    margin_bottom = 0.5*cm
    margin_left = 1*cm
    margin_right = 1*cm
    
    class band_page_header(ReportBand):
        height = 1.5*cm
        elements = [
                Image(left=1*cm, top=0*cm, filename='C:/Python25/Scripts/claro/media/img/logo.png', style={'alignment': TA_LEFT}),
                SystemField(expression=u'Página %(page_number)d de %(page_count)d', top=0.7*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 8, 'alignment': TA_RIGHT}),
                SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 11, 'alignment': TA_CENTER}),
        ]
        borders = {'bottom': True}
    

    class band_detail(ReportBand):
        height = 0.4*cm
        elements=(
                Label(text='OS:', left=1*cm, top=1*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='ordemServico.id', left=5*cm, top=1*cm),
                Label(text='Data Solicitação:', left=1*cm, top=2*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='data_solicitacao', left=5*cm, top=2*cm,get_value=lambda instance: instance.data_solicitacao.strftime('%d/%m/%Y')),
                Label(text='Revenda:', left=1*cm, top=3*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.revenda.nome', left=5*cm, top=3*cm),
                Label(text='Empresa:', left=1*cm, top=4*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.empresa.nome', left=5*cm, top=4*cm),
                Label(text='Servico:', left=1*cm, top=5*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.tipo', left=5*cm, top=5*cm),
                Label(text='Cliente:', left=1*cm, top=6*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.cliente.nome', left=5*cm, top=6*cm),
                Label(text='CPF/CNPJ:', left=1*cm, top=7*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.cliente.id_fiscal', left=5*cm, top=7*cm),
                Label(text='Contado:', left=1*cm, top=8*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.cliente.fone', left=5*cm, top=8*cm),
                Label(text='Modelo:', left=1*cm, top=9*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.modelo.modelo', left=5*cm, top=9*cm),
                Label(text='Marca:', left=1*cm, top=10*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.modelo.marca', left=5*cm, top=10*cm),
                Label(text='IMEI:', left=1*cm, top=11*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.imei', left=5*cm, top=11*cm),
                Label(text='Defeitos:', left=1*cm, top=12*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),
                Label(text='Itens Enviados:', left=11.5*cm, top=12*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),
                
                Label(text='COMPROVANTE DO CLIENTE', top=18*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 8, 'alignment': TA_CENTER}),
                Label(text='Nome:', left=0.5*cm, top=19*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.cliente.nome', left=5*cm, top=19*cm),
                Label(text='Data Solicitação:', left=0.5*cm, top=20*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='ordemServico.data_solicitacao', left=5*cm, top=20*cm,get_value=lambda instance: instance.data_solicitacao.strftime('%d/%m/%Y')),
                Label(text='Modelo:', left=8*cm, top=20*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.modelo.modelo', left=9.5*cm, top=19.9*cm),
                Label(text='Marca:', left=13*cm, top=20*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),ObjectValue(attribute_name='ordemServico.servico.modelo.marca', left=14.5*cm, top=19.9*cm),
                Label(text='Serviço Prestado:', left=0.5*cm, top=21*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='ordemServico.servico.tipo', left=5*cm, top=20.9*cm),
                Label(text='O aparelho NÂO retirado dentro de 60 dias será vendido posteriormente para cobrir as despesas do conserto, conforme lei 4.131/08. Aparelho reprovado não será avisado. Para a retirada o cliente deve procurar a loja.', left=0.5*cm, top=22*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}),
                Label(text='Aparelho Emprestado:', left=0.5*cm, top=23.5*cm, style={'fontName': 'Helvetica-Bold', 'fontSize': 8,}), ObjectValue(attribute_name='ordemServico.servico.aparelho_emprestado_detail', left=5*cm, top=23.5*cm, width=BAND_WIDTH),
        
        )

    
    class band_page_footer(ReportBand):
        height = 9.5*cm
        elements = [
            Label(text='Pinhalzinho - SC', top=8.5*cm, left=0.5*cm),
            SystemField(expression='Gerado em %(now:%d/%m/%Y)s às %(now:%H:%M)s   ', top=8.5*cm, left=13.5*cm),
        ]
        borders = {'top': True, 'bottom': True, 'left': True, 'right': True,}
    
    
    subreports = [
                  SubReport(
                            queryset_string = '%(object)s.ordemServico.servico.defeitos.all()',
                            band_detail = ReportBand(
                                                     height=0.5*cm,
                                                     elements=[
                                                               ObjectValue(attribute_name='nome', left=5*cm, top=11.6*cm),
                                                    ]
                            ),
                ),
                SubReport(
                            queryset_string = '%(object)s.ordemServico.servico.itens.all()',
                            band_detail = ReportBand(  
                                                     height=0.5*cm, 
                                                     elements=[
                                                               ObjectValue(attribute_name='nome', left=15*cm, top=10.5*cm),
                                                    ]
                            ),
                ),
    ]  

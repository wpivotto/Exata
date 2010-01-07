# -*- coding: utf-8 -*- 
from django.conf.urls.defaults import *
from django.conf import settings


from django.contrib import admin

urlpatterns = patterns('',

    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/sistema/ordemservico/report/(?P<os_id>\d+)/$', 'claro.sistema.views.reports.ordem_servico'),
    (r'^admin/sistema/solicitacao/report/(?P<param_id>\d+)/$', 'claro.sistema.views.reports.solicitacao'),
    (r'^admin/sistema/orcamento/notify/(?P<servico_id>\d+)/$', 'claro.sistema.views.email.send'),
    (r'^admin/sistema/orcamento/new/os/(?P<servico_id>\d+)/$', 'claro.sistema.views.ordens.orcamento'),
    (r'^admin/sistema/garantia/new/os/(?P<servico_id>\d+)/$', 'claro.sistema.views.ordens.garantia'),
    (r'^admin/export/', include('export.urls')),
    (r'^admin/messages/', include('messages.urls')),
    (r'^admin/djangodblog/error/send_mail/(?P<error_id>\d+)/$', 'djangodblog.views.send_email_view'),
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/(.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),

)


admin.autodiscover()


    
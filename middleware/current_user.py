# threadlocals middleware
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

class Users(object):
    
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
    
    @staticmethod
    def current():
        return getattr(_thread_locals, 'user', None)

from django import forms
from django.contrib import admin

class ReadOnlyWidget(forms.Widget):
    def __init__(self, original_value, display_value):
        self.original_value = original_value
        self.display_value = display_value

        super(ReadOnlyWidget, self).__init__()

    def render(self, name, value, attrs=None):
        if self.display_value is not None:
            return unicode(self.display_value)
        return unicode(self.original_value)

    def value_from_datadict(self, data, files, name):
        return self.original_value
    

class HiddenWidget(forms.Widget):
    def __init__(self, original_value, display_value):
        self.original_value = original_value
        self.display_value = display_value

        super(HiddenWidget, self).__init__()

    def render(self, name, value, attrs=None):
        return unicode(self.display_value)

    def value_from_datadict(self, data, files, name):
        return self.original_value

class ReadOnlyAdminFields(admin.ModelAdmin):
    
    def get_form(self, request, obj=None):
        
        form = super(ReadOnlyAdminFields, self).get_form(request, obj)
    
        if hasattr(self, 'readonly_fields'):
            if self.validForUser(request.user, self.readonly_fields.keys()):
                    for user_group, readOnlyFields in self.readonly_fields.iteritems():
                        for field_name in readOnlyFields:
                                self.setReadOnly(field_name, obj, form)
        
        if hasattr(self, 'hidden_fields'):
            if self.validForUser(request.user, self.hidden_fields.keys()):
                    for user_group, hiddenFields in self.hidden_fields.iteritems():
                        for field_name in hiddenFields:
                                self.setHide(field_name, obj, form)

        return form
    
    def validForUser(self, user, user_names):
        return user.username in user_names
    
    def setReadOnly(self, field_name, obj, form):
        if field_name in form.base_fields:
            if hasattr(obj, 'get_%s_display' % field_name):
                display_value = getattr(obj, 'get_%s_display' % field_name)()
            else:
                display_value = None
            
            form.base_fields[field_name].widget = ReadOnlyWidget(getattr(obj, field_name, ''), display_value)
            form.base_fields[field_name].required = False
        
        
    def setHide(self, field_name, obj, form):
        if field_name in form.base_fields:
            if hasattr(obj, 'get_%s_display' % field_name):
                display_value = getattr(obj, 'get_%s_display' % field_name)()
            else:
                display_value = None
            
            form.base_fields[field_name].widget = HiddenWidget(getattr(obj, field_name, ''), ' ')
            form.base_fields[field_name].required = False
        
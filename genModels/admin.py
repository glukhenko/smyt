# -*- encoding: utf-8 -*-
from django.contrib import admin
from genModels import models as m

class modelGenerateAdmin(object):
    
    def createModelAdmin(self, modelNameAdmin = None, listFieldsAdmin = None):
        
        class Meta:
            app_label = 'genModels'
            db_table = modelNameAdmin
        
        attrs = {'__module__': self.__class__.__module__,
                 'Meta': Meta,
                    }
        
        fields = {'list_display': listFieldsAdmin,
                  'fields': listFieldsAdmin,
                  'ordering': ('id',),
                    }
                    
        if fields:
            attrs.update(fields)
        
        return type(modelNameAdmin, (admin.ModelAdmin,), attrs)
    
# Создание классов Admin для существующих моделей
for name in m.generateModels:
    
    model = m.generateModels[name]['model']
    
    fieldsAdmin = [ field['id'] for field in m.generateModels[name]['fields'] ]
    
    modelAdmin = modelGenerateAdmin()
    modelAdmin = modelAdmin.createModelAdmin(name + 'Admin', fieldsAdmin)
    
    admin.site.register(model, modelAdmin)
    
    
    
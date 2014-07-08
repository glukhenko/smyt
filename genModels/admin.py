from django.contrib import admin
from django.db import models
from genModels import models as m
import os
import yaml


prefixIn = '.\\input\\' 
    
class modelGenerateAdmin(object):
    
    def __init__(self):
        pass
        
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
        
        modelAdmin = type(modelNameAdmin, (admin.ModelAdmin,), attrs)
        return modelAdmin
    
    
def main():
    
    for file in os.listdir(prefixIn):
        
        with open(prefixIn + file, 'r') as hf:
            content = yaml.load(hf)
            
            for key, value in content.items():
                
                model = m.generateModels[key]['model']
                
                fieldsAdmin = [ field['id'] for field in value['fields'] ]
                    
                modelAdm = modelGenerateAdmin()
                modelAdm = modelAdm.createModelAdmin(key + 'Admin', fieldsAdmin)
                
                admin.site.register(model, modelAdm)
    
main()
    
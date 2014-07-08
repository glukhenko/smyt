# -*- encoding: utf-8 -*-

from django.db import models
import os
import yaml

prefixIn = '.\\input\\'
    
class modelGenerate(object):
    
    def __init__(self):
        pass
        
    def createModel(self, modelName = None, fields = None):
        
        class Meta:
            app_label = 'genModels'
            db_table = modelName
        
        attrs = {'__module__': self.__class__.__module__,
                 'Meta': Meta,
                    }
                    
        if fields:
            attrs.update(fields)
        
        return type(modelName, (models.Model,), attrs)
    
def main():
    
    global generateModels
    
    typeFields = {'char': models.CharField,
                  'int': models.IntegerField,
                  'date': models.DateField, 
                    }
                    
    getField = lambda field: typeFields[field](max_length=100) if field=='char' else typeFields[field]()
    
    for file in os.listdir(prefixIn):
        
        hf = open(prefixIn + file, 'r')
        content = yaml.load(hf)
        
        for key, value in content.items():
            
            fields = { field['id']: getField(field['type']) for field in value['fields'] }
            model = modelGenerate()
            model = model.createModel(key, fields)
            
            content[key]['model'] = model
            
        generateModels = content
            
generateModels = None
main()
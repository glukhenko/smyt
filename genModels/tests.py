# -*- encoding: utf-8 -*-

from django.test import TestCase
from django.test.client import Client
from genModels import models as m
import datetime
import random

class generateTest(object):
    
    def createTest(self, modelName = None, fields = None):
        
        class Meta:
            app_label = 'genModels'
            db_table = modelName
        
        attrs = {'__module__': self.__class__.__module__,
                 'Meta': Meta,
                    }
                    
        if fields:
            attrs.update(fields)
        
        return type(modelName, (TestCase,), attrs)
        
def testCreateRecords(self):
    
    values = {'int': lambda : random.randint(1, 100) * 1000,
              'char': lambda : ''.join( [ chr(random.randint(65, 90)) for _ in range(10) ] ),
              'date': lambda: datetime.datetime.now().date()
                }
    
    for name in m.generateModels:
        
        # Создаем 10 рандомных объектов
        print 'try create 10 records for model=' + name
        for _ in range(10):
            fields = { field['id']: values[field['type']]() for field in m.generateModels[name]['fields'] }
            record = self.models[name](**fields)
            record.save()
            
        records = self.models[name].objects.all()
        self.assertEqual(10, len(records))
        
def testUpdateRecords(self):
    
    values = {'int': lambda : random.randint(1, 100),
              'char': lambda : ''.join( [ chr(random.randint(65, 90)) for _ in range(10) ] ) + '_new_value',
              'date': lambda: datetime.datetime.now().date() + datetime.timedelta(days=random.randint(1, 10))
                }
    
    idRow = random.randint(1, 10)
    
    for name in m.generateModels:
    
        # Попробуем обновить по одной записи на каждый тип
        print 'try update all field for model=' + name
        
        fields = [ (field['id'], field['type']) for field in m.generateModels[name]['fields'] ]
        
        for nameField, typeField in fields:
            
            rowid = random.randint(1, 10)
            newValue = values[typeField]()
            newFields = { nameField: newValue }
            print '[' + name + '] update ' + str(rowid) + ' record: ' + nameField + '=' + str(newValue)
            self.models[name].objects.filter(id=rowid).update(**newFields)
            
def testGetIndexPageForModel(self):
    
    c = Client()
    
    for name in m.generateModels:
        
        print 'try get index page for model=' + name
        response = c.get('/', {'nameDB': name})
        self.assertEqual(response.status_code, 200)
    
def testGetIndexPageForModel(self):
    
    c = Client()
    
    for name in m.generateModels:
        
        print 'try get index page for model=' + name
        response = c.get('/', {'nameDB': name})
        self.assertEqual(response.status_code, 200)

def testSaveDataFromAjax(self):
    
    values = {'int': lambda : random.randint(1, 100),
              'char': lambda : ''.join( [ chr(random.randint(65, 90)) for _ in range(10) ] ) + '_new_value_ajax',
              'date': lambda: datetime.datetime.now().date() + datetime.timedelta(days=random.randint(1, 10))
                }
    
    c = Client()
    
    for name in m.generateModels:
        
        fields = [ (field['id'], field['type']) for field in m.generateModels[name]['fields'] ]
        
        for nameField, typeField in fields:
            
            
            rowid = random.randint(1, 10)
            newValue = values[typeField]()
            newFields = { 'nameDB': name,
                          'id': rowid,
                          'field': nameField,
                          'value': newValue
                          }
            
            print '[' + name + '] try save ' + str(rowid) + ' record from ajax: ' + nameField + '=' + str(newValue)
            
            response = c.get('/', newFields)
            self.assertEqual(response.status_code, 200)
    
models = { 'models': { name: m.generateModels[name]['model'] for name in m.generateModels } }

testModel = generateTest()
testModel = testModel.createTest('testModels', models)

setattr(testModel, 'testCreateRecords', testCreateRecords)
setattr(testModel, 'testUpdateRecords', testUpdateRecords)
setattr(testModel, 'testGetIndexPageForModel', testGetIndexPageForModel)
setattr(testModel, 'testSaveDataFromAjax', testSaveDataFromAjax)


    
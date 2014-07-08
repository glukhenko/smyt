# -*- encoding: utf-8 -*-
from django.utils import simplejson 
from dajaxice.core import dajaxice_functions 

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from genModels import models as m
import datetime

@dajaxice_register
def getData(request, nameDB):
    
    model = m.generateModels[nameDB]['model']
    nameFields = ['id'] + [ field['id'] for field in m.generateModels[nameDB]['fields'] ]
    
    # Получим данные из базы в формате [ [row1.cell1, row1.cellN], [rowN.cell1, rowN.cellN] ] 
    dataTable = [ [ row.serializable_value(name) for name in nameFields ] for row in model.objects.all() ]
    # Используем strftime если дата
    dataTable = [ [ cell.strftime('%Y-%m-%d') if type(cell)==datetime.date else cell for cell in row ] for row in dataTable ]
    
    return simplejson.dumps({'nameDB': nameDB,
                             'fields': m.generateModels[nameDB]['fields'],
                             'dataTable': dataTable,
                             })
                             
                             
@dajaxice_register
def setData(request, nameDB, id, field, value):
    
    fields = {field: value}
    
    try:
        model = m.generateModels[nameDB]['model']
        model.objects.filter(id=id).update(**fields)
        result = 'ok'
    except:
        result = 'error'
    
    return simplejson.dumps({'result': result})
    
    
    
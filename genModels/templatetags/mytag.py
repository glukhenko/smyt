# -*- encoding: utf-8 -*-
from django import template
register = template.Library()
    
@register.filter
def getTitle(models, tableName):
    return models[tableName]['title']
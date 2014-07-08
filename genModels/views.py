# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from genModels import models as m
from django.core.context_processors import csrf

def index(request):
    
    if request.method == 'POST':
    
        if 'nameDB' in request.POST:
            model = m.generateModels[request.POST['nameDB']]['model']
            
            fields = [ field['id'] for field in m.generateModels[request.POST['nameDB']]['fields'] ]
            fields = { field: request.POST[field] for field in fields if field in request.POST}
            
            newRecord = model(**fields)
            newRecord.save()
            
        return redirect('/')
    
    context = {'tables': m.generateModels}
    
    context.update(csrf(request))
    return render_to_response('index.html', context)
    

var editCell = 0;

function dataReceived(data){
    
    createTable(data);
    setDataTable(data);
    createFormNewRecord(data);
    
    initDatepicker();
}

function saveData(data){
    
    if(data.result=='error') alert('Ошибка записи в базу');
    
}

function createTable(data){
    //Создаем заголовок таблицы
    var table = document.getElementById('table');
    table.setAttribute('name', data.nameDB);
    table.innerHTML = '';
    
    
    thead = document.createElement('thead');
    tr = document.createElement('tr');
    td = document.createElement('td');
    td.innerHTML = 'id';
    tr.appendChild(td);
    
    for(var i=0; i<data.fields.length; i++){
        td = document.createElement('td');
        td.innerHTML = data.fields[i]['title'];
        tr.appendChild(td);
    }
    
    thead.appendChild(tr);
    table.appendChild(thead);
    
}

function setDataTable(data){
    //Заполняем таблицу данными
    var table = document.getElementById('table');
    
    for(var i=0; i<data.dataTable.length; i++){
        tr = document.createElement('tr');
        for(var j=0; j<data.dataTable[i].length; j++){
            
            td = document.createElement('td');
            var cellValue = data.dataTable[i][j];
            td.innerHTML = cellValue;
            
            var idrow = data.dataTable[i][0];
            
            if(j){
                var cellType = data.fields[j-1]['type'];
                var cellName = data.fields[j-1]['id'];
                
                td.setAttribute('typefield', cellType);
                td.setAttribute('namefield', cellName);
                td.setAttribute('onclick', 'editTd(this)');
                td.setAttribute('idrow', idrow)
            }
            
            tr.appendChild(td);
            
        }
        table.appendChild(tr);
    }
    
}

function createFormNewRecord(data){
    //Создание формы для ввода новой записи
    newRecord = document.getElementById('newRecord');
    newRecord.innerHTML = '';
    
    for(var i=0; i<data.fields.length; i++){
        b = document.createElement('b');
        input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('typefield', data.fields[i]['type']);
        input.setAttribute('namefield', data.fields[i]['title']);
        input.setAttribute('name', data.fields[i]['id']);
        
        if(data.fields[i]['type']=='date'){
            input.id = 'datepicker';
        }
        
        b.innerHTML = data.fields[i]['title'];
        newRecord.appendChild(b);
        newRecord.appendChild(input);
        newRecord.appendChild(document.createElement('br'));
    }
    
    // Устанавливаем в hidden имя таблицы
    input = document.createElement('input');
    input.setAttribute('type', 'hidden');
    input.setAttribute('name', 'nameDB');
    input.setAttribute('value', data.nameDB);
    newRecord.appendChild(input);
    
}

function checkData(){
    
    newRecord = document.getElementById('newRecord');
    
    for(var i=0; i<newRecord.childNodes.length; i++){
        if(newRecord.childNodes[i].tagName=='INPUT'){
            elem = newRecord.childNodes[i];
            
            if(elem.getAttribute('type')=='hidden') continue
            
            if(elem.value.length==0){
                alert('Ошибка: поле ' + newRecord.childNodes[i].getAttribute('namefield') + ' не заполнено');
                return;
            }
            
            if(!checkCell( elem.value, elem.getAttribute('typefield') )) return;
        }
    }
    
    document.getElementById('form').submit();
}

function checkCell(str, typeField){
    
    if(typeField=='int'){
        if (!checkInt(str)){
            alert('Ошибка: значение "' + str + '" некорректно, необходимо ввести число');
            return 0;
        }
        
    }else if(typeField=='date'){
        if (!checkDate(str)){
            alert('Ошибка: значение "' + str + '" некорректно, предполагается дата формата yyyy-mm-dd');
            return 0;
        }
        
    }
    
    return 1;
    
}


function checkInt(str){
    
    if(str.search(/^\d+$/) != -1){
        return 1;
    }else{
        return 0;
    }
    
}

function checkDate(str){
    
    //yyyy-mm-dd
    var reg = /^(\d{4})-((01|02|03|04|05|06|07|08|09|10|11|12){1})-(((0|1|2){1}\d{1})|(30|31){1})$/
    if(str.search(reg) != -1){
        return 1;
    }else{
        return 0;
    }
}

function editTd(elem){
    
    if(elem.id=='edit'){
        return;
    }else{
        // Выбрана другая ячейка в таблице, удаляем поле ввода и сохраняем результат
        var input = document.getElementById('editInput');
        
        if(input){
            if(!sendDataToSave(input)) return;
        }else{
            var input = document.getElementById('editDate');
            if(input){
                if(!sendDataToSave(input)) return;
            }
        }
    }
    
    var cellValue = elem.innerHTML;
    elem.innerHTML = '';
    elem.id = 'edit';
    var input = document.createElement('input');
    
    if(elem.getAttribute('typefield')=='date'){
        input.id = 'editDate';
    }else{
        input.id = 'editInput';
    }
    
    input.value = cellValue;
    elem.appendChild(input);
    input.focus();
    editCell = elem;
    
    if(elem.getAttribute('typefield')=='date'){
        initDateEditor();
    }
}

function sendDataToSave(input){
    
    if(!checkCell(input.value, editCell.getAttribute('typefield'))){
        input.focus();
        return 0;
    }
    
    input.parentNode.innerHTML = input.value;
    editCell.id = '';
    
    input.remove();
    
    nameDB = document.getElementById('table').getAttribute('name');
    // Отправляем запрос сохранения данных
    Dajaxice.genModels.setData(saveData, {'nameDB': nameDB,
                                          'id': editCell.getAttribute('idrow'),
                                          'field': editCell.getAttribute('namefield'),
                                          'value': editCell.innerHTML
                                            });
                                            
    return 1;
    
}
 
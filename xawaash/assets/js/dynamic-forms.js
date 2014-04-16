function addForm(prefix, target, nested){
  var templateForm = $( '#empty_' + prefix );
  templateForm.find('select:not(select[multiple=multiple])').each(function(){
    if($(this).data('uiCombobox')){
      $(this).combobox('destroy');
    }
  });
  var newForm = templateForm.clone(true);
  newForm.find('select:not(select[multiple=multiple])').each(function(){
    $(this).combobox();
  });
  newForm.find('.img-upload').each(function(){
    $(this).dropzone({
      url:'/post/wp/upload/',
      success: function(file, response){
        var target = $(this.element).attr('data-target');
        $(target + 'wordpress_image_id').val(response.id);
        $(target + 'link').val(response.link);
        $(target + 'width').val(response.width);
        $(target + 'height').val(response.height);
        $(target + 'img').attr({
          'src': response.link,
          'width': response.width/4,
          'height': response.height/4,
        }).removeClass('hidden');
        $(this.element).addClass('hidden');
      },
    });
  });
  var total = $( '#id_' + prefix + '-TOTAL_FORMS' ).val();
  newForm.removeAttr('id');
  newForm.find('.form_info > :input').each(function(){
    var nameList = $(this).attr('name').split('-');
    var field = nameList[nameList.length-1];
    if(field == '_loc_index'){
      $(this).val($(target).children().length);
    } else if (field == 'DELETE'){
      $(this).removeAttr('checked');
    }
  });
  templateForm.find(':input,select,textarea,img,.dropzone').each(function(){
    var name = $(this).attr('name');
    if(name){
      var nameList = name.split('-');
      nameList[nameList.length-2] = total;
      name = nameList.join('-');
      var id = 'id_' + name;
      $(this).attr({'name':name, 'id':id});
      if($(this).hasClass('dropzone')){
        nameList[nameList.length-1] = '';
        var target = '#id_' + nameList.join('-');
        $(this).attr({'data-target':target});
      } else if($(this).attr('data-target')){
        var target = '#id_' + name.substring(0, name.length - 6);
        $(this).attr({'data-target':target});
      }
    }
  });
  total++;
  $( '#id_' + prefix + '-TOTAL_FORMS' ).val(total);
  if(nested){
    newForm.removeAttr('class');
    newForm.insertBefore('#empty_' + prefix);
  } else {
    newForm.appendTo( target );
  }
}

function addFormSet(prefix, target){
  var templateFormSet = $( '#empty_' + prefix );
  templateFormSet.find('select:not(select[multiple=multiple])').each(function(){
    if($(this).data('uiCombobox')){
      $(this).combobox('destroy');
    }
  });
  var newFormSet = templateFormSet.clone(true);
  newFormSet.find('select:not(select[multiple=multiple])').each(function(){
    $(this).combobox();
  });
  newFormSet.find('.img-upload').each(function(){
    $(this).dropzone({
      url:'/post/wp/upload/',
      success: function(file, response){
        var target = $(this.element).attr('data-target');
        $(target + 'wordpress_image_id').val(response.id);
        $(target + 'link').val(response.link);
        $(target + 'width').val(response.width);
        $(target + 'height').val(response.height);
        $(target + 'img').attr({
          'src': response.link,
          'width': response.width/4,
          'height': response.height/4,
        }).removeClass('hidden');
        $(this.element).addClass('hidden');
      },
    });
  });
  var total = $( '#id_' + prefix + '-TOTAL_FORMS' ).val();
  newFormSet.removeAttr('id');
  newFormSet.find('.formset_info > :input').each(function(){
    var nameList = $(this).attr('name').split('-');
    var field = nameList[nameList.length-1];
    if(field == '_loc_index'){
      $(this).val($(target).children().length);
    } else if (field == 'DELETE'){
      $(this).removeAttr('checked');
    }
  }); 
  templateFormSet.find(':input,select,textarea').each(function(){
    var name = $(this).attr('name');
    if(name){
      var nameList = name.split('-');
      nameList[1] = total;
      name = nameList.join('-');
      var id = 'id_' + name;
      $(this).attr({'name':name, 'id':id});
      if($(this).attr('data-target')){
        var target = '#id_' + name.substring(0, name.length - 6);
        $(this).attr({'data-target':target});
      }
    }
  });

  templateFormSet.find('.nested,.nested > .nested_empty').each(function(){
    var idList = $(this).attr('id').split('-');
    idList[1] = total;
    var id = idList.join('-');
    $(this).attr({'id':id});
  });
  
  total++;
  $( '#id_' + prefix + '-TOTAL_FORMS' ).val(total);
  newFormSet.appendTo( target );
}



$(document).ready(function(){
    $('#imagechooser').hide();
    
    $('#imagechoices').hide();
    $('#id_chosenImage').hide();
    $('#id_lastChosenImage').val($('#viewChosenImage').val());
    
    $('#showChooser').click(function(event){
        event.preventDefault();
        $('#imagechoices').toggle();
    });
    $('.imageList').click(function(event){
        $('.imageList').css('border', "none");
        $('#id_chosenImage').val($(this).attr("alt"));
        
        $('#id_lastChosenImage').val($(this).attr("alt"));
        
        $(this).css('border', "solid 2px red");
        
    });
    
    /*
    if($('#id_colorSelect_1').is(':checked')) {
        //$('#id_numberOfColors').attr('disabled', 'disabled'); 
        $('#id_numberOfColors').prop('disabled', true);
    }
    */

});


$(function(){
    $('#my_form').submit(function(event){
       
       $('#loadingimage').show();
        $('#userimage').hide();
        $('.well').hide();
        $('.imageupload').hide();
        $('#my_form').hide();
        $('#help').hide();
	    $('#instructionsArea').hide();
          
    });

});

/*
$('#id_colorSelect_1').click(function() { // disabled numColors field
    if($('#id_colorSelect_1').is(':checked')) { 
        //$('#id_numberOfColors').attr('disabled', 'disabled'); 
        $('#id_numberOfColors').prop('disabled', true);
    }
});

$('#id_colorSelect_0').click(function() { // turn numColors back on
    if($('#id_colorSelect_0').is(':checked')) {
        //$('#id_numberOfColors').attr('disabled', 'disabled'); 
        $('#id_numberOfColors').prop('disabled', false);
    } 
});

$('#renderBt').click(function() { // make sure numColors is enabled
    $('#id_numberOfColors').prop('disabled', false);
});
*/

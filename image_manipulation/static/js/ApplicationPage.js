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

S(document).ready(function(){
       $('#userimage').show();
       $('#loadingimage').hide();
       $('#my_form').show();
	$('.imageupload').show();
	$('#help').show();
	$('#instructionsArea').show();
});

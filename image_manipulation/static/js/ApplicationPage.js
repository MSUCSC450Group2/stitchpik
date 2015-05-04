$(document).ready(function(){
    $('#imagechooser').hide();
    alert($('#viewChosenImage').val());
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
          
    });

});

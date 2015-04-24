$(document).ready(function(){
    $('#imagechooser').hide();
    $('#imagechoices').hide();
    $('#id_chosenImage').hide();
    $('#showChooser').click(function(event){
        event.preventDefault();
        $('#imagechoices').toggle();
    });
    $('.imageList').click(function(event){
        $('.imageList').css('border', "none");
        $('#id_chosenImage').val($(this).attr("alt"));
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

$(document).ready(function() {

   //Register review form submition function
    $("#show_publications").click(
    function() 
    { 
      if($(".publications_autre").css('display') == 'none')
        $(".publications_autre").show();
      else
        $(".publications_autre").hide();
    
    });

    // Activer le datepicker sur les input de classe "date"
    $.datepicker.setDefaults($.datepicker.regional['fr']);
    $('input:text.date').datepicker();
});

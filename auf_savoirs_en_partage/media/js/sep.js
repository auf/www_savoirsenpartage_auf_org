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

});

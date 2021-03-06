(function() {

    $(document).ready(function() {

        //Register review form submition function
        $("#show_publications").click(function() {
            if($(".publications_autre").css('display') == 'none') {
                $(".publications_autre").show();
            }
            else {
                $(".publications_autre").hide();
            }
        });

        $("#btnrechercheavance").click(function() {
            if($("#rechercheavancee").css('display') == 'none') {
                $("#rechercheavancee").show();
            }
            else {
                $("#rechercheavancee").hide();
            }
			return false;
        });

        // Activer le datepicker sur les input de classe "date"
        $.datepicker.setDefaults($.datepicker.regional['fr']);
        $('input:text.date')
            .datepicker({
                autoSize: true,
                dateFormat: 'dd/mm/yy',
                showAnim: 'fadeIn',
                onSelect: function(dateText) {
                    $('input:text.date').datepicker('option', 'defaultDate', dateText);
                }
            })
            .change(function() {
                $(this).datepicker('setDate', $(this).datepicker('getDate'));
                return true;
            });
        $('input:text.time').timepicker({
            timeFormat: 'HH:mm',
        });

        // S'assurer qu'on tient compte de ce qui se trouve dans le champ de
        // recherche par mots-clés lorsqu'on choisit une région ou une
        // discipline.
        $('#col-menu a').click(function() {
            var href = this.href
            var pos = href.indexOf('?')
            if (pos != -1) {
                href = href.substring(0, pos)
            }
            var query = $('#fRecherche input[name=q]').val();
            if (query) {
                if (href.search(/\/recherche\/?/) == -1) {
                    href += 'recherche/';
                }
                href += '?q=' + query;
            }
            window.location = href;
            return false;
        });

    });

})();

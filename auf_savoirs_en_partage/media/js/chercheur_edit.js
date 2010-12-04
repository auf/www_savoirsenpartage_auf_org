(function() {

    $(document).ready(function() {
        $('#expertises fieldset').formset({
            prefix: 'expertise',
            addText: 'ajouter une expertise',
            deleteText: 'supprimer cette expertise',
            formCssClass: 'dynamic-form-expertises'
        });
        $('#publications fieldset').formset({
            prefix: 'publication',
            addText: 'ajouter une publication',
            deleteText: 'supprimer cette publication',
            formCssClass: 'dynamic-form-publications'
        });
        $('input[name=chercheur-etablissement]').autocomplete({ 
            source: '/etablissements/autocomplete/',
            select: function(event, ui) {
                var etablissement = ui.item.value;
                $.getJSON(
                    '/etablissements/pays/', 
                    { etablissement: etablissement },
                    function(pays) {
                        $('select[name=chercheur-pays_etablissement]').val(pays);
                    }
                );
            }
        });
    });

})();

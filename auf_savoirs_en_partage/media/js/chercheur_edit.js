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
        var $edit_publication_link = $('<a class="edit-publication">éditer cette publication</a>');
        var $additional_fields = $('.publication_affichage').next();
        $additional_fields.after($edit_publication_link).hide();
        $edit_publication_link.click(function() { $additional_fields.show(); $(this).hide(); });
    });

})();

(function() {

    $(document).ready(function() {

        // Fieldsets
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

        // Auto-complete des établissements
        var $etablissement = $('input[name=chercheur-etablissement]');
        $etablissement.autocomplete({ source: '/etablissements/autocomplete/' });
        $('select[name=chercheur-pays_etablissement]').change(function() {
            $etablissement.autocomplete('option', 'source', '/etablissements/autocomplete/' + $(this).val() + '/');
        }).change();

        // Publications legacy
        var $edit_publication_link = $('<a class="edit-publication">éditer cette publication</a>');
        var $additional_fields = $('.publication_affichage').next();
        $additional_fields.after($edit_publication_link).hide();
        $edit_publication_link.click(function() { $additional_fields.show(); $(this).hide(); });
    });

})();

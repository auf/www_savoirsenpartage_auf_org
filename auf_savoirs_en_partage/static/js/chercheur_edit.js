(function() {
    var nom_expertise_selector = 'input[name^="expertise"][name$="nom"]';

    function expertise_added($row) {
        $row.find(nom_expertise_selector).change(show_or_hide_sollicitation_expert);
    }
    
    function expertise_removed($row) {
        show_or_hide_sollicitation_expert();
    }
    
    function show_or_hide_sollicitation_expert() {
        var $sollicitation_field = $('input[name$="pas_de_sollicitation_expertises"]').closest('table');
        var $non_empty_fields = $(nom_expertise_selector + '[value!=""]:visible');
        if ($non_empty_fields.size() > 0) {
            $sollicitation_field.show();
        }
        else {
            $sollicitation_field.hide();
        }
    }

    $(document).ready(function() {

        // Fieldsets
        $('#expertises fieldset').formset({
            prefix: 'expertise',
            addText: 'ajouter une expertise',
            deleteText: 'supprimer cette expertise',
            formCssClass: 'dynamic-form-expertises',
            added: expertise_added,
            removed: expertise_removed
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

        // Montrer ou cacher la case à cocher "sollicitation pour expertise"
        show_or_hide_sollicitation_expert();
        $(nom_expertise_selector).change(show_or_hide_sollicitation_expert);

    });

})();

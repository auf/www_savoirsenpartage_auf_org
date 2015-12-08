(function() {
    $(document).ready(function() {
        // Auto-complete des établissements
        var $etablissement = $('input[name=etablissement]');
        $etablissement.autocomplete({ source: '/etablissements/autocomplete/' });
        $('select[name=pays]').change(function() {
            $etablissement.autocomplete('option',
                                        'source',
                                        '/etablissements/autocomplete/'
                                            + $(this).val() + '/');
        }).change();
    });

})();

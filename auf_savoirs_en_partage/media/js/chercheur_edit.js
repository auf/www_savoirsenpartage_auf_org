(function() {

    function update_etablissement_autre() {
        if ($('#id_chercheur-etablissement').val() == '') {
            $('#etablissement_autre').slideDown('fast');
        }
        else {
            $('#etablissement_autre').slideUp('fast');
        }
    }

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
        update_etablissement_autre()
        $('#id_chercheur-etablissement').change(update_etablissement_autre)
    });
})();

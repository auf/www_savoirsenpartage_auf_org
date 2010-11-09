$(document).ready(function() {
    $('#expertises fieldset').formset({
        prefix: 'expertise',
        addText: 'ajouter une expertise',
        deleteText: 'supprimer cette expertise',
        formCssClass: 'dynamic-form-expertises'
    });
});

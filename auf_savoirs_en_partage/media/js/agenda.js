(function() {

    function update_fuseau() {
        var pays = $('select[name=pays]').val();
        $('select[name=fuseau]').load('options_fuseau_horaire/?pays=' + pays);
    }
    $(document).ready(function() {
        $('select[name=pays]').change(update_fuseau);
        update_fuseau();
    });
})();

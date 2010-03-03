var AUF = {};

AUF.validation = {};
AUF.validation.regex = {
	date : /^[0-9]{4}\-[0-9]{1,2}\-[0-9]{1,2}$/,
	url : /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
}

$(document).ready(function() {
	/************************************************************
	 * Calendriers
	 ************************************************************/
	Date.format = 'yyyy-mm-dd';
	if ($('.date-pick').length > 0) {
		// Traduction des textes du calendrier
		$.dpText = {
			TEXT_PREV_YEAR		:	'Année précédente',
			TEXT_PREV_MONTH		:	'Mois précédent',
			TEXT_NEXT_YEAR		:	'Année suivante',
			TEXT_NEXT_MONTH		:	'Mois suivant',
			TEXT_CLOSE			:	'Fermer',
			TEXT_CHOOSE_DATE	:	'Choisir une date',
			HEADER_FORMAT		:	'mmmm yyyy'
		};

		$('.date-pick').datePicker({
			showYearNavigation: false
		}).each(function() {
			//if ($(this).val() == "") {
				//$(this).val(new Date().asString())
			//}
			$(this).trigger('change');
		});

		$('.dp-choose-date').click(function() {
			$('.champ').removeClass('focus');
			$(this).parent().addClass('focus');
		});
		
	}
});
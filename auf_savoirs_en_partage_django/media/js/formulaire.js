$(document).ready(function() {
	$('form').submit(function() {
		var valide = true;
		
		// Titre
		if ($('#titre').val() == "") {
			valide = false;
		}

		// Date de début
		if ($('#dateDebut').val().match(AUF.validation.regex.date) == null) {
			valide = false;
		} else {
			var date = $('#dateDebut').val();
			if (date != "") { date = date.split('-'); }
			date = date[1]+'/'+date[2]+'/'+date[0];
			// Date valide
			if (!isDate(date)) {
				valide = false;
			}	
		}

		// Date de fin
		if ($('#dateFin').val() != "") {
			if ($('#dateFin').val().match(AUF.validation.regex.date) == null) {
				valide = false;
			} else {
				var date = $('#dateFin').val();
				if (date != "") { date = date.split('-'); }
				date = date[1]+'/'+date[2]+'/'+date[0];
				// Date valide
				if (!isDate(date)) {
					valide = false;
				}	
			}
		}
		
		// Organisateur
		if ($('#organisateur').val() == "") {
			valide = false;
		}
		
		// Lieu
		if ($('#lieu').val() == "") {
			valide = false;
		}
		
		// Ville
		if ($('#ville').val() == "") {
			valide = false;
		}
		
		// Pays
		if ($('#pays').val() == "") {
			valide = false;
		}
		
		// Site web
		if ($('#siteWeb').val() != "") {
			if ($('#siteWeb').val().match(AUF.validation.regex.url) == null) {
				valide = false;
			}
		}
		
		// Discipline
		if ($('#discipline').val() == "") {
			valide = false;
		}
		
		// Discipline
		if ($('#description').val() == "") {
			valide = false;
		}
	});
});
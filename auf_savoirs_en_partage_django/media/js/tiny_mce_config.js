//justifyleft,justifycenter,justifyright,justifyfullsup

tinyMCE.init({
	// Décommenter la ligne suivants pour utiliser ibrowser.
	// Il ne faut pas oublier de configurer le fichier js/tiny_mce/plugins/ibrowser/config/config.inc.php
	// Ajouter ceci à la ligne theme_advanced_buttons1 : "ibrowser",
	//plugins : "paste,fullscreen,safari,flash,ibrowser",
	
	// Décommenter la ligne suivants pour utiliser filemanager.
	// Il ne faut pas oublier de configurer le fichier js/tiny_mce/plugins/filemanager/config.php
	// Ajouter ceci à la ligne theme_advanced_buttons1 : "image",
	//plugins : "paste,fullscreen,safari,flash,filemanager",
	
	plugins : "paste,safari,flash,nonbreaking,visualchars,xhtmlxtras,preview",
	//italique, bold, exposant, indice, ligature (oe), ul, ol, paste from word
	theme_advanced_buttons1 : "cut,copy,pastetext,pasteword,separator,undo,redo,separator,code,separator,preview",
	theme_advanced_buttons2 : "formatselect,separator,bullist,numlist,outdent,indent,separator,blockquote,separator,justifyleft,justifycenter,justifyright,justifyfull",
	theme_advanced_buttons3 : "bold,italic,separator,link,unlink,anchor,separator,forecolor,sub,sup,charmap,abbr,nonbreaking",
	theme_advanced_buttons4 : "",
	theme_advanced_toolbar_location : "top",
	theme_advanced_toolbar_align : "left",
	mode : "textareas",
	editor_selector : "mceEditor",
	theme : "advanced",
	convert_urls : false,
	relative_urls : false,
	language : "fr", //en
	force_br_newlines : false,
	force_p_newlines : true,
	remove_linebreaks : false,
	apply_source_formatting : true,
	cleanup_on_startup : true,
	browsers : "msie,gecko,safari,opera",
	theme_advanced_blockformats : "p,h2,h3,h4",
	entity_encoding : "raw"
	//auto_resize : true
});
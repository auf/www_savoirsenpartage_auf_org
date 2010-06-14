<!-- Copyright (c) 2005 Rob Lanphier.
See http://robla.net/2005/jsonwidget/LICENSE for license (BSD style)
-->

<?php

$jsonfile = 'electiondata.json';
$schemafile = 'electionschema.json';
$schemaschemafile = 'schemaschema.json';
switch($_GET['user']) {
 case "advanced":
     $enableschemaedit = true;
     $debuglevel = 1;
     break;
 case "debug":
     $enableschemaedit = true;
     $debuglevel = 2;
     break;
}
switch($_GET['sample']) {
 case "large":
     $schemafile = 'electionschema.json';
     $jsonfile = 'electionlarge.json';
     break;
    
 case "tiny":
     $jsonfile = 'electiontiny.json';
     break;
     
 case "blank":
     $jsonfile = null;
     break;

 case "byexample":
     $jsonfile = null;
     $schemafile = 'openschema.json';
     $byexample = true;
     $enableschemaedit = true;
     break;
 case "schemaedit":
     $jsonfile = null;
     $schemafile = 'schemaschema.json';
     break;
 case "schemaschema":
     $jsonfile = 'schemaschema.json';
     $schemafile = 'schemaschema.json';
     break;
 case "electoschema":
     $jsonfile = 'electionschema.json';
     $schemafile = 'schemaschema.json';
     break;
 case "addressbookschema":
     $jsonfile = 'addressbookschema.json';
     $schemafile = 'schemaschema.json';
     break;
 case "openschema":
     $jsonfile = null;
     $schemafile = 'openschema.json';
     break;
 case "blankaddr":
     $jsonfile = null;
     $schemafile = 'addressbookschema.json';
     break;
 case "normal":
 default:
     $jsonfile = 'electionnormal.json';
     break;
}



?>

<html>
 
<head>
 
<title>JSON widget prototype</title>


<script src="json.js"></script> 
<script src="jsonedit.js"></script> 

<link rel="stylesheet" type="text/css" href="jsonwidget.css" />

<script type="text/javascript" language="javascript">

function sample_init() {
    var je=new jsonwidget.editor();

    //default values for ids are in script, but can be overridden.
    //For example, to set the formdiv id to something other than
    //"je_formdiv", add the following line:
    //je.htmlids.formdiv = "myveryownformdiv";
    
    <?php if($debuglevel > 1) { ?>
    je.debuglevel = <?php print $debuglevel.';';
    } ?>

    <?php if($enableschemaedit) { ?>
    je.views = ['form','source','schemaform','schemasource'];
    je.schemaEditInit();
    <?php } ?>

    <?php if($byexample) { ?>
    je.byExampleInit();
    <?php } ?>


    je.setView('form');
}

</script>

</head>
 
<?php
if($_POST['jsonsubmit'] != 'true') {
    $onload = ' onload="sample_init();"';
}
?>

<body<?php print $onload?>>

<?php
if($_POST['jsonsubmit'] != 'true') {
    //this encapsulates most of this page
?>
<div id="je_warningdiv">
</div>

<div>
<span id="je_formbutton" style="cursor: pointer">[Edit w/Form]</span>
<span id="je_sourcebutton" style="cursor: pointer">[Edit Source]</span>
<?php if($enableschemaedit) { ?>
<span id="je_schemaformbutton" style="cursor: pointer">[Edit Schema w/Form]</span>
<span id="je_schemasourcebutton" style="cursor: pointer">[Edit Schema Source]</span>
<?php } ?>
</div>


<div id="je_formdiv" style="text-background: white">
</div>

<div>

<div id="je_schemaformdiv" style="text-background: white">
</div>

<textarea id="je_schematextarea" style="display: none" rows="30" cols="80">
<?php 
if($schemafile != null) {
    readfile($schemafile);
}
?>
</textarea>

<form method='POST' id="je_sourcetextform">
<textarea id="je_sourcetextarea" rows="30" cols="80" name="sourcearea">
<?php 
if($jsonfile != null) {
    readfile($jsonfile);
}
?>
</textarea>
<p>
<input type="hidden" name="jsonsubmit" value="true"/>
      <input type="submit" value="Submit JSON"/> - WARNING: submitting your form data ends your editing session.  This merely illustrates what your data looks like on the server side.
</p>
</form>

</div>

<?php if($enableschemaedit) { ?>
<textarea id="je_schemaschematextarea" style="display: none" rows="30" cols="80" name="sourcearea">
<?php 
if($schemaschemafile != null) {
    readfile($schemaschemafile);
}
?>
</textarea>
<?php } ?>


<div>

<form submit="example.php" method="GET">
<fieldset><legend>Demo options</legend>
JSON sample: 
<select name="sample" type="text">
<option value="normal">Election - typical</option>
<option value="byexample">Create a schema by example</option>
<option value="openschema">Freeform JSON</option>
<option value="blankaddr">Address book - blank</option>
<option value="blank">Election - blank</option>
<option value="tiny">Election - minimal</option>
<option value="large">Election - large(ish) data set</option>
<option value="schemaedit">Edit a new schema</option>
<option value="electoschema">Edit the election configuration schema</option>
<option value="addressbookschema">Edit the address book schema</option>
<option value="schemaschema">Edit the schema for schemas</option>
</select>
<br/>
User type: 
<select name="user" type="text">
<option>normal</option>
<option default>advanced</option>
<option>debug</option>
</select>
<br/>
<input value="Change demo" type="submit">
</fieldset>
</form>

</div>
<textarea style="display: none;" id="rawhtml" rows="30" cols="80">
</textarea>

<?php 
}
else {
    //this means $_POST['jsonsubmit'] == 'true'
    require_once('JSON.php');
    $rawjson = $_POST['sourcearea'];
    
    $json = new Services_JSON(JSON_LOOSE_TYPE);
    $jsondata = $json->decode(stripslashes($rawjson));

    print "Data structure as parsed and output by PHP's print_r:<br>";
    print '<textarea  rows="30" cols="80">';
    print_r($jsondata);
    print "</textarea>";
}
?>

</body>
</html>

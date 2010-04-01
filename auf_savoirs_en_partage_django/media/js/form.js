var JSONForm = function (schemadiv, formdiv, sourcediv) {
    this._schema = JSON.parse ($("#"+schemadiv).html());
    this._form = $("#"+formdiv);
    this._source = $("#"+sourcediv);

    this.addToList = JSONForm.addToList;
    this.setup = JSONForm.setup;

    this.readList = JSONForm.readList;
    this.serialize = JSONForm.serialize;
}

JSONForm.addToList = function (divid, no) {
    $("<p><input type='text' id='" + divid + no + "' /></p>").appendTo ("#"+divid);
}

JSONForm.setup = function () {
    // Initial stuff
    var initial = {};
    if (this._source.html().length > 0) {
      initial = JSON.parse (this._source.html());
    }

    var form = "<table>";
    for (k in this._schema.mapping) {
        var field = this._schema.mapping[k];
        if (field.hidden != true) {
            form += "<tr><td>";
            if (typeof(field.title) != 'undefined')
              form += field.title;
            else
              form += k;
            form += "</td><td>";

            var value = initial[k];
            if (typeof (value) == 'undefined')
              value = "";

            var id = "field_" + k;

            if (field.type == "text") {
                form += "<textarea id='"+id+"'>"+value+"</textarea>"
            }
            else if (field.type == "str") {
                form += "<input id='"+id+"' type=\"text\" value=\""+value+"\" />"
            }
            else if (field.type == "seq") {
                form += "<div id='"+id+"'>";
                var i = -1;
                for (i in value) {
                    form += "<p><input type='text' id='" + id + i
                      + "' value=\"" + value[i].replace(/"/g, "\\\"") + "\" /></p>";
                }
                form += "</div><p align=\"left\">[<a href=\"#\" id='add_" + id 
                  + "' onclick='JSONForm.addToList(\"" + id + "\", " 
                  + (parseInt(i) + 1) + ");'>+</a>]</p>";
            }
            form += "</td></tr>";
        }
    }
    form += "</table>";
    this._form.html (form);
}

JSONForm.readList = function (list) {
    var rc = [];
    var nodes = list.find("input[type='text']").toArray();
    for (var i in nodes)
      if (nodes[i].value.length > 0)
        rc.push (nodes[i].value);
    return rc;
}

JSONForm.serialize = function () {
    var root = {};
    if (this._source.html().length > 0) {
      root = JSON.parse (this._source.html());
    }
    for (k in this._schema.mapping) {
        var field = this._schema.mapping[k];
        if (field.hidden != true) {
            var value = "";
            if (field.type == 'str' || field.type == 'text')
                value = $("#field_"+k).val().trim ();
            else if (field.type == 'seq')
                value = this.readList ($("#field_"+k));

            if (value.length > 0)
              root[k] = value;
            else
              delete (root[k]);
        }
    }
    //alert (JSON.stringify(root));
    this._source.html (JSON.stringify(root));
}


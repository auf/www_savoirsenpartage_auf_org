function urlencode(str) {
    return escape(unescape(str)).replace(/\+/g,'%2B').replace(
                 /%20/g, '+').replace(/\*/g, '%2A').replace(
                 /\//g, '%2F').replace(/@/g, '%40');
}
function getUrlVars()
{
    var vars = {};
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        var hash = hashes[i].split('=');
        vars[hash[0]] = hash[1];
    }
    return vars;
}
function makeLink (page) {
    var params = getUrlVars ();
    params.page = page;
    var rc = "?";
    for (k in params) {
        rc += k + "=" + urlencode(params[k]) + "&";
    }
    rc = rc.substr (0, rc.length - 1);
    return rc;
}
function makePageLinks (currentPage, lastPage, more) {
    var span = $("#pageLinks");
    // Premiere page
    if (currentPage == 0)
      span.append ('<span class="lien-texte">&lt;&lt;</span>&nbsp;&nbsp;');
    else
      span.append ('<a href="' + makeLink(0) + 
                   '"><span class="lien-texte">&lt;&lt;</span></a>&nbsp;&nbsp;');

    // Boucle
    var f = currentPage - 4;
    var t = 0;
    if (f < 0) { t = -f; f = 0; }
    t += currentPage + 4;
    if (t > lastPage) t = lastPage;

    for (var i = f; i <= t; i++) {
        var display = i + 1;
        if (i == currentPage)
          span.append ("<span>" + display + "</span>&nbsp;&nbsp;");
        else
          span.append ('<a href="' + makeLink(i) + '"><span>' + 
                       display + '</span></a>&nbsp;&nbsp;');
    }

    // Derniere page
    if (currentPage == lastPage)
      span.append ('<span class="lien-texte">&gt;&gt;</span>');
    else
      span.append ('<a href="' + makeLink(lastPage) + 
                   '"><span class="lien-texte">&gt;&gt;</span></a>');

    if (more.length > 0)
      span.append ('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 
                   '<a href="'+more+'"><span class="lien-texte">Plus de résultats</span></a>');
}

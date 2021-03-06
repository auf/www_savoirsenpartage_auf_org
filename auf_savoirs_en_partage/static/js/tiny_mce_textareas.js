tinyMCE.init({
    mode: 'textareas',
    plugins: 'nonbreaking,paste',
    theme: 'advanced',
    theme_advanced_blockformats: 'p,h1,h2,h3,dt,dd',
    theme_advanced_toolbar_align: 'left',
    theme_advanced_toolbar_location: 'top',
    theme_advanced_buttons1: 'formatselect,bold,italic,underline,strikethrough,sub,sup,removeformat,|,justifyleft,justifycenter,justifyright,justifyfull,|,bullist,numlist,|,outdent,indent',
    theme_advanced_buttons2: 'cut,copy,paste,|,undo,redo,|,link,unlink,anchor,|,nonbreaking,|,code',
    theme_advanced_buttons3: '',
    theme_advanced_statusbar_location: 'bottom',
    theme_advanced_resizing: true,
    relative_urls: false,
    language: 'fr',
    entity_encoding: 'raw',
    height: '400',
    body_id: 'contenu',
    content_css: '/media/css/global.css',
    valid_elements : '@[id|class|style|title|dir<ltr?rtl|lang|xml::lang|onclick|ondblclick|onmousedown|onmouseup|onmouseover|onmousemove|onmouseout|onkeypress|onkeydown|onkeyup],a[rel|rev|charset|hreflang|tabindex|accesskey|type|name|href|target|title|class|onfocus|onblur],strong/b,em/i,strike,u,#p,-ol[type|compact],-ul[type|compact],-li,br,img[longdesc|usemap|src|border|alt=|title|hspace|vspace|width|height|align],-sub,-sup,-blockquote[cite],-table[border|cellspacing|cellpadding|width|frame|rules|height|align|summary|bgcolor|background|bordercolor],-tr[rowspan|width|height|align|valign|bgcolor|background|bordercolor],tbody,thead,tfoot,#td[colspan|rowspan|width|height|align|valign|bgcolor|background|bordercolor|scope],#th[colspan|rowspan|width|height|align|valign|scope],caption,-div,-span,-code,-pre,address,-h1,-h2,-h3,-h4,-h5,-h6,hr[size|noshade],-font[face|size|color],dd,dl,dt,cite,abbr,acronym,del[datetime|cite],ins[datetime|cite],object[classid|width|height|codebase|*],param[name|value],embed[type|width|height|src|*],script[src|type],map[name],area[shape|coords|href|alt|target],bdo,button,col[align|char|charoff|span|valign|width],colgroup[align|char|charoff|span|valign|width],dfn,fieldset,form[action|accept|accept-charset|enctype|method],input[accept|alt|checked|disabled|maxlength|name|readonly|size|src|type|value|tabindex|accesskey],kbd,label[for],legend,noscript,optgroup[label|disabled],option[disabled|label|selected|value],q[cite],samp,select[disabled|multiple|name|size],small,textarea[cols|rows|disabled|name|readonly],tt,var,big,iframe[align<bottom?left?middle?right?top|class|frameborder|height|id|longdesc|marginheight|marginwidth|name|scrolling<auto?no?yes|src|style|title|width]'
});

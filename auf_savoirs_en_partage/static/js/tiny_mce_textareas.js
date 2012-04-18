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
    content_css: '/media/css/global.css'
});

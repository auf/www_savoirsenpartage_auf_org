(function(){if(window.google&&google.gears){return;}var factory=null;if(typeof GearsFactory!='undefined'){factory=new GearsFactory();}else{try{factory=new ActiveXObject('Gears.Factory');if(factory.getBuildInfo().indexOf('ie_mobile')!=-1){factory.privateSetGlobalObject(this);}}catch(e){if((typeof navigator.mimeTypes!='undefined')&&navigator.mimeTypes["application/x-googlegears"]){factory=document.createElement("object");factory.style.display="none";factory.width=0;factory.height=0;factory.type="application/x-googlegears";document.documentElement.appendChild(factory);}}}if(!factory){return;}if(!window.google){google={};}if(!google.gears){google.gears={factory:factory};}})(); if(typeof deconcept=="undefined"){var deconcept=new Object();}if(typeof deconcept.util=="undefined"){deconcept.util=new Object();}if(typeof deconcept.SWFObjectUtil=="undefined"){deconcept.SWFObjectUtil=new Object();}deconcept.SWFObject=function(_1,id,w,h,_5,c,_7,_8,_9,_a){if(!document.getElementById){return;}this.DETECT_KEY=_a?_a:"detectflash";this.skipDetect=deconcept.util.getRequestParameter(this.DETECT_KEY);this.params=new Object();this.variables=new Object();this.attributes=new Array();if(_1){this.setAttribute("swf",_1);}if(id){this.setAttribute("id",id);}if(w){this.setAttribute("width",w);}if(h){this.setAttribute("height",h);}if(_5){this.setAttribute("version",new deconcept.PlayerVersion(_5.toString().split(".")));}this.installedVer=deconcept.SWFObjectUtil.getPlayerVersion();if(!window.opera&&document.all&&this.installedVer.major>7){deconcept.SWFObject.doPrepUnload=true;}if(c){this.addParam("bgcolor",c);}var q=_7?_7:"high";this.addParam("quality",q);this.setAttribute("useExpressInstall",false);this.setAttribute("doExpressInstall",false);var _c=(_8)?_8:window.location;this.setAttribute("xiRedirectUrl",_c);this.setAttribute("redirectUrl","");if(_9){this.setAttribute("redirectUrl",_9);}};deconcept.SWFObject.prototype={useExpressInstall:function(_d){this.xiSWFPath=!_d?"expressinstall.swf":_d;this.setAttribute("useExpressInstall",true);},setAttribute:function(_e,_f){this.attributes[_e]=_f;},getAttribute:function(_10){return this.attributes[_10];},addParam:function(_11,_12){this.params[_11]=_12;},getParams:function(){return this.params;},addVariable:function(_13,_14){this.variables[_13]=_14;},getVariable:function(_15){return this.variables[_15];},getVariables:function(){return this.variables;},getVariablePairs:function(){var _16=new Array();var key;var _18=this.getVariables();for(key in _18){_16[_16.length]=key+"="+_18[key];}return _16;},getSWFHTML:function(){var _19="";if(navigator.plugins&&navigator.mimeTypes&&navigator.mimeTypes.length){if(this.getAttribute("doExpressInstall")){this.addVariable("MMplayerType","PlugIn");this.setAttribute("swf",this.xiSWFPath);}_19="<embed type=\"application/x-shockwave-flash\" src=\""+this.getAttribute("swf")+"\" width=\""+this.getAttribute("width")+"\" height=\""+this.getAttribute("height")+"\" style=\""+this.getAttribute("style")+"\"";_19+=" id=\""+this.getAttribute("id")+"\" name=\""+this.getAttribute("id")+"\" ";var _1a=this.getParams();for(var key in _1a){_19+=[key]+"=\""+_1a[key]+"\" ";}var _1c=this.getVariablePairs().join("&");if(_1c.length>0){_19+="flashvars=\""+_1c+"\"";}_19+="/>";}else{if(this.getAttribute("doExpressInstall")){this.addVariable("MMplayerType","ActiveX");this.setAttribute("swf",this.xiSWFPath);}_19="<object id=\""+this.getAttribute("id")+"\" classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\" width=\""+this.getAttribute("width")+"\" height=\""+this.getAttribute("height")+"\" style=\""+this.getAttribute("style")+"\">";_19+="<param name=\"movie\" value=\""+this.getAttribute("swf")+"\" />";var _1d=this.getParams();for(var key in _1d){_19+="<param name=\""+key+"\" value=\""+_1d[key]+"\" />";}var _1f=this.getVariablePairs().join("&");if(_1f.length>0){_19+="<param name=\"flashvars\" value=\""+_1f+"\" />";}_19+="</object>";}return _19;},write:function(_20){if(this.getAttribute("useExpressInstall")){var _21=new deconcept.PlayerVersion([6,0,65]);if(this.installedVer.versionIsValid(_21)&&!this.installedVer.versionIsValid(this.getAttribute("version"))){this.setAttribute("doExpressInstall",true);this.addVariable("MMredirectURL",escape(this.getAttribute("xiRedirectUrl")));document.title=document.title.slice(0,47)+" - Flash Player Installation";this.addVariable("MMdoctitle",document.title);}}if(this.skipDetect||this.getAttribute("doExpressInstall")||this.installedVer.versionIsValid(this.getAttribute("version"))){var n=(typeof _20=="string")?document.getElementById(_20):_20;n.innerHTML=this.getSWFHTML();return true;}else{if(this.getAttribute("redirectUrl")!=""){document.location.replace(this.getAttribute("redirectUrl"));}}return false;}};deconcept.SWFObjectUtil.getPlayerVersion=function(){var _23=new deconcept.PlayerVersion([0,0,0]);if(navigator.plugins&&navigator.mimeTypes.length){var x=navigator.plugins["Shockwave Flash"];if(x&&x.description){_23=new deconcept.PlayerVersion(x.description.replace(/([a-zA-Z]|\s)+/,"").replace(/(\s+r|\s+b[0-9]+)/,".").split("."));}}else{if(navigator.userAgent&&navigator.userAgent.indexOf("Windows CE")>=0){var axo=1;var _26=3;while(axo){try{_26++;axo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash."+_26);_23=new deconcept.PlayerVersion([_26,0,0]);}catch(e){axo=null;}}}else{try{var axo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");}catch(e){try{var axo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");_23=new deconcept.PlayerVersion([6,0,21]);axo.AllowScriptAccess="always";}catch(e){if(_23.major==6){return _23;}}try{axo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash");}catch(e){}}if(axo!=null){_23=new deconcept.PlayerVersion(axo.GetVariable("$version").split(" ")[1].split(","));}}}return _23;};deconcept.PlayerVersion=function(_29){this.major=_29[0]!=null?parseInt(_29[0]):0;this.minor=_29[1]!=null?parseInt(_29[1]):0;this.rev=_29[2]!=null?parseInt(_29[2]):0;};deconcept.PlayerVersion.prototype.versionIsValid=function(fv){if(this.major<fv.major){return false;}if(this.major>fv.major){return true;}if(this.minor<fv.minor){return false;}if(this.minor>fv.minor){return true;}if(this.rev<fv.rev){return false;}return true;};deconcept.util={getRequestParameter:function(_2b){var q=document.location.search||document.location.hash;if(_2b==null){return q;}if(q){var _2d=q.substring(1).split("&");for(var i=0;i<_2d.length;i++){if(_2d[i].substring(0,_2d[i].indexOf("="))==_2b){return _2d[i].substring((_2d[i].indexOf("=")+1));}}}return "";}};deconcept.SWFObjectUtil.cleanupSWFs=function(){var _2f=document.getElementsByTagName("OBJECT");for(var i=_2f.length-1;i>=0;i--){_2f[i].style.display="none";for(var x in _2f[i]){if(typeof _2f[i][x]=="function"){_2f[i][x]=function(){};}}}};if(deconcept.SWFObject.doPrepUnload){if(!deconcept.unloadSet){deconcept.SWFObjectUtil.prepUnload=function(){__flash_unloadHandler=function(){};__flash_savedUnloadHandler=function(){};window.attachEvent("onunload",deconcept.SWFObjectUtil.cleanupSWFs);};window.attachEvent("onbeforeunload",deconcept.SWFObjectUtil.prepUnload);deconcept.unloadSet=true;}}if(!document.getElementById&&document.all){document.getElementById=function(id){return document.all[id];};}var getQueryParamValue=deconcept.util.getRequestParameter;var FlashObject=deconcept.SWFObject;var SWFObject=deconcept.SWFObject;;(function($){var $scrollTo=$.scrollTo=function(target,duration,settings){$(window).scrollTo(target,duration,settings);};$scrollTo.defaults={axis:'y',duration:1};$scrollTo.window=function(scope){return $(window).scrollable();};$.fn.scrollable=function(){return this.map(function(){var win=this.parentWindow||this.defaultView,elem=this.nodeName=='#document'?win.frameElement||win:this,doc=elem.contentDocument||(elem.contentWindow||elem).document,isWin=elem.setInterval;return elem.nodeName=='IFRAME'||isWin&&$.browser.safari?doc.body:isWin?doc.documentElement:this;});};$.fn.scrollTo=function(target,duration,settings){if(typeof duration=='object'){settings=duration;duration=0;}if(typeof settings=='function')settings={onAfter:settings};settings=$.extend({},$scrollTo.defaults,settings);duration=duration||settings.speed||settings.duration;settings.queue=settings.queue&&settings.axis.length>1;if(settings.queue)duration/=2;settings.offset=both(settings.offset);settings.over=both(settings.over);return this.scrollable().each(function(){var elem=this,$elem=$(elem),targ=target,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case 'number':case 'string':if( /^([+-]=)?\d+(px)?$/.test(targ)){targ=both(targ);break;}targ=$(targ,this);case 'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset();}$.each(settings.axis.split(''),function(i,axis){var Pos=axis=='x'?'Left':'Top',pos=Pos.toLowerCase(),key='scroll'+Pos,old=elem[key],Dim=axis=='x'?'Width':'Height',dim=Dim.toLowerCase();if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(settings.margin){attr[key]-=parseInt(targ.css('margin'+Pos))||0;attr[key]-=parseInt(targ.css('border'+Pos+'Width'))||0;}attr[key]+=settings.offset[pos]||0;if(settings.over[pos])attr[key]+=targ[dim]()* settings.over[pos];}else attr[key]=targ[pos];if( /^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max(Dim));if(!i&&settings.queue){if(old!=attr[key])animate(settings.onAfterFirst);delete attr[key];}});animate(settings.onAfter);function animate(callback){$elem.animate(attr,duration,settings.easing,callback&&function(){callback.call(this,target,settings);});};function max(Dim){var attr='scroll'+Dim,doc=elem.ownerDocument;return win?Math.max(doc.documentElement[attr],doc.body[attr]):elem[attr];};}).end();};function both(val){return typeof val=='object'?val:{top:val,left:val};};})(jQuery);(function($){var id=0;$.multiUpload=function(s){var up=this,mul;up.id=up.generateID();up.settings={};up.settings=s=$.extend(up.settings,s);if(s.max_size)s.max_size=up.parseSize(s.max_size);if(s.chunk_size)s.chunk_size=up.parseSize(s.chunk_size);if(s.oninit){$(up).bind('multiUpload:init',function(){s.oninit.call(up,up);});}up.init();$(['setup','filesSelected','fileProgress','filesProgress','filesUploaded','fileUploaded','fileUploadProgress']).each(function(){if(s[(this)])$(up).bind('multiUpload:'+this,s[(this)]);});$(up).trigger('multiUpload:setup');$(up).bind('multiUpload:selectFiles',function(){this.cache={};});$(up).bind('multiUpload:filesSelected',function(e,fs){var mx=up.settings.max_size;function filter(f){var m= /\.([^.]+)$/.exec(f.name.toLowerCase()),ext=m?m[1]:null;return ext&&$.inArray(ext,s.filter)!=-1&&(!mx||f.size<mx);};if(s.filter[0]!='*'){this.files=$.grep(this.files,filter);fs.files=$.grep(fs.files,filter);}this.cache={};});};$.extend($.multiUpload.prototype,{files:[],cache:{},listeners:{},status:0,init:function(){},repaint:function(){},selectFiles:function(){$(this).trigger('multiUpload:selectFiles');},startUpload:function(){this.status=1;$(this).trigger('multiUpload:startUpload');this.uploadNext();},stopUpload:function(){this.status=0;$(this).trigger('multiUpload:stopUpload');},uploadNext:function(){var i,fl=this.files;if(!this.status)return;for(i=0;i<fl.length;i++){if(!fl[i].status){$(this).trigger('multiUpload:uploadFile',[fl[i]]);return;}}this.stopUpload();},getFile:function(id){var t=this,f,i,fl=t.files;if(f=t.cache[id])return f;for(i=0;i<fl.length;i++){if(fl[i].id==id)return t.cache[id]=fl[i];}},removeFile:function(id){var up=this,f;up.files=$.grep(up.files,function(v){if(v.id==id)f=v;return v.id!=id;});$(this).trigger('multiUpload:removeFile',f);$(this).trigger('multiUpload:filesChanged');},clearFiles:function(){this.stopUpload();this.files=[];this.cache={};$(this).trigger('multiUpload:clearFiles');$(this).trigger('multiUpload:filesChanged');},formatSize:function(v){if(v>1048576)return Math.round(v/1048576,1)+" MB";if(v>1024)return Math.round(v/1024,1)+" KB";return v+" b";},generateID:function(){return 'u'+(id++);},parseSize:function(sz){var mul;if(typeof(sz)=='string'){sz= /^([0-9]+)([mk]+)$/.exec(sz.toLowerCase().replace(/[^0-9mk]/g,''));mul=sz[2];sz=parseInt(sz[1]);if(mul=='m')sz *=1048576;if(mul=='k')sz *=1024;}return sz;}});$.extend($.multiUpload,{instances:{},create:function(s){return this.add(new $.multiUpload(s));},remove:function(id){if(this.get(id))delete this.instances[id];},add:function(up){return this.instances[up.id]=up;},get:function(id){return this.instances[id];}});})(jQuery);(function($){if(!$.multiUpload.initialized&&window.google&&google.gears){$.multiUpload.initialized=1;$.multiUpload.runtime='gears';$.extend($.multiUpload.prototype,{init:function(){var up=this;$(up).trigger('multiUpload:init');$(up).bind('multiUpload:selectFiles',function(e){var up=this,desk=google.gears.factory.create('beta.desktop'),s={};if(up.settings.filter[0]!='*')s.filter=$.map(up.settings.filter,function(v){return '.'+v});desk.openFiles(function(f){var sf=[];if(f.length){up._fireEvent('multiUpload:beforeFilesSelected');$(f).each(function(){var fo={id:up.generateID(),name:this.name,blob:this.blob,size:this.blob.length,loaded:0};up.files.push(fo);sf.push(fo);});up._fireEvent('multiUpload:filesSelected',[{files:sf}]);up._fireEvent('multiUpload:filesChanged');}else up._fireEvent('multiUpload:filesSelectionCancelled');},s);});$(up).bind('multiUpload:uploadFile',function(e,fo){var req,up=this,chunkSize,chunk=0,chunks,i,start,loaded=0,curChunkSize;chunkSize=up.settings.chunk_size||1024 * 1024;chunks=Math.ceil(fo.blob.length/chunkSize);uploadNextChunk();function uploadNextChunk(){var url=up.settings.upload_url;if(fo.status)return;curChunkSize=Math.min(chunkSize,fo.blob.length-(chunk * chunkSize));req=google.gears.factory.create('beta.httprequest');req.open('POST',url+(url.indexOf('?')==-1?'?':'&')+'name='+escape(fo.name)+'&chunk='+chunk+'&chunks='+chunks+'&path='+escape(up.settings.path));req.setRequestHeader('Content-Disposition','attachment; filename="'+fo.name+'"');req.setRequestHeader('Content-Type','application/octet-stream');req.setRequestHeader('Content-Range','bytes '+chunk * chunkSize);req.upload.onprogress=function(pr){fo.loaded=loaded+pr.loaded;up._fireEvent('multiUpload:fileUploadProgress',[{file:fo,loaded:fo.loaded,total:fo.size}]);};req.onreadystatechange=function(){var ar;if(req.readyState==4){if(req.status==200){ar={file:fo,chunk:chunk,chunks:chunks,response:req.responseText};up._fireEvent('multiUpload:chunkUploaded',[ar]);if(ar.cancel){fo.status='failed';up._fireEvent('multiUpload:filesChanged');up.uploadNext();return;}loaded+=curChunkSize;if(++chunk>=chunks){fo.status='completed';up._fireEvent('multiUpload:fileUploaded',[{file:fo,response:req.responseText}]);up._fireEvent('multiUpload:filesChanged');up.uploadNext();}else uploadNextChunk();}else up._fireEvent('multiUpload:uploadChunkError',[{file:fo,chunk:chunk,chunks:chunks,error:'Status: '+req.status}]);}};if(chunk<chunks)req.send(fo.blob.slice(chunk * chunkSize,curChunkSize));};});},_fireEvent:function(ev,ar){$(this).trigger(ev,ar);}});}})(jQuery);(function($){function getFlashVersion(){var v;try{v=navigator.plugins['Shockwave Flash'];v=v.description;}catch(ex){try{v=new ActiveXObject('ShockwaveFlash.ShockwaveFlash').GetVariable('$version');}catch(ex){v='0.0';}}v=v.match(/\d+/g);return parseFloat(v[0]+'.'+v[1]);};if(!$.multiUpload.initialized&&getFlashVersion()>=10){$.multiUpload.initialized=1;$.multiUpload.runtime='flash';$.multiUpload.instances=[];$.multiUpload._fireEvent=function(na,p1,p2,p3,p4){window.setTimeout(function(){$($.multiUpload.instances).each(function(i,v){$(v).trigger('multiUpload:'+na,[p1,p2,p3,p4]);v.repaint();});},0);};$.extend($.multiUpload.prototype,{getFlash:function(){return $('#flashuploader')[0];},repaint:function(){var up=this,fb=$(up.settings.flash_browse_button),off=fb.offset();up.flashContainer.css({position:'absolute',top:off.top,left:off.left,width:fb.width(),height:fb.height(),backgr2ound:'red'});},init:function(){var up=this,s=up.settings,so,fb;$.multiUpload.instances.push(up);$(up).bind('multiUpload:flashInit',function(e){$(up).trigger('multiUpload:init');});$(document.body).append('<div id="flashUploaderContainer"></div>');so=new SWFObject("js/jquery/jquery.multiupload.flash.swf","flashuploader","100%","100%","10.0");so.addVariable("file_filter",$.map(up.settings.filter,function(v){return '*.'+v}).join(';'));so.addParam("wmode","transparent");so.write("flashUploaderContainer");up.flashContainer=$('#flashUploaderContainer');$(function(e){up.repaint();});up.repaint();$(up).bind('multiUpload:flashSelectFiles',function(e,sel){$(sel).each(function(i,fo){up.files.push(fo);});$(up).trigger('multiUpload:filesSelected',[{files:sel}]);$(up).trigger('multiUpload:filesChanged');});$(up).bind('multiUpload:flashUploadComplete',function(e,o){var fo;if(fo=up.getFile(o.id)){if(!fo.status){fo.status='completed';$(up).trigger('multiUpload:fileUploaded',[{file:fo,response:o.text}]);}}$(up).trigger('multiUpload:filesChanged');up.uploadNext();});$(up).bind('multiUpload:flashUploadProcess',function(e,pr){var fo=up.getFile(pr.id);if(!fo.status){fo.loaded=pr.loaded;$(up).trigger('multiUpload:fileUploadProgress',[{file:fo,loaded:fo.loaded,total:fo.size}]);}});$(up).bind('multiUpload:flashIOError',function(e,o){var fo;if(fo=up.getFile(o.id)){if(!fo.status){fo.status='failed';$(up).trigger('multiUpload:uploadChunkError',[{file:fo,error:o.message}]);}}});$(up).bind('multiUpload:stopUpload',function(e){up.getFlash().cancelUpload();});$(up).bind('multiUpload:removeFile',function(e,fo){up.getFlash().removeFile(fo.id);});$(up).bind('multiUpload:clearFiles',function(e){up.getFlash().clearFiles();});$(up).bind('multiUpload:uploadFile',function(e,fo){var pageURL=document.location.href.replace(/\/[^\/]+$/g,'/');up.getFlash().uploadFile(fo.id,{upload_url:pageURL+up.settings.upload_url+'&path='+escape(up.settings.path)+'&name='+escape(fo.name),chunk_size:up.settings.chunk_size,file_field:'file0',post_args:{name0:fo.name}});});$(up).bind('multiUpload:flashUploadChunkComplete',function(e,o){var fo=up.getFile(o.id),arg;arg={file:fo,chunk:o.chunk,chunks:o.chunks,response:o.text};if(!fo.status)$(up).trigger('multiUpload:chunkUploaded',[arg]);if(arg.cancel){fo.status='failed';up.getFlash().cancelUpload();}});}});}})(jQuery); function onSilverlightError(sender,args){alert("onSilverlightError: "+args.errormessage);};(function($){function isInstalled(version){var isVersionSupported=false;var container=null;try{var control=null;try{control=new ActiveXObject('AgControl.AgControl');if(version==null)isVersionSupported=true;else if(control.IsVersionSupported(version))isVersionSupported=true;control=null;}catch(e){var plugin=navigator.plugins["Silverlight Plug-In"];if(plugin){if(version===null){isVersionSupported=true;}else{var actualVer=plugin.description;if(actualVer==="1.0.30226.2")actualVer="2.0.30226.2";var actualVerArray=actualVer.split(".");while(actualVerArray.length>3)actualVerArray.pop();while(actualVerArray.length<4)actualVerArray.push(0);var reqVerArray=version.split(".");while(reqVerArray.length>4)reqVerArray.pop();var requiredVersionPart,actualVersionPart,index=0;do{requiredVersionPart=parseInt(reqVerArray[index]);actualVersionPart=parseInt(actualVerArray[index]);index++;}while(index<reqVerArray.length&&requiredVersionPart===actualVersionPart);if(requiredVersionPart<=actualVersionPart&&!isNaN(requiredVersionPart))isVersionSupported=true;}}}}catch(e){isVersionSupported=false;}return isVersionSupported;};if(!$.multiUpload.initialized&&isInstalled('2.0.31005.0')){$.multiUpload.initialized=1;$.multiUpload.runtime='silverlight';$.multiUpload.setup=function(se){$.multiUpload.plugin=$('#multiuploader')[0].content.Upload;$.multiUpload._fireEvent('init');};$.multiUpload.instances=[];$.multiUpload._fireEvent=function(na,p1,p2,p3,p4){window.setTimeout(function(){$($.multiUpload.instances).each(function(i,v){$(v).trigger('multiUpload:'+na,[p1,p2,p3,p4]);});},0);};$.extend($.multiUpload.prototype,{init:function(){var up=this,sel=[];$.multiUpload.instances.push(up);if(!$('#multiuploader')[0]){$("body").append('<object id="multiuploader" data="data:application/x-silverlight," type="application/x-silverlight-2" width="100" height="100">'+'<param name="source" value="'+up.settings.silverlight_xap_url+'"/>'+'<param name="onerror" value="onSilverlightError" /></object>');}$(up).bind('multiUpload:slSelectFile',function(e,id,na,sz){var fo={id:id,name:na,size:sz,loaded:0};sel.push(fo);up.files.push(fo);});$(up).bind('multiUpload:slSelectSuccessful',function(){$(up).trigger('multiUpload:filesSelected',[{files:sel}]);$(up).trigger('multiUpload:filesChanged');sel=[];});$(up).bind('multiUpload:slSelectCancelled',function(){$(up).trigger('multiUpload:filesSelectionCancelled',[sel]);sel=[];});$(up).bind('multiUpload:slUploadFileProgress',function(e,id,lod,tot){var file=up.getFile(id);file.loaded=lod;$(up).trigger('multiUpload:fileUploadProgress',[{file:file,loaded:lod,total:tot}]);});$(up).bind('multiUpload:slUploadSuccessful',function(e,id,resp){var fo;if(fo=up.getFile(id)){if(!fo.status){fo.status="completed";$(up).trigger('multiUpload:fileUploaded',[{file:fo,response:resp}]);}}$(up).trigger('multiUpload:filesChanged');up.uploadNext();});$(up).bind('multiUpload:stopUpload',function(e){$.multiUpload.plugin.CancelUpload();});$(up).bind('multiUpload:slUploadChunkSuccessful',function(e,id,chunk,chunks,resp){var fo=up.getFile(id),ar={file:fo,chunk:chunk,chunks:chunks,response:resp};$(up).trigger('multiUpload:chunkUploaded',[ar]);if(ar.cancel){fo.status="failed";$.multiUpload.plugin.CancelUpload();}});$(up).bind('multiUpload:slUploadChunkError',function(e,id,chunk,chunks,err){$(up).trigger('multiUpload:uploadChunkError',[{file:up.getFile(id),chunk:chunk,chunks:chunks,error:err}]);});$(up).bind('multiUpload:selectFiles',function(e){$.multiUpload.plugin.SelectFiles('Files |'+$.map(up.settings.filter,function(v){return '*.'+v}).join(';'));});$(up).bind('multiUpload:removeFile',function(e,fo){$.multiUpload.plugin.RemoveFile(fo.id);});$(up).bind('multiUpload:uploadFile',function(e,fo){$.multiUpload.plugin.UploadFile(fo.id,up.settings.upload_url+'&name='+escape(fo.name)+"&path="+escape(up.settings.path),parseInt(up.settings.chunk_size));});$(up).bind('multiUpload:clearFiles',function(e){$.multiUpload.plugin.ClearFiles();});}});}})(jQuery);(function($){window.UploadDialog={currentWin:$.WindowManager.find(window),init:function(){var t=this,args;t.args=args=$.extend({path:'{default}',visual_path:'/'},t.currentWin.getArgs());t.fileListTpl=$.templateFromScript('#filelist_item_template');$('.uploadtype').html($.translate('{#upload.basic_upload}',0,{a:'<a id="singleupload" href="#basic">','/a':'</a>'}));$('#createin').html(args.visual_path);$('form input[name=path]').val(args.path);$('form input[name=file0]').change(function(e){$('form input[name=name0]').val(t.cleanName(/([^\/\\]+)$/.exec(e.target.value)[0].replace(/\.[^\.]+$/,'')));});$('form').submit(function(){$.WindowManager.showProgress({message:$.translate('{#upload.progress}')});});if(document.location.hostname!=document.domain)$('form input[name=domain]').val(document.domain);t.path=args.path;$('#singleupload').click(function(e){$('#multiupload_view').hide();$('#singleupload_view').show();});RPC.exec('fm.getConfig',{path:args.path},function(data){var config=data.result,maxSize,upExt,fsExt,outExt=[],i,x,found;maxSize=config['upload.maxsize'];fsExt=config['filesystem.extensions'].split(',');upExt=config['upload.extensions'].split(',');t.debug=config['general.debug']=="true";t.shouldCleanNames=config['filesystem.clean_names']=="true";t.chunkSize=config['upload.chunk_size']||'1mb';$('#content').show();if($.multiUpload.initialized)$('#multiupload_view').show();else $('#singleupload_view').show();if(config['upload.multiple_upload']!="true"){$('#multiupload_view').hide();$('#singleupload_view').show();}maxSize=maxSize.replace(/\s+/,'');maxSize=maxSize.replace(/([0-9]+)/g,'$1 ');if(upExt[0]=='*')upExt=fsExt;if(fsExt[0]=='*')fsExt=upExt;for(i=0;i<upExt.length;i++){upExt[i]=$.trim(upExt[i].toLowerCase());found=false;for(x=0;x<fsExt.length;x++){fsExt[x]=$.trim(fsExt[x]).toLowerCase();if(upExt[i]==fsExt[x]){found=true;break;}}if(found)outExt.push(upExt[i]);}t.validExtensions=outExt;t.maxSize=maxSize;$('#facts').html($.templateFromScript('#facts_template'),{extensions:outExt.join(', '),maxsize:maxSize,path:args.visual_path});if(config['upload.multiple_upload']=="true")t.initMultiUpload();});$('#cancel').click(function(){t.currentWin.close();});},cleanName:function(s){if(this.shouldCleanNames)s=$.cleanName(s);return s;},handleSingleUploadResponse:function(data){var t=this,args=t.currentWin.getArgs();$.WindowManager.hideProgress();if(!RPC.handleError({message:'{#error.upload_failed}',visual_path:t.args.visual_path,response:data})){var res=RPC.toArray(data.result);$.WindowManager.info($.translate('{#message.upload_ok}'));$('#file0, #name0').val('');t.insertFiles([res[0].file]);}},initMultiUpload:function(){var t=this,up,args=t.currentWin.getArgs(),initial=1,startTime;up=$.multiUpload.create({silverlight_xap_url:'../../stream/index.php?theme=fm&package=static_files&file=multiupload_xap',upload_url:'../../stream/index.php?cmd=fm.upload',path:t.path,filter:t.validExtensions,chunk_size:t.chunkSize,max_size:t.maxSize,flash_browse_button:'#add',oninit:function(){$('#add').removeClass('hidden');}});if(t.debug)alert('Runtime used: '+$.multiUpload.runtime);function calc(up){var size=0,uploaded=0,loaded=0,unloaded=0,bps=0,finished=true,fl=[];if(!up.files.length){$('#selectview').css('top',0);$('#selectview').show();$('#fileblock').css({position:'relative',top:400});initial=1;return;}$(up.files).each(function(i,f){size+=f.size;loaded+=f.loaded;if(f.status=='completed')uploaded++;if(!f.status)finished=false;});bps=Math.ceil(loaded / ((new Date().getTime() - startTime || 1) / 1000.0));if(finished){$('#abortupload').hide();$(up.files).each(function(i,f){if(f.status=='completed')fl.push(t.path+'/'+f.name);});t.insertFiles(fl);$('#progressbar').css('width','100%');return;}$('#progressinfo').html($.translate('{#upload.progressinfo}',1,{loaded:up.formatSize(loaded),total:up.formatSize(size),speed:up.formatSize(bps)}));$('#progressbar').css('width',Math.round(loaded/size * 100.0)+'%');$('#stats').html($.translate('{#upload.statusrow}',1,{files:up.files.length,size:up.formatSize(size)}));};$(up).bind('multiUpload:filesSelected',function(e,fs){var up=this,totalSize=0;if(!fs.files.length){$.WindowManager.info($.translate('{#upload.no_valid_files}'));return;}if(initial){$('#selectview').animate({top:'-150px'},1000);$('#fileblock').animate({top:'-60px'},1000,'linear',function(){$('#fileblock').css('position','static');$('#selectview').hide();up.repaint();});initial=0;}$(fs.files).each(function(i,fo){fo.name=t.cleanName(fo.name);$('#files').show();$('#files tbody').append(t.fileListTpl,{id:fo.id,name:fo.name,size:fo.size});$('#'+fo.id+' a.remove').click(function(e){$('#'+fo.id).remove();$.multiUpload.get(up.id).removeFile(fo.id);e.preventDefault();return false;});$('#'+fo.id+' a.rename').click(function(e){var a=$(e.target),inp,parts;if(!a.hasClass('disabled')){parts= /^(.+)(\.[^\.]+)$/.exec(fo.name);a.hide();$(e.target).parent().append('<input id="rename" type="text" class="text" />');inp=$('#rename').val(parts[1]);t.renameEnabled=1;inp.focus().blur(function(){t.endRename();}).keydown(function(e){var c=e.keyCode;if(c==13||c==27){if(c==13){fo.name=t.cleanName(inp.val())+parts[2];a.html(fo.name);}t.endRename();}});}e.preventDefault();return false;});});up.settings.flash_browse_button='#addmore';up.repaint();$('#filelist')[0].scrollTop=0;});$(up).bind('multiUpload:fileUploaded',function(e,o){$('#'+o.file.id).removeClass('failed').addClass('done');});$(up).bind('multiUpload:filesChanged',function(){calc(up);up.repaint();t.endRename();});$(up).bind('multiUpload:fileUploadProgress',function(e,pr){if(up.status){if(!pr.file.scroll){$('#filelist').scrollTo($('#'+pr.file.id),50);pr.file.scroll=1;}$('#'+pr.file.id+' td.status').html(Math.round(pr.loaded/pr.total * 100.0)+'%');calc(up);}});$(up).bind('multiUpload:chunkUploaded',function(e,o){var res=$.parseJSON(o.response),data=RPC.toArray(res.result);if(data[0]["status"]!='OK'){o.file.loaded=o.file.size;calc(up);$('#'+o.file.id).addClass('failed');$('#'+o.file.id+' td.status').html($.translate(data[0]["message"]));o.cancel=1;}});$(up).bind('multiUpload:uploadChunkError',function(e,o){$('#'+o.file.id).addClass('failed');$('#'+o.file.id+' td.status').html('Failed').attr('title',o.error);});$('#add, #addmore').click(function(e){up.selectFiles();e.preventDefault();return false;});$('#abortupload').click(function(e){up.stopUpload();$.WindowManager.info($.translate('{#upload.cancelled}'),function(){t.currentWin.close();});});$('#uploadstart').click(function(e){$('#uploadstart').parent().hide();$('#status').show();$('#statsrow').hide();$('#files .status').html('-');$('#files .fname a').addClass('disabled');startTime=new Date().getTime();up.startUpload();e.preventDefault();return false;});$('#uploadstop').click(function(e){up.stopUpload();e.preventDefault();return false;});$('#clear').click(function(e){up.clearFiles();$('#files').hide();$('#files tbody').html('');e.preventDefault();return false;});},insertFiles:function(pa){var s=this.currentWin.getArgs();if(s.onupload){RPC.insertFiles({relative_urls:s.relative_urls,document_base_url:s.document_base_url,default_base_url:s.default_base_url,no_host:s.remove_script_host||s.no_host,paths:pa,insert_filter:s.insert_filter,oninsert:function(o){s.onupload(o);}});}},isDemo:function(){if(this.currentWin.getArgs().is_demo){$.WindowManager.info($.translate('{#error.demo}'));return true;}},endRename:function(){if(this.renameEnabled){$('#files input').remove();$('#files a').show();this.renameEnabled=0;}}};window.handleJSON=function(data){window.focus();UploadDialog.handleSingleUploadResponse(data);};$(function(e){UploadDialog.init();});})(jQuery);
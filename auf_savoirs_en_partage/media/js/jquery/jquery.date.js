/*
 * Date prototype extensions. Doesn't depend on any
 * other code. Doens't overwrite existing methods.
 *
 * Adds dayNames, abbrDayNames, monthNames and abbrMonthNames static properties and isLeapYear,
 * isWeekend, isWeekDay, getDaysInMonth, getDayName, getMonthName, getDayOfYear, getWeekOfYear,
 * setDayOfYear, addYears, addMonths, addDays, addHours, addMinutes, addSeconds methods
 *
 * Copyright (c) 2006 Jörn Zaefferer and Brandon Aaron (brandon.aaron@gmail.com || http://brandonaaron.net)
 *
 * Additional methods and properties added by Kelvin Luck: firstDayOfWeek, dateFormat, zeroTime, asString, fromString -
 * I've added my name to these methods so you know who to blame if they are broken!
 * 
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 */

 eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('g.O=[\'2a\',\'1N\',\'1s\',\'1f\',\'27\',\'1V\',\'1M\'];g.S=[\'1r\',\'1l\',\'L\',\'1a\',\'24\',\'1Z\',\'1U\'];g.Z=[\'1L\',\'Fé1A\',\'1w\',\'1q\',\'N\',\'1k\',\'1h\',\'1eût\',\'19\',\'17\',\'23\',\'Dé1Y\'];g.B=[\'1T\',\'1R\',\'L\',\'1Q\',\'N\',\'1P\',\'1K\',\'1I\',\'1F\',\'1D\',\'1z\',\'1x\'];g.1v=1;g.H=\'J/E/C\';(8(){8 h(a,b){l(!g.Y[a]){g.Y[a]=b}};h("11",8(){j y=5.A();9(y%4==0&&y%21!=0)||y%20==0});h("13",8(){9 5.v()==0||5.v()==6});h("1W",8(){9!5.13()});h("1S",8(){9[k,(5.11()?29:28),k,x,k,x,k,k,x,k,x,k][5.q()]});h("1O",8(a){9 a?g.S[5.v()]:g.O[5.v()]});h("M",8(a){9 a?g.B[5.q()]:g.Z[5.q()]});h("X",8(){j a=W g("1/1/"+5.A());9 V.1H((5.I()-a.I())/1E)});h("1C",8(){9 V.1B(5.X()/7)});h("1y",8(a){5.w(0);5.G(a);9 5});h("1u",8(a){5.P(5.A()+a);9 5});h("1t",8(a){j b=5.p();5.w(5.q()+a);l(b>5.p())5.Q(-5.p());9 5});h("Q",8(a){5.G(5.p()+a);9 5});h("1p",8(a){5.R(5.1o()+a);9 5});h("1n",8(a){5.U(5.1m()+a);9 5});h("1G",8(a){5.T(5.1j()+a);9 5});h("1i",8(){5.1J(0);5.T(0);5.U(0);5.R(0);9 5});h("1g",8(){j r=g.H;9 r.u(\'C\').n(5.A()).u(\'15\').n(5.1d()).u(\'10\').n(5.M(1c)).u(\'E\').n(e(5.q()+1)).u(\'J\').n(e(5.p()))});g.1b=8(s){j f=g.H;j d=W g(\'K/K/18\');j a=f.o(\'C\');l(a>-1){d.P(z(s.m(a,4)))}12{d.16(z(s.m(f.o(\'15\'),2)))}j b=f.o(\'10\');l(b>-1){j c=s.m(b,3);22(j i=0;i<g.B.14;i++){l(g.B[i]==c)25}d.w(i)}12{d.w(z(s.m(f.o(\'E\'),2))-1)}d.G(z(s.m(f.o(\'J\'),2)));l(26(d.I())){9 1X}9 d};j e=8(a){j s=\'0\'+a;9 s.2b(s.14-2)}})();',62,136,'|||||this|||function|return|||||||Date|add||var|31|if|substr|join|indexOf|getDate|getMonth||||split|getDay|setMonth|30||Number|getFullYear|abbrMonthNames|yyyy||mm||setDate|format|getTime|dd|01|Mar|getMonthName|Mai|dayNames|setFullYear|addDays|setHours|abbrDayNames|setSeconds|setMinutes|Math|new|getDayOfYear|prototype|monthNames|mmm|isLeapYear|else|isWeekend|length|yy|setYear|Octobre|1977|Septembre|Mer|fromString|true|getYear|Ao|Mercredi|asString|Juillet|zeroTime|getSeconds|Juin|Lun|getMinutes|addMinutes|getHours|addHours|Avril|Dim|Mardi|addMonths|addYears|firstDayOfWeek|Mars|Dec|setDayOfYear|Nov|vrier|ceil|getWeekOfYear|Oct|86400000|Sep|addSeconds|floor|Aou|setMilliseconds|Jul|Janvier|Samedia|Lundi|getDayName|Jun|Avr|Fev|getDaysInMonth|Jan|Sam|Vendredi|isWeekDay|false|cembre|Ven|400|100|for|Novembre|Jeu|break|isNaN|Jeudi|||Dimanche|substring'.split('|'),0,{}))
/* Navigation and requested local, device-level specialist gate. */
(function(){'use strict';document.documentElement.classList.add('js');
var toggle=document.querySelector('.nav-toggle'),nav=document.getElementById('site-nav');
if(toggle&&nav){function setOpen(open){toggle.setAttribute('aria-expanded',String(open));nav.setAttribute('data-open',String(open));}toggle.addEventListener('click',function(){setOpen(toggle.getAttribute('aria-expanded')!=='true');});nav.addEventListener('click',function(e){if(e.target.closest('a'))setOpen(false);});document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false);});}
if(document.documentElement.dataset.pro!=='true')return;
var key='visage.pro.access.v1',unlocked=false;try{unlocked=localStorage.getItem(key)==='granted';}catch(e){}
if(unlocked){document.documentElement.classList.remove('pro-locked');return;}
var background=Array.from(document.body.children);background.forEach(function(el){if(el.tagName!=='SCRIPT'&&el.tagName!=='NOSCRIPT')el.inert=true;});
var overlay=document.createElement('div');overlay.className='access-overlay';overlay.innerHTML='<section class="access-panel" role="dialog" aria-modal="true" aria-labelledby="access-title"><h2 id="access-title">Раздел для специалистов <em>эстетической медицины</em></h2><form id="access-form"><label for="access-code">Код доступа</label><div class="access-fields"><input id="access-code" name="code" type="password" autocomplete="off" required aria-describedby="access-error"><button type="submit">Войти</button></div><p id="access-error" class="access-error" role="status" aria-live="polite"></p></form><a class="access-return" href="baza-kozhi.html">Открытые материалы для пациентов ↗</a></section>';document.body.appendChild(overlay);
var input=overlay.querySelector('input'),form=overlay.querySelector('form');input.focus();
form.addEventListener('submit',function(e){e.preventDefault();if(input.value.trim()!=='PRO2026'){overlay.querySelector('#access-error').textContent='Неверный код. Попробуйте ещё раз.';input.setAttribute('aria-invalid','true');input.select();return;}try{localStorage.setItem(key,'granted');}catch(e){}background.forEach(function(el){el.inert=false;});document.documentElement.classList.remove('pro-locked');overlay.remove();var heading=document.querySelector('main h1');if(heading){heading.setAttribute('tabindex','-1');heading.focus();}});
overlay.addEventListener('keydown',function(e){if(e.key!=='Tab')return;var f=Array.from(overlay.querySelectorAll('input,button,a'));if(e.shiftKey&&document.activeElement===f[0]){e.preventDefault();f[f.length-1].focus();}else if(!e.shiftKey&&document.activeElement===f[f.length-1]){e.preventDefault();f[0].focus();}});
})();

/* Yandex.Metrika counter 92335892 */
if(location.protocol!=='file:'){
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
m[i].l=1*new Date();
for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
ym(92335892, "init", {
     clickmap:true,
     trackLinks:true,
     accurateTrackBounce:true,
     webvisor:true
});
}
